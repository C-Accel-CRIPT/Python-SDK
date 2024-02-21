from json import JSONDecodeError
from typing import Dict, Optional, Union
from urllib.parse import quote

import requests
from beartype import beartype

from cript.api.api_config import _API_TIMEOUT
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

    _http_headers: dict

    _api_endpoint: str

    # if query or page number are None, then it means that api_endpoint does not allow for whatever that is None
    # and that is not added to the URL
    # by default the page_number and query are `None` and they can get filled in
    _query: Union[str, None]
    _current_page_number: int
    _current_position: int
    _fetched_nodes: list

    @beartype
    def __init__(
        self,
        http_headers: dict,
        api_endpoint: str,
        query: Optional[str] = None,
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
        self._http_headers = http_headers
        self._api_endpoint = None
        self._query = ""
        self._current_page_number = 0
        self._fetched_nodes = []
        self._current_position = 0

        # check if it is a string and not None to avoid AttributeError
        try:
            self._api_endpoint = api_endpoint.rstrip("/").strip()
        except AttributeError as exc:
            if self._api_endpoint is not None:
                raise RuntimeError(f"Invalid type for api_endpoint {self._api_endpoint} for a paginator.") from exc

        # check if it is a string and not None to avoid AttributeError
        try:
            self._query = quote(query)
        except TypeError as exc:
            self._query = ""
            if query is not None:
                raise RuntimeError(f"Invalid type for query {self._query} a paginator.") from exc

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
        temp_api_endpoint: str = self._api_endpoint
        temp_api_endpoint += "/?q="
        if self._query is not None:
            temp_api_endpoint += f"{self._query}"
        temp_api_endpoint += f"&page={self._current_page_number}"

        response: requests.Response = requests.get(url=temp_api_endpoint, headers=self._http_headers, timeout=_API_TIMEOUT)

        # it is expected that the response will be JSON
        # try to convert response to JSON
        try:
            api_response: Dict = response.json()

        # if converting API response to JSON gives an error
        # then there must have been an API error, so raise the requests error
        # this is to avoid bad indirect errors and make the errors more direct for users
        except JSONDecodeError:
            response.raise_for_status()

        # handling both cases in case there is result inside of data or just data
        try:
            current_page_results = api_response["data"]["result"]
        except KeyError:
            current_page_results = api_response["data"]
        except TypeError:
            current_page_results = api_response["data"]

        if api_response["code"] == 404 and api_response["error"] == "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.":
            current_page_results = []
        import json

        # if API response is not 200 raise error for the user to debug
        if api_response["code"] != 200:
            raise APIError(api_error=str(response.json()), http_method="GET", api_url=temp_api_endpoint)
        if len(current_page_results) == 0:
            raise StopIteration

        node_list = load_nodes_from_json(current_page_results)
        self._fetched_nodes += node_list

    def __next__(self):
        if self._current_position >= len(self._fetched_nodes):
            self._fetch_next_page()
        self._current_position += 1
        return self._fetched_nodes[self._current_position - 1]

    def __iter__(self):
        self._current_position = 0
        return self
