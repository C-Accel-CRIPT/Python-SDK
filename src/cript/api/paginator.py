from typing import Any, List


class Paginator:
    """
    Paginator to flip through different pages of data that the API returns
    """

    query: str = ""
    current_page_number: int = None
    page_of_data: List[Any] = None

    def __init__(self, query: str, current_page_number: int):
        self.query = query
        self.current_page_number = current_page_number
        return

    def next(self):
        """
        flip to the next page of data.
        This works by adding one to the current page number to get the next page number.
        Then call set_page() method with the next page number
        """
        pass

    def previous(self):
        """
        flip to the next page of data.
        This works by subtracting one to the current page number to get the previous page number.
        Then call set_page() method with the previous page number
        """
        pass

    def set_page(self, new_page_number: int):
        """
        flips to a specific page of data that has been requested

        Args:
            new_page_number (int): specific page of data that the user wants to go to

        Example:
            requests.get("criptapp.org/api?page=2)
            requests.get(f"{self.query}?page={self.current_page_number - 1}")

        Raises:
            InvalidPageRequest, in case the user tries to get a negative page or a page that doesn't exist
        """
        pass
