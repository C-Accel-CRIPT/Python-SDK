from typing import Any, List

from cript.api.valid_search_modes import SearchModes
from cript.exceptions import CRIPTException


class CRIPTConnectionError(CRIPTException):
    """
    Raised when the API object cannot connect to CRIPT with the given host and token
    """

    def __init__(self, host, token):
        self.host = host
        # Do not store full token in stack trace for security reasons
        uncovered_chars = len(token) // 4
        self.token = token[:uncovered_chars]
        self.token += "*" * (len(token) - 2 * uncovered_chars)
        self.token += token[-uncovered_chars:]

    def __str__(self) -> str:
        """

        Returns
        -------
        str
            Explanation of the error
        """

        ret_str = f"Could not connect to CRIPT with the given host ({self.host}) and token ({self.token})."
        ret_str += " Please be sure both host and token are entered correctly."
        return ret_str


class InvalidVocabulary(CRIPTException):
    """
    Raised when the CRIPT controlled vocabulary is invalid
    """

    vocab: str = ""
    possible_vocab: List[str] = []

    def __init__(self, vocab: str, possible_vocab: List[str]):
        self.vocab = vocab
        self.possible_vocab = possible_vocab

    def __str__(self) -> str:
        ret_str = f"The vocabulary '{self.vocab}' entered does not exist within the CRIPT controlled vocabulary."
        ret_str += f" Please pick a valid CRIPT vocabulary from {self.possible_vocab}"
        return ret_str


class InvalidVocabularyCategory(CRIPTException):
    """
    Raised when the CRIPT controlled vocabulary category is unknown
    and gives the user a list of all valid vocabulary categories
    """

    def __init__(self, vocab_category: str, valid_vocab_category: List[str]):
        self.vocab_category = vocab_category
        self.valid_vocab_category = valid_vocab_category

    def __str__(self) -> str:
        ret_str = f"The vocabulary category '{self.vocab_category}' does not exist within the CRIPT controlled vocabulary."
        ret_str += f" Please pick a valid CRIPT vocabulary category from {self.valid_vocab_category}."
        return ret_str


class CRIPTAPIAccessError(CRIPTException):
    """
    Exception to be raised when the cached API object is requested, but no cached API exists yet.
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        ret_str = "An operation you requested (see stack trace) requires that you "
        ret_str += " connect to a CRIPT host via an cript.API object first.\n"
        ret_str += "This is common for node creation, validation and modification.\n"
        ret_str += "It is necessary that you connect with the API via a context manager like this:\n"
        ret_str += "`with cript.API('https://criptapp.org/', secret_token) as api:\n"
        ret_str += "\t# code that use the API object explicitly (`api.save(..)`) or implicitly (`cript.Experiment(...)`)."
        ret_str += "See documentation of cript.API for more details."
        return ret_str


class CRIPTAPISaveError(CRIPTException):
    """
    CRIPTAPISaveError is raised when the API responds with a status that is not 200
    The API response along with status code is shown to the user

    Parameters
    ----------
    api_host_domain: str
        cript API host domain such as "https://criptapp.org"
    api_response: str
        message that the API returned

    Returns
    -------
    Error Message: str
        Error message telling the user what was the issue and giving them helpful clues as how to fix the error
    """

    api_host_domain: str
    http_code: str
    api_response: str

    def __init__(self, api_host_domain: str, http_code: str, api_response: str):
        self.api_host_domain = api_host_domain
        self.http_code = http_code
        self.api_response = api_response

    def __str__(self) -> str:
        error_message = f"API responded with 'http:{self.http_code} {self.api_response}'"

        return error_message


class InvalidSearchModeError(CRIPTException):
    """
    Exception for when the user tries to search the API with an invalid search mode that is not supported
    """

    invalid_search_mode: str = ""

    def __init__(self, invalid_search_mode: Any):
        self.invalid_search_mode = invalid_search_mode

    # TODO this method is not being used currently, if it never gets used, remove it
    def _get_valid_search_modes(self) -> List[str]:
        """
        gets the valid search modes available in the CRIPT API

        This method can be easily converted to a function if needed

        Returns
        -------
        list of valid search modes: List[str]
        """

        # list of valid search mode values "", "uuid", "contains_name", etc.
        # return [mode.value for mode in SearchModes]

        # outputs: ['NODE_TYPE', 'UUID', 'CONTAINS_NAME', 'EXACT_NAME', 'UUID_CHILDREN']
        return list(SearchModes.__members__.keys())

    def __str__(self) -> str:
        """
        tells the user the search mode they picked for the api client to get a node from the API is invalid
        and lists all the valid search modes they can pick from

        Returns
        -------
        error message: str
        """

        # TODO This error message needs more documentation because it is not as intuitive
        error_message = f"'{self.invalid_search_mode}' is an invalid search mode. " f"The valid search modes come from cript.api.SearchModes"

        return error_message


class InvalidHostError(CRIPTException):
    """
    Exception is raised when the host given to the API is invalid

    Error message is given to it to be displayed to the user
    """

    error_message: str

    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        """
        tells the user the search mode they picked for the api client to get a node from the API is invalid
        and lists all the valid search modes they can pick from

        Returns
        -------
        error message: str
        """

        return self.error_message


class APIError(CRIPTException):
    """
    Generic error made to display API errors to the user
    """

    api_error: str = ""

    def __init__(self, api_error: str) -> None:
        """
        create an APIError
        Parameters
        ----------
        api_error: str
            JSON string of API error

        Returns
        -------
        None
            create an API Error
        """
        self.api_error = api_error

    def __str__(self):
        error_message: str = f"The API responded with {self.api_error}"

        return error_message


class FileDownloadError(CRIPTException):
    """
    This error is raised when the API wants to download a file from an AWS S3 URL
    but the status is something other than 200
    """

    error_message: str = ""

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message

    def __str__(self) -> str:
        return self.error_message
