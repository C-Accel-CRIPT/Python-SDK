from typing import List, Union
from urllib.parse import quote

import requests


class Paginator:
    """
    Paginator to flip through different pages of data that the API returns
    """

    _http_headers: dict

    api_endpoint: str

    # if query or page number are None, then it means that api_endpoint does not allow for whatever that is None
    # and that is not added to the URL
    # by default the page_number and query are `None` and they can get filled in
    query: Union[str, None]
    _current_page_number: [int, None]

    current_page_results: List[dict]

    def __init__(
        self,
        http_headers: dict,
        api_endpoint: str,
        current_page_number: [int, None] = None,
        query: [str, None] = None,
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
        This works by adding one to the current page number to get the next page number.
        Then call set_page() method with the next page number
        """
        self.current_page_number += 1

    def previous_page(self):
        """
        flip to the next page of data.
        This works by subtracting one to the current page number to get the previous page number.
        Then call set_page() method with the previous page number
        """
        self.current_page_number -= 1

    @property
    def current_page_number(self) -> int:
        """
        get the current page number for the query.
        The setting the page will take you to that specific page of results

        Returns
        -------
        current page number: int
        """
        return self._current_page_number

    @current_page_number.setter
    def current_page_number(self, new_page_number: int) -> None:
        """
        flips to a specific page of data that has been requested

        sets the current_page_number and then sends the request to the API and gets the results of this page number

        Parameters
        ----------
        new_page_number (int): specific page of data that the user wants to go to

        Examples
        --------
        requests.get("https://criptapp.org/api?page=2)
        requests.get(f"{self.query}?page={self.current_page_number - 1}")

        Raises
        --------
        InvalidPageRequest, in case the user tries to get a negative page or a page that doesn't exist
        """
        if new_page_number < 0:
            error_message: str = (
                f"Paginator current page number is invalid because it is negative: "
                f"{self.current_page_number} please set paginator.current_page_number "
                f"to a positive page number"
            )

            # TODO replace with custom error
            raise Exception(error_message)

        else:
            self._current_page_number = new_page_number
            # when new page number is set, it is then fetched from the API
            self.fetch_page_from_api()

    def fetch_page_from_api(self) -> List[dict]:
        """

        Raises
        ------
        InvalidPageRequest

        Returns
        -------
        current page results: List[dict]
        """

        # temporary variable to not overwrite api_endpoint
        temp_api_endpoint: str = self.api_endpoint

        if self.query is not None:
            temp_api_endpoint += f"/?q={self.query}"

        if self.current_page_number is not None:
            temp_api_endpoint += f"/?page={self.current_page_number}"

        response = requests.get(
            url=temp_api_endpoint,
            headers=self._http_headers,
        ).json()

        self.current_page_results = response["data"]["result"]

        # TODO give error if HTTP response if anything other than 200
        if response["code"] != 200:
            raise Exception(f"API responded with: {response['error']}")

        return self.current_page_results
