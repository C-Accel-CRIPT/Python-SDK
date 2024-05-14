import json
from typing import Dict, Optional, Tuple
from urllib.parse import quote

import requests
from beartype import beartype

from cript.api.exceptions import APIError
from cript.nodes.util import load_nodes_from_json


def _get_uuid_score_from_json(node_dict: Dict) -> Tuple[str, Optional[float]]:
    """
    Get the UUID string and search score from a JSON node representation if available.
    """
    node_uuid: str = node_dict["uuid"]
    node_score: Optional[float] = node_dict.get("score", None)

    return node_uuid, node_score


class Paginator:
    """
    Paginator is used to flip through different pages of data that the API returns when searching.
    > Instead of the user manipulating the URL and parameters, this object handles all of that for them.

    Using the Paginator object, the user can simply and easily flip through the results of the search.
    The details, that results are listed as pages are hidden from the user.
    The pages are automatically requested from the API as needed.

    This object implements a python iterator, so `for node in Paginator` works as expected.
    It will loop through all results of the search, returning the nodes one by one.

    !!! Warning "Do not create paginator objects"
        Please note that you are not required or advised to create a paginator object, and instead the
        Python SDK API object will create a paginator for you, return it, and let you simply use it

    """

    _url_path: str
    _query: str
    _current_position: int
    _fetched_nodes: list
    _uuid_search_score_map: Dict
    _number_fetched_pages: int = 0
    _limit_node_fetches: Optional[int] = None
    _start_after_uuid: Optional[str] = None
    _start_after_score: Optional[float] = None
    auto_load_nodes: bool = True

    @beartype
    def __init__(self, api, url_path: str, query: str, limit_node_fetches: Optional[int] = None):
        """
        create a paginator

        1. set all the variables coming into constructor
        1. then prepare any variable as needed e.g. strip extra spaces or url encode query

        Parameters
        ----------
        api: cript.API
           Object through which the API call is routed.
        url_path: str
            query URL used.
        query: str
            the value the user is searching for
        limit_node_fetches: Optional[int] = None
            limits the number of nodes fetches through this call.

        Returns
        -------
        None
            instantiate a paginator
        """
        self._api = api
        self._fetched_nodes = []
        self._current_position = 0
        self._limit_node_fetches = limit_node_fetches
        self._uuid_search_score_map = {}

        # check if it is a string and not None to avoid AttributeError
        try:
            self._url_path = url_path.rstrip("/").strip()
        except Exception as exc:
            raise RuntimeError(f"Invalid type for api_endpoint {self._url_path} for a paginator.") from exc

        self._query = query

    @beartype
    def _fetch_next_page(self) -> None:
        """
        1. builds the URL from the query and page number
        1. makes the request to the API
        1. API responds with a JSON that has data or JSON that has data and result
            1. parses the response
            2. creates cript.Nodes from the response
            3. Add the nodes to the fetched_data so the iterator can return them

        Raises
        ------
        InvalidSearchRequest
            In case the API responds with an error
        StopIteration
            In case there are no further results to fetch


        Returns
        -------
             None
        """

        # Composition of the query URL
        temp_url_path: str = self._url_path + "/"

        query_list = []

        if len(self._query) > 0:
            query_list += [f"q={self._query}"]

        if self._limit_node_fetches is None or self._limit_node_fetches > 1:  # This limits these parameters
            if self._start_after_uuid is not None:
                query_list += [f"after={self._start_after_uuid}"]
                if self._start_after_score is not None:  # Always None for none BigSMILES searches
                    query_list += [f"score={self._start_after_score}"]

                # Reset to allow normal search to continue
                self._start_after_uuid = None
                self._start_after_score = None

            elif len(self._fetched_nodes) > 0:  # Use known last element
                node_uuid, node_score = _get_uuid_score_from_json(self._fetched_nodes[-1])
                query_list += [f"after={node_uuid}"]
                if node_score is not None:
                    query_list += [f"score={node_score}"]

        for i, query in enumerate(query_list):
            if i == 0:
                temp_url_path += "?"
            else:
                temp_url_path += "&"
            temp_url_path += quote(query, safe="/=&?")

        response: requests.Response = self._api._capsule_request(url_path=temp_url_path, method="GET")

        # it is expected that the response will be JSON
        # try to convert response to JSON
        try:
            api_response: Dict = response.json()

        # if converting API response to JSON gives an error
        # then there must have been an API error, so raise the requests error
        # this is to avoid bad indirect errors and make the errors more direct for users
        except json.JSONDecodeError as json_exc:
            try:
                response.raise_for_status()
            except Exception as exc:
                raise exc from json_exc

        # handling both cases in case there is result inside of data or just data
        try:
            current_page_results = api_response["data"]["result"]
        except KeyError:
            current_page_results = api_response["data"]
        except TypeError:
            current_page_results = api_response["data"]

        if api_response["code"] == 404 and api_response["error"] == "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.":
            current_page_results = []
            self._api.logger.debug(f"The paginator hit a 404 HTTP for requesting this {temp_url_path} with GET. We interpret it as no nodes present, but this is brittle at the moment.")
        # if API response is not 200 raise error for the user to debug
        elif api_response["code"] != 200:
            raise APIError(api_error=str(response.json()), http_method="GET", api_url=temp_url_path)

        # Here we only load the JSON into the temporary results.
        # This delays error checking, and allows users to disable auto node conversion
        json_list = current_page_results
        self._fetched_nodes += json_list

    def __next__(self):
        if self._limit_node_fetches and self._current_position >= self._limit_node_fetches:
            raise StopIteration

        if self._current_position >= len(self._fetched_nodes):
            self._fetch_next_page()

        try:
            next_node_json = self._fetched_nodes[self._current_position - 1]
        except IndexError as exc:  # This is not a random access iteration.
            # So if fetching a next page wasn't enough to get the index inbound,
            # The iteration stops
            raise StopIteration from exc

        if self.auto_load_nodes:
            return_data = load_nodes_from_json(next_node_json)
        else:
            return_data = next_node_json

        # Advance position last, so if an exception occurs, for example when
        # node decoding fails, we do not advance, and users can try again without decoding
        self._current_position += 1

        return return_data

    def __iter__(self):
        self._current_position = 0
        return self

    @beartype
    def limit_node_fetches(self, max_num_nodes: Optional[int]) -> None:
        """Limit pagination to a maximum number of pages.

        This can be used for very large searches with the paginator, so the search can be split into
        smaller portions.

        Parameters
        ----------
        max_num_nodes: Optional[int],
          positive integer with maximum number of page fetches.
          or None, indicating unlimited number of page fetches are permitted.
        """
        self._limit_node_fetches = max_num_nodes

    @beartype
    def start_after_uuid(self, start_after_uuid: str, start_after_score: Optional[float] = None):
        """
        This can be used to continue a search from a last known node.

        Parameters
        ----------
        start_after_uuid: str
            UUID string of the last node from a previous search
        start_after_score: float
            required for BigSMILES searches, the last score from a BigSMILES search.
            Must be None if not a BigSMILES search.

        Returns
        -------
        None
        """
        self._start_after_uuid = start_after_uuid
        self._start_after_score = start_after_score

    @beartype
    def get_bigsmiles_search_score(self, uuid: str):
        """
        Get the ranking score for nodes from the BigSMILES search.
        Will return None if not a BigSMILES search or raise an Exception.
        """
        if uuid not in self._uuid_search_score_map.keys():
            start = len(self._uuid_search_score_map.keys())
            for node_json in self._fetched_nodes[start:]:
                node_uuid, node_score = _get_uuid_score_from_json(node_json)
                self._uuid_search_score_map[node_uuid] = node_score
        try:
            return self._uuid_search_score_map[uuid]
        except KeyError as exc:
            raise RuntimeError(f"The requested UUID {uuid} is not know from the search. Search scores are limited only to current search.") from exc
