import json
from typing import List, Set

from beartype import beartype

from cript.exceptions import CRIPTException


class CRIPTConnectionError(CRIPTException):
    """
    ## Definition
    Raised when the cript.API object cannot connect to CRIPT with the given host and token

    ## Troubleshooting
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
    Also make sure to use it in a context manager `with cript.API as api:` or  manually call
    `connect` and `disconnect`.

    The CRIPT Python SDK relies on a cript.API object for creation, validation, and modification of nodes.
    The cript.API object may be explicitly called by the user to perform operations to the API, or
    implicitly called by the Python SDK under the hood to perform some sort of validation.

    ## Troubleshooting
    To fix this error please instantiate an api object

    ```python
    import cript

    my_host = "https://api.criptapp.org/"
    my_token = "123456" # To use your token securely, please consider using environment variables

    my_api = cript.API(host=my_host, token=my_token)
    my_api.connect()
    # Your code
    my_api.disconnect()
    ```
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        error_message = (
            "cript.API object is required for an operation, but it does not exist."
            "Please instantiate a cript.API object and connect it to API for example with a context manager `with cript.API() as api:` to continue."
            "See the documentation for more details."
        )

        return error_message


class CRIPTAPISaveError(CRIPTException):
    """
    ## Definition
    CRIPTAPISaveError is raised when the API responds with a http status code that is anything other than 200.
    The status code and API response is shown to the user to help them debug the issue.

    ## Troubleshooting
    This error is more of a case by case basis, but the best way to approach it to understand that the
    CRIPT Python SDK sent an HTTP POST request with a giant JSON in the request body
    to the CRIPT API. The API then read that request, and it responded with some sort of error either
    to the that JSON or how the request was sent.
    """

    api_host_domain: str
    http_code: str
    api_response: str

    def __init__(self, api_host_domain: str, http_code: str, api_response: str, patch_request: bool, pre_saved_nodes: Set[str], json_data: str):
        self.api_host_domain = api_host_domain
        self.http_code = http_code
        self.api_response = api_response
        self.patch_request = patch_request
        self.pre_saved_nodes = pre_saved_nodes
        self.json_data = json_data

    def __str__(self) -> str:
        type = "POST"
        if self.patch_request:
            type = "PATCH"
        error_message = f"API responded to {type} with 'http:{self.http_code} {self.api_response}'"
        if self.json_data:
            error_message += f" data: {self.json_data}"

        return error_message


class CRIPTDuplicateNameError(CRIPTAPISaveError):
    """
    Exception raised when attempting to save a node with a name that already exists in CRIPT.

    This exception class extends `CRIPTAPISaveError` and is used to handle errors
    that occur when a node's name duplicates an existing node's name in the CRIPT database.

    Parameters
    ----------
    api_response : dict
        The response returned from the API that contains the error details.
    json_data : str
        The JSON data of the node that caused the duplication error.
    parent_cript_save_error : CRIPTAPISaveError
        The original `CRIPTAPISaveError` instance containing additional context of the error.

    ## Troubleshooting
    #### Duplicate Name Errors
    Make sure that the name you are using to save a node is unique and does not already exist in the database.
    If you encounter a `CRIPTDuplicateNameError`, check the name of your node and try a different name.
    """

    def __init__(self, api_response, json_data: str, parent_cript_save_error: CRIPTAPISaveError):
        super().__init__(
            parent_cript_save_error.api_host_domain, api_response["code"], api_response=api_response["error"], patch_request=parent_cript_save_error.patch_request, pre_saved_nodes=parent_cript_save_error.pre_saved_nodes, json_data=json_data
        )

        # We don't care if the data is invalid JSON
        # So let's catch a couple of common exceptions and ensure still meaning error messages
        # (and debug info in case it does happen.)
        try:
            json_dict = json.loads(self.json_data)
        except (TypeError, json.JSONDecodeError):
            self.name = "unknown_name"
            self.node = "UnknownType"
        try:
            self.name = json_dict["name"]
        except KeyError:
            self.name = "unknown_name_key"
        try:
            self.node = json_dict["node"][0]
        except KeyError:
            self.node = "UnknownTypeKey"
        except IndexError:
            self.node = "UnknownTypeIdx"

    def __str__(self) -> str:
        return f"The name '{self.name}' for your {self.node} node is already present in CRIPT. Please use a unique name"


class InvalidHostError(CRIPTException):
    """
    ## Definition
    Exception is raised when the host given to the API is invalid

    ## Troubleshooting
    This is a simple error to fix, simply put `http://` or preferably `https://` in front of your domain
    when passing in the host to the cript.API class such as `https://api.criptapp.org/`

    Currently, the only web protocol that is supported with the CRIPT Python SDK is `HTTP`.

    ### Example
    ```python
    import cript

    my_valid_host = "https://api.criptapp.org/"
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

    ## Troubleshooting
    Please keep in mind that the CRIPT Python SDK turns the [Project](../../nodes/primary_nodes/project)
    node into a giant JSON and sends that to the API to be processed. If there are any errors while processing
    the giant JSON generated by the CRIPT Python SDK, then the API will return an error about the http request
    and the JSON sent to it.

    The best way to trouble shoot this is to figure out what the API error means and figure out where
    in the Python SDK this error occurred and what could be the reason under the hood.

    ### Steps to try:
    1. What does the API error mean?
        1. Is the error something you can easily fix by maybe renaming a node?
        1. Does the `http_method` look reasonable?
        1. Does the `URL` that the data was sent to look reasonable?
    1. Is there a problem within the JSON?
    1. Is the problem within how the SDK is converting nodes from and to JSON (serialization and deserialization)?
    """

    api_error: str = ""

    # having the URL that the API gave an error for helps in debugging
    api_url: str = ""
    http_method: str = ""

    @beartype
    def __init__(self, api_error: str, http_method: str, api_url: str) -> None:
        self.api_error = api_error

        self.api_url = api_url

        # TODO consider having an enum for all the HTTP methods so they are easily entered and disallows anything
        #   that would be not make sense
        self.http_method = http_method

    def __str__(self) -> str:
        return f"CRIPT Python SDK sent HTTP `{self.http_method.upper()}` request to URL: `{self.api_url}` and API responded with {self.api_error}"


class FileDownloadError(CRIPTException):
    """
    ## Definition
    This error is raised when the API wants to download a file from an AWS S3 URL
    via the `cript.API.download_file()` method, but the status is something other than 200.
    """

    error_message: str = ""

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message

    def __str__(self) -> str:
        return self.error_message
