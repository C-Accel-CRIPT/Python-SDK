import json
from typing import Dict, Union
from urllib.parse import quote

import requests
from beartype import beartype

from cript.api.exceptions import APIError
from cript.nodes.util import load_nodes_from_json


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
    _initial_page_number: Union[int, None]
    _current_position: int
    _fetched_nodes: list
    _number_fetched_pages: int = 0
    _limit_page_fetches: Union[int, None] = None
    _num_skip_pages: int = 0
    auto_load_nodes: bool = True

    @beartype
    def __init__(
        self,
        api,
        url_path: str,
        page_number: Union[int, None],
        query: str,
    ):
        """
        create a paginator

        1. set all the variables coming into constructor
        1. then prepare any variable as needed e.g. strip extra spaces or url encode query

        Parameters
        ----------
        http_headers: dict
            get already created http headers from API and just use them in paginator
        api_endpoint: str
            api endpoint to send the search requests to
            it already contains what node the user is looking for
        current_page_number: int
            page number to start from. Keep track of current page for user to flip back and forth between pages of data
        query: str
            the value the user is searching for

        Returns
        -------
        None
            instantiate a paginator
        """
        self._api = api
        self._initial_page_number = page_number
        self._number_fetched_pages = 0
        self._fetched_nodes = []
        self._current_position = 0

        # check if it is a string and not None to avoid AttributeError
        try:
            self._url_path = quote(url_path.rstrip("/").strip())
        except Exception as exc:
            raise RuntimeError(f"Invalid type for api_endpoint {self._url_path} for a paginator.") from exc

        self._query = quote(query)

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

        # Check if we are supposed to fetch more pages
        if self._limit_page_fetches and self._number_fetched_pages >= self._limit_page_fetches:
            raise StopIteration

        # Composition of the query URL
        temp_url_path: str = self._url_path
        temp_url_path += f"/?q={self._query}"
        if self._initial_page_number is not None:
            temp_url_path += f"&page={self.page_number}"
        self._number_fetched_pages += 1

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
        if self._current_position >= len(self._fetched_nodes):
            # Without a page number argument, we can only fetch once.
            if self._initial_page_number is None and self._number_fetched_pages > 0:
                raise StopIteration
            self._fetch_next_page()

        try:
            next_node_json = self._fetched_nodes[self._current_position - 1]
        except IndexError:  # This is not a random access iteration.
            # So if fetching a next page wasn't enough to get the index inbound,
            # The iteration stops
            raise StopIteration

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

    @property
    def page_number(self) -> Union[int, None]:
        """Obtain the current page number the paginator is fetching next.

        Returns
        -------
        int
          positive number of the next page this paginator is fetching.
        None
          if no page number is associated with the pagination
        """
        page_number = self._num_skip_pages + self._number_fetched_pages
        if self._initial_page_number is not None:
            page_number += self._initial_page_number
        return page_number

    @beartype
    def limit_page_fetches(self, max_num_pages: Union[int, None]) -> None:
        """Limit pagination to a maximum number of pages.

        This can be used for very large searches with the paginator, so the search can be split into
        smaller portions.

        Parameters
        ----------
        max_num_pages: Union[int, None],
          positive integer with maximum number of page fetches.
          or None, indicating unlimited number of page fetches are permitted.
        """
        self._limit_page_fetches = max_num_pages

    def skip_pages(self, skip_pages: int) -> int:
        """Skip pages in the pagination.

        Warning this function is advanced usage and may not produce the results you expect.
        In particular, every search is different, even if we search for the same values there is
        no guarantee that the results are in the same order. (And results can change if data is
        added or removed from CRIPT.) So if you break up your search with `limit_page_fetches` and
        `skip_pages` there is no guarantee that it is the same as one continuous search.
        If the paginator associated search does not accept pages, there is no effect.

        Parameters
        ----------
        skip_pages:int
          Number of pages that the paginator skips now before fetching the next page.
          The parameter is added to the internal state, so repeated calls skip more pages.

        Returns
        -------
        int
          The number this paginator is skipping. Internal skip count.

        Raises
        ------
        RuntimeError
          If the total number of skipped pages is negative.
        """
        num_skip_pages = self._num_skip_pages + skip_pages
        if self._num_skip_pages < 0:
            RuntimeError(f"Invalid number of skipped pages. The total number of pages skipped is negative {num_skip_pages}, requested to skip {skip_pages}.")
        self._num_skip_pages = num_skip_pages
        return self._num_skip_pages
