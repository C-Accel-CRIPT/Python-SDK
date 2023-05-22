from typing import List

from cript.exceptions import CRIPTException


class CRIPTConnectionError(CRIPTException):
    """
    ## Definition
    Raised when the cript.API object cannot connect to CRIPT with the given host and token

    ## How to Fix
    The best way to fix this error is to check that your host and token are written and used correctly within
    the cript.API object. This error could also be shown if the API is unresponsive and the cript.API object
    just cannot successfully connect to it.
    """

    def __init__(self, host, token):
        self.host = host
        # Do not store full token in stack trace for security reasons
        uncovered_chars = len(token) // 4
        self.token = token[:uncovered_chars]
        self.token += "*" * (len(token) - 2 * uncovered_chars)
        self.token += token[-uncovered_chars:]

    def __str__(self) -> str:
        error_message = f"Could not connect to CRIPT with the given host ({self.host}) and token ({self.token}). " f"Please be sure both host and token are entered correctly."

        return error_message


# TODO refactor
class InvalidVocabulary(CRIPTException):
    """
    Raised when the CRIPT controlled vocabulary is invalid
    """

    vocab: str = ""
    possible_vocab: List[str] = []

    def __init__(self, vocab: str, possible_vocab: List[str]) -> None:
        self.vocab = vocab
        self.possible_vocab = possible_vocab

    def __str__(self) -> str:
        error_message = f"The vocabulary '{self.vocab}' entered does not exist within the CRIPT controlled vocabulary." f" Please pick a valid CRIPT vocabulary from {self.possible_vocab}"
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
        error_message = f"The vocabulary category {self.vocab_category} does not exist within the CRIPT controlled vocabulary. " f"Please pick a valid CRIPT vocabulary category from {self.valid_vocab_category}."

        return error_message


class CRIPTAPIRequiredError(CRIPTException):
    """
    ## Definition
    Exception to be raised when the API object is requested, but no cript.API object exists yet.

    The CRIPT Python SDK relies on a cript.API object for creation, validation, and modification of nodes.
    The cript.API object may be explicitly called by the user to perform operations to the API, or
    implicitly called by the Python SDK under the hood to perform some sort of validation.

    ## How to Fix
    To fix this error please instantiate an api object

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
        error_message = "cript.API object is required for an operation, but it does not exist." "Please instantiate a cript.API object to continue." "See the documentation for more details."

        return error_message


class CRIPTAPISaveError(CRIPTException):
    """
    ## Definition
    CRIPTAPISaveError is raised when the API responds with a http status code that is anything other than 200.
    The status code and API response is shown to the user to help them debug the issue.

    ## How to Fix
    This error is more of a case by case basis, but the best way to approach it to understand that the
    CRIPT Python SDK sent an HTTP POST request with a giant JSON in the request body
    to the CRIPT API. The API then read that request, and it responded with some sort of error either
    to the that JSON or how the request was sent.
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


class InvalidHostError(CRIPTException):
    """
    ## Definition
    Exception is raised when the host given to the API is invalid

    ## How to Fix
    This is a simple error to fix, simply put `http://` or preferably `https://` in front of your domain
    when passing in the host to the cript.API class such as `https://criptapp.org`

    Currently, the only web protocol that is supported with the CRIPT Python SDK is `HTTP`.

    ### Example
    ```python
    import cript

    my_valid_host = "https://criptapp.org"
    my_token = "123456" # To use your token securely, please consider using environment variables

    my_api = cript.API(host=my_valid_host, token=my_token)
    ```

    Warnings
    --------
    Please consider always using [HTTPS](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS)
    as that is a secure protocol and avoid using `HTTP` as it is insecure.
    The CRIPT Python SDK will give a warning in the terminal when it detects a host with `HTTP`


    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "The host must start with http or https"


class APIError(CRIPTException):
    """
    ## Definition
    This is a generic error made to display API errors to the user to troubleshoot.

    ## How to Fix
    Please keep in mind that the CRIPT Python SDK turns the [Project](../../nodes/primary_nodes/project)
    node into a giant JSON and sends that to the API to be processed. If there are any errors while processing
    the giant JSON generated by the CRIPT Python SDK, then the API will return an error about the http request
    and the JSON sent to it. Therefore, the error shown might be an error within the JSON and not particular
    within the Python code that was created

    The best way to trouble shoot this is to figure out what the API error means and figure out where
    in the Python SDK this error occurred and what have been the reason under the hood.
    """

    api_error: str = ""

    def __init__(self, api_error: str) -> None:
        self.api_error = api_error

    def __str__(self) -> str:
        error_message: str = f"The API responded with {self.api_error}"

        return error_message
