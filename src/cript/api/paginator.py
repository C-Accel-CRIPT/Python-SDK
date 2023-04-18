from typing import Any, List

import requests


class Paginator:
    """
    Paginator to flip through different pages of data that the API returns
    """

    api_endpoint: str = ""
    _token: str = ""

    current_page_number: int = None
    current_page_results: List[dict]

    page_of_data: List[Any] = None

    def __init__(
        self,
        api_endpoint: str,
        current_page_number: int,
        _token: str,
    ):
        self.api_endpoint = api_endpoint
        self._token = f"Bearer {_token}"
        self.current_page_number = current_page_number

    def next(self):
        """
        flip to the next page of data.
        This works by adding one to the current page number to get the next page number.
        Then call set_page() method with the next page number
        """
        self.current_page_number += 1

    def previous(self):
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
        return self.current_page_number

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
        self.current_page_number = new_page_number
        self.fetch_page_from_api()

    def fetch_page_from_api(self):
        api_endpoint: str = f"{self.api_endpoint}/?page={self.current_page_number}"

        http_headers = {"Authorization": self._token, "Content-Type": "application/json"}

        response = requests.get(
            url=api_endpoint,
            headers=http_headers,
        ).json()

        self.current_page_results = response["data"]["results"]

        return self.current_page_results
