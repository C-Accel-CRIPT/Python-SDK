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

    def __init__(self, vocab: str, possible_vocab: List[str]) -> None:
        """
        create an InvalidVocabularyError

        Parameters
        ----------
        vocab: str
        possible_vocab: List[str]
        """
        self.vocab = vocab
        self.possible_vocab = possible_vocab

    def __str__(self) -> str:
        """
        show user the error message

        Returns
        -------
        error_message: str
        """
        error_message = (
            f"The vocabulary '{self.vocab}' entered does not exist within the CRIPT controlled vocabulary." 
            f" Please pick a valid CRIPT vocabulary from {self.possible_vocab}"
        )
        return error_message


class InvalidVocabularyCategory(CRIPTException):
    """
    Raised when the CRIPT controlled vocabulary category is unknown
    and gives the user a list of all valid vocabulary categories
    """

    def __init__(self, vocab_category: str, valid_vocab_category: List[str]):
        self.vocab_category = vocab_category
        self.valid_vocab_category = valid_vocab_category

    def __str__(self) -> str:
        """
        Returns an error message for the user.

        Returns
        -------
        error_message:str
            error message for the user
        """
        error_message = (
            f"The vocabulary category {self.vocab_category} does not exist within the CRIPT controlled vocabulary. "
            f"Please pick a valid CRIPT vocabulary category from {self.valid_vocab_category}."
        )

        return error_message


class CRIPTAPIRequiredError(CRIPTException):
    """
    Exception to be raised when the cached API object is requested, but no cached API exists yet.

    The CRIPT Python SDK relies on a cript.API object for creation, validation, and modification of nodes.
    The cript.API object may be explicitly called by the user to perform operations to the API, or
    implicitly called by the Python SDK under the hood to perform some sort of validation.

    To fix the error please instantiate an api object

    ```python
    import cript

    my_host = "https://criptapp.org"
    my_token = "123456" # To use your token securely, please consider using environment variables

    my_api = cript.API(host=my_host, token=my_token)
    ```
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        return "cript.API object is required for an operation, but it does not exist." "Please instantiate a cript.API object to continue." "See the documentation for more details."


class CRIPTAPISaveError(CRIPTException):
    """
    CRIPTAPISaveError is raised when the API responds with a http status code that is anything other than 200.
    The status code and API response is shown to the user to help them debug the issue.

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

    def __init__(self, error_message: str) -> None:
        pass

    def __str__(self) -> str:
        """
        tells the user the search mode they picked for the api client to get a node from the API is invalid
        and lists all the valid search modes they can pick from

        Returns
        -------
        error message: str
        """

        return "The host must start with http or https"


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
