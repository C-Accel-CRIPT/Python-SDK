from typing import Dict, List, Optional, Union
from urllib.parse import quote

import requests
from beartype import beartype

from cript.api.exceptions import APIError


class Paginator:
    """
    Paginator is used to flip through different pages of data that the API returns when searching.
    > Instead of the user manipulating the URL and parameters, this object handles all of that for them.

    When conducting any kind of search the API returns pages of data and each page contains 10 results.
    This is equivalent to conducting a Google search when Google returns a limited number of links on the first page
    and all other results are on the next pages.

    Using the Paginator object, the user can simply and easily flip through the pages of data the API provides.

    !!! Warning "Do not create paginator objects"
        Please note that you are not required or advised to create a paginator object, and instead the
        Python SDK API object will create a paginator for you, return it, and let you simply use it


    Attributes
    ----------
    current_page_results: List[dict]
        List of JSON dictionary results returned from the API
        ```python
        [{result 1}, {result 2}, {result 3}, ...]
        ```
    """

    _http_headers: dict

    api_endpoint: str

    # if query or page number are None, then it means that api_endpoint does not allow for whatever that is None
    # and that is not added to the URL
    # by default the page_number and query are `None` and they can get filled in
    query: Union[str, None]
    _current_page_number: int

    current_page_results: List[dict]

    @beartype
    def __init__(
        self,
        http_headers: dict,
        api_endpoint: str,
        query: Optional[str] = None,
        current_page_number: int = 0,
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
        self.api_endpoint = api_endpoint
        self.query = query
        self._current_page_number = current_page_number

        # check if it is a string and not None to avoid AttributeError
        if api_endpoint is not None:
            # strip the ending slash "/" to make URL uniform and any trailing spaces from either side
            self.api_endpoint = api_endpoint.rstrip("/").strip()

        # check if it is a string and not None to avoid AttributeError
        if query is not None:
            # URL encode query
            self.query = quote(query)

        self.fetch_page_from_api()

    def next_page(self):
        """
        flip to the next page of data.

        Examples
        --------
        ```python
        my_paginator.next_page()
        ```
        """
        self.current_page_number += 1

    def previous_page(self):
        """
        flip to the next page of data.

        Examples
        --------
        ```python
        my_paginator.previous_page()
        ```
        """
        self.current_page_number -= 1

    @property
    @beartype
    def current_page_number(self) -> int:
        """
        get the current page number that you are on.

        Setting the page will take you to that specific page of results

        Examples
        --------
        ```python
        my_paginator.current_page = 10
        ```

        Returns
        -------
        current page number: int
            the current page number of the data
        """
        return self._current_page_number

    @current_page_number.setter
    @beartype
    def current_page_number(self, new_page_number: int) -> None:
        """
        flips to a specific page of data that has been requested

        sets the current_page_number and then sends the request to the API and gets the results of this page number

        Parameters
        ----------
        new_page_number (int): specific page of data that the user wants to go to

        Examples
        --------
        requests.get("https://api.criptapp.org//api?page=2)
        requests.get(f"{self.query}?page={self.current_page_number - 1}")

        Raises
        --------
        InvalidPageRequest, in case the user tries to get a negative page or a page that doesn't exist
        """
        if new_page_number < 0:
            error_message: str = f"Paginator current page number is invalid because it is negative: " f"{self.current_page_number} please set paginator.current_page_number " f"to a positive page number"

            # TODO replace with custom error
            raise Exception(error_message)

        else:
            self._current_page_number = new_page_number
            # when new page number is set, it is then fetched from the API
            self.fetch_page_from_api()

    @beartype
    def fetch_page_from_api(self) -> List[dict]:
        """
        1. builds the URL from the query and page number
        1. makes the request to the API
        1. API responds with a JSON that has data or JSON that has data and result
            1. parses it and correctly sets the current_page_results property

        Raises
        ------
        InvalidSearchRequest
            In case the API responds with an error

        Returns
        -------
        current page results: List[dict]
            makes a request to the API and gets a page of data
        """

        # temporary variable to not overwrite api_endpoint
        temp_api_endpoint: str = self.api_endpoint

        if self.query is not None:
            temp_api_endpoint = f"{temp_api_endpoint}/?q={self.query}"

        elif self.query is None:
            temp_api_endpoint = f"{temp_api_endpoint}/?q="

        temp_api_endpoint = f"{temp_api_endpoint}&page={self.current_page_number}"

        response: Dict = requests.get(
            url=temp_api_endpoint,
            headers=self._http_headers,
        ).json()

        # handling both cases in case there is result inside of data or just data
        try:
            self.current_page_results = response["data"]["result"]
        except KeyError:
            self.current_page_results = response["data"]
        except TypeError:
            self.current_page_results = response["data"]

        if response["code"] == 404 and response["error"] == "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.":
            self.current_page_results = []
            return self.current_page_results

        # TODO give a CRIPT error if HTTP response is anything other than 200
        if response["code"] != 200:
            raise APIError(api_error=str(response), http_method="GET", api_url=temp_api_endpoint)

        return self.current_page_results
