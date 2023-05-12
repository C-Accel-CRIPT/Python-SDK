import copy
import json
import os
import pathlib
import uuid
import warnings
from pathlib import Path
from typing import Union

import boto3
import jsonschema
import requests

from cript.api.exceptions import (
    APIError,
    CRIPTAPIAccessError,
    CRIPTAPISaveError,
    CRIPTConnectionError,
    InvalidHostError,
    InvalidVocabulary,
    InvalidVocabularyCategory,
    FileDownloadError,
)
from cript.api.paginator import Paginator
from cript.api.valid_search_modes import SearchModes
from cript.api.vocabulary_categories import all_controlled_vocab_categories
from cript.nodes.core import BaseNode
from cript.nodes.exceptions import CRIPTJsonNodeError, CRIPTNodeSchemaError
from cript.nodes.primary_nodes.project import Project

# Do not use this directly! That includes devs.
# Use the `_get_global_cached_api for access.
_global_cached_api = None


def _get_global_cached_api():
    """
    Read-Only access to the globally cached API object.
    Raises an exception if no global API object is cached yet.
    """
    if _global_cached_api is None:
        raise CRIPTAPIAccessError
    return _global_cached_api


class API:
    """
    ## Definition
    API Client class to communicate with the CRIPT API
    """

    _host: str = ""
    _token: str = ""
    _http_headers: dict = {}
    _vocabulary: dict = {}
    _db_schema: dict = {}
    _api_handle: str = "api"
    _api_version: str = "v1"

    # AWS S3 constants
    _REGION_NAME: str = "us-east-1"
    _IDENTITY_POOL_ID: str = "us-east-1:555e15fe-05c1-4f63-9f58-c84d8fd6dc99"
    _COGNITO_LOGIN_PROVIDER: str = "cognito-idp.us-east-1.amazonaws.com/us-east-1_VinmyZ0zW"
    _BUCKET_NAME: str = "cript-development-user-data"
    _BUCKET_DIRECTORY_NAME: str = "tests"
    _s3_client: boto3.client = None

    def __init__(self, host: Union[str, None], token: [str, None]):
        """
        Initialize object with host and token.
        It is necessary to use a `with` context manager for the API

        Examples
        --------
        ```Python
        with cript.API('https://criptapp.org', 'secret_token') as api:
           # node creation, api.save(), etc.
        ```

        Notes
        -----

        Parameters
        ----------
        host : str, None
            CRIPT host for the Python SDK to connect to such as `https://criptapp.org`
            This host address is the same address used to login to cript website.
            If `None` is specified, the host is inferred from the environment variable `CRIPT_HOST`.
        token : str, None
            CRIPT API Token used to connect to CRIPT
            You can find your personal token on the cript website at User > Security Settings.
            The user icon is in the top right.
            If `None` is specified, the token is inferred from the environment variable `CRIPT_TOKEN`.


        Notes
        -----
        * if `host=None` and `token=None`
            then the Python SDK will grab the host from the users environment variable of `"CRIPT_HOST"`
            and `"CRIPT_TOKEN"`

        Warns
        -----
        UserWarning
            If `host` is using "http" it gives the user a warning that HTTP is insecure and the user shuold use HTTPS

        Raises
        ------
        CRIPTConnectionError
            If it cannot connect to CRIPT with the provided host and token a CRIPTConnectionError is thrown.

        Returns
        -------
        None
            Instantiate a new CRIPT API object
        """

        # if host and token is none then it will grab host and token from user's environment variables
        if host is None:
            host = os.environ.get("CRIPT_HOST")
            if host is None:
                raise RuntimeError("API initilized with `host=None` but environment variable `CRIPT_HOST` not found.\n" "Set the environment variable (preferred) or specify the host explictly at the creation of API.")
        if token is None:
            token = os.environ.get("CRIPT_TOKEN")
            if token is None:
                raise RuntimeError("API initilized with `token=None` but environment variable `CRIPT_TOKEN` not found.\n" "Set the environment variable (preferred) or specify the token explictly at the creation of API.")

        self._host = self._prepare_host(host=host)
        self._token = token

        # assign headers
        # TODO might need to add Bearer to it or check for it
        self._http_headers = {"Authorization": f"{self._token}", "Content-Type": "application/json"}

        self._s3_client = self._create_s3_client()

        # check that api can connect to CRIPT with host and token
        self._check_initial_host_connection()

        self._get_db_schema()

    def _prepare_host(self, host: str) -> str:
        # strip ending slash to make host always uniform
        host = host.rstrip("/")
        host = f"{host}/{self._api_handle}/{self._api_version}"

        # if host is using unsafe "http://" then give a warning
        if host.startswith("http://"):
            warnings.warn("HTTP is an unsafe protocol please consider using HTTPS.")

        if not host.startswith("http"):
            raise InvalidHostError("The host must start with http or https")

        return host

    def _create_s3_client(self) -> boto3.client:
        """

        Returns
        -------
        """
        auth = boto3.client("cognito-identity", region_name=self._REGION_NAME)

        identity_id = auth.get_id(IdentityPoolId=self._IDENTITY_POOL_ID, Logins={self._COGNITO_LOGIN_PROVIDER: self._token})

        aws_credentials = auth.get_credentials_for_identity(IdentityId=identity_id["IdentityId"], Logins={self._COGNITO_LOGIN_PROVIDER: self._token})

        aws_credentials = aws_credentials["Credentials"]

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_credentials["AccessKeyId"],
            aws_secret_access_key=aws_credentials["SecretKey"],
            aws_session_token=aws_credentials["SessionToken"],
        )

        return s3_client

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def connect(self):
        """
        Connect this API globally as the current active access point.
        It is not necessary to call this function manually if a context manager is used.
        A context manager is preferred where possible.
        Jupyter notebooks are a use case where this connection can be handled manually.
        If this function is called manually, the `API.disconnect` function has to be called later.

        For manual connection: nested API object are discouraged.
        """
        # Store the last active global API (might be None)
        global _global_cached_api
        self._previous_global_cached_api = copy.copy(_global_cached_api)
        _global_cached_api = self
        return self

    def disconnect(self):
        """
        Disconnect this API from the active access point.
        It is not necessary to call this function manually if a context manager is used.
        A context manager is preferred where possible.
        Jupyter notebooks are a use case where this connection can be handled manually.
        This function has to be called manually if  the `API.connect` function has to be called before.

        For manual connection: nested API object are discouraged.
        """
        # Restore the previously active global API (might be None)
        global _global_cached_api
        _global_cached_api = self._previous_global_cached_api

    @property
    def schema(self):
        """
        Access the CRIPT Database Schema that is associated with this API connection.
        The CRIPT Database Schema is used  to validate a node's JSON so that it is compatible with the CRIPT API.
        """
        return self._db_schema

    @property
    def host(self):
        """
        Read only access to the currently connected host.

        Examples
        --------
        ```python
        print(cript_api.host)
        ```
        Output
        ```Python
        https://criptapp.org/api/v1
        ```
        """
        return self._host

    def _check_initial_host_connection(self) -> None:
        """
        tries to create a connection with host and if the host does not respond or is invalid it raises an error

        Raises
        -------
        CRIPTConnectionError
            raised when the host does not give the expected response

        Returns
        -------
        None
        """
        try:
            pass
        except Exception as exc:
            raise CRIPTConnectionError(self.host, self._token) from exc

    # TODO this needs a better name because the current name is unintuitive if you are just getting vocab
    def _get_vocab(self) -> dict:
        """
        gets the entire controlled vocabulary to be used with validating nodes
        with attributes from controlled vocabulary
        1. checks global variable to see if it is already set
            if it is already set then it just returns that
        2. if global variable is empty, then it makes a request to the API
           and gets the entire controlled vocabulary
           and then sets the global variable to it

           Examples
           --------
           The vocabulary looks like this
           ```json
           {'algorithm_key':
                [
                    {
                    'description': "Velocity-Verlet integration algorithm. Parameters: 'integration_timestep'.",
                    'name': 'velocity_verlet'
                    },
            }
           ```
        """

        # check cache if vocabulary dict is already populated
        # TODO needs to be changed to MappingTypeProxy
        if bool(self._vocabulary):
            return self._vocabulary

        # TODO this needs to be converted to a dict of dicts instead of dict of lists
        #  because it would be faster to find needed vocab word within the vocab category
        # loop through all vocabulary categories and make a request to each vocabulary category
        # and put them all inside of self._vocab with the keys being the vocab category name
        for category in all_controlled_vocab_categories:
            response = requests.get(f"{self.host}/cv/{category}").json()["data"]
            self._vocabulary[category] = response

        return self._vocabulary

    def _is_vocab_valid(self, vocab_category: str, vocab_word: str) -> Union[bool, InvalidVocabulary, InvalidVocabularyCategory]:
        """
        checks if the vocabulary is valid within the CRIPT controlled vocabulary.
        Either returns True or InvalidVocabulary Exception

        1. if the vocabulary is custom (starts with "+")
            then it is automatically valid
        2. if vocabulary is not custom, then it is checked against its category
            if the word cannot be found in the category then it returns False

        Parameters
        ----------
        vocab_category: str
            the category the vocabulary is in e.g. "Material keyword", "Data type", "Equipment key"
        vocab_word: str
            the vocabulary word e.g. "CAS", "SMILES", "BigSmiles", "+my_custom_key"

        Returns
        -------
        a boolean of if the vocabulary is valid or not

        Raises
        ------
        InvalidVocabulary
            If the vocabulary is invalid then the error gets raised
        """

        # check if vocab is custom
        # This is deactivated currently, no custom vocab allowed.
        if vocab_word.startswith("+"):
            return True

        # TODO do we need to raise an InvalidVocabularyCategory here, or can we just give a KeyError?
        try:
            # get the entire vocabulary
            controlled_vocabulary = self._get_vocab()
            # get just the category needed
            controlled_vocabulary = controlled_vocabulary[vocab_category]
        except KeyError:
            # vocabulary category does not exist within CRIPT Controlled Vocabulary
            raise InvalidVocabularyCategory(vocab_category=vocab_category, valid_vocab_category=all_controlled_vocab_categories)

        # TODO this can be faster with a dict of dicts that can do o(1) look up
        #  looping through an unsorted list is an O(n) look up which is slow
        # loop through the list
        for vocab_dict in controlled_vocabulary:
            # check the name exists within the dict
            if vocab_dict.get("name") == vocab_word:
                return True

        raise InvalidVocabulary(vocab=vocab_word, possible_vocab=list(controlled_vocabulary))

    def _get_db_schema(self) -> dict:
        """
        Sends a GET request to CRIPT to get the database schema and returns it.
        The database schema can be used for validating the JSON request
        before submitting it to CRIPT.

        1. checks if the db schema is already set
            * if already exists then it skips fetching it from the API and just returns what it already has
        2. if db schema has not been set yet, then it fetches it from the API
            * after getting it from the API it saves it in the `_schema` class variable,
            so it can be easily and efficiently gotten next time
        """

        # check if db schema is already saved
        if bool(self._db_schema):
            return self._db_schema

        # fetch db_schema from API
        else:
            # fetch db schema, get the JSON body of it, and get the data of that JSON
            response = requests.get(url=f"{self.host}/schema/").json()

            if response["code"] != 200:
                raise APIError(api_error=response.json())

            # get the data from the API JSON response
            self._db_schema = response["data"]
            return self._db_schema

    # TODO this should later work with both POST and PATCH. Currently, just works for POST
    def _is_node_schema_valid(self, node_json: str) -> Union[bool, CRIPTNodeSchemaError]:
        """
        checks a node JSON schema against the db schema to return if it is valid or not.

        1. get db schema
        1. convert node_json str to dict
        1. take out the node type from the dict
            1. "node": ["material"]
        1. use the node type from dict to tell the db schema which node schema to validate against
            1. Manipulates the string to be title case to work with db schema

        Parameters
        ----------
        node_json: str
            a node in JSON form string

        Notes
        -----
        This function does not take into consideration vocabulary validation.
            For vocabulary validation please check `is_vocab_valid`

        Raises
        ------
        CRIPTNodeSchemaError
            in case a node is invalid

        Returns
        -------
        bool
            whether the node JSON is valid or not
        """

        db_schema = self._get_db_schema()

        node_dict = json.loads(node_json)
        try:
            node_list = node_dict["node"]
        except KeyError:
            raise CRIPTNodeSchemaError(error_message=f"'node' attriubte not present in serialization of {node_json}. Missing for exmaple 'node': ['material'].")

        # TODO should use the `_is_node_field_valid()` function from utils.py to keep the code DRY
        # checking the node field "node": "Material"
        if isinstance(node_list, list) and len(node_list) == 1 and isinstance(node_list[0], str):
            node_type = node_list[0]
        else:
            raise CRIPTJsonNodeError(node_list, str(node_list))

        # set which node you are using schema validation for
        db_schema["$ref"] = f"#/$defs/{node_type}Post"

        try:
            jsonschema.validate(instance=node_dict, schema=db_schema)
        except jsonschema.exceptions.ValidationError as error:
            raise CRIPTNodeSchemaError(error_message=str(error))

        # if validation goes through without any problems return True
        return True

    def save(self, project: Project) -> None:
        """
        This method takes a project node, serializes the class into JSON
        and then sends the JSON to be saved to the API.
        It takes Project node because everything is connected to the Project node,
        and it can be used to send either a POST or PATCH request to API

        Parameters
        ----------
        project: Project
            the Project Node that the user wants to save

        Raises
        ------
        CRIPTAPISaveError
            If the API responds with anything other than an HTTP of `200`, the API error is displayed to the user

        Returns
        -------
        None
            Just sends a `POST` or `Patch` request to the API
        """
        # TODO work on this later to allow for PATCH as well
        response = requests.post(url=f"{self._host}/{project.node_type.lower()}", headers=self._http_headers, data=project.json)

        response = response.json()

        # if htt response is not 200 then show the API error to the user
        if response["code"] != 200:
            raise CRIPTAPISaveError(api_host_domain=self._host, http_code=response["code"], api_response=response["error"])

    def upload_file(self, file_path: Union[Path, str]) -> str:
        """
        uploads a file to AWS S3 bucket and returns a URL of the uploaded file in AWS S3
        The URL is has no expiration time limit and is available forever

        1. take an  file path of type path or str to the file on local storage
            * see Example for more details
        1. convert the file path to pathlib object, so it is versatile and
            always uniform regardless if the user passes in a str or path object
        1. get the file
        1. rename the file to avoid clash or overwriting of previously uploaded files
            * change file name to `original_name_uuid4.extension`
                *  `document_42926a201a624fdba0fd6271defc9e88.txt`
        # it would be without the hyphens like: `document_42926a201a624fdba0fd6271defc9e88.txt`
        1. upload file to AWS S3
        1. get the link of the uploaded file and return it


        Examples
        --------
        ```python
        import cript

        api = cript.API(host, token)

        # programmatically create the absolute path of your file, so the program always works correctly
        my_file_path = (Path(__file__) / Path('../upload_files/my_file.txt')).resolve()

        my_file_s3_url = api.upload_file(absolute_file_path=my_file_path)
        ```

        Parameters
        ----------
        file_path: Union[str, Path]
            file path as str or Path object. Path Object is recommended

        Raises
        ------
        FileNotFoundError
            In case the file could not be found because the file does not exist

        Returns
        -------
        url: str
            url of the AWS S3 uploaded file to be put into the File node source attribute
        """

        # convert file path from whatever the user passed in to a pathlib object
        file_path = pathlib.Path(file_path).resolve()

        # get file_name and file_extension from absolute file path
        # file_extension includes the dot, e.g. ".txt"
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))

        # generate a UUID4 string without dashes, making a cleaner file name
        uuid_str = str(uuid.uuid4().hex)

        new_file_name: str = f"{file_name}_{uuid_str}{file_extension}"

        # e.g. "directory/file_name_uuid.extension"
        object_name = f"{self._BUCKET_DIRECTORY_NAME}/{new_file_name}"

        # upload file to AWS S3
        self._s3_client.upload_file(file_path, self._BUCKET_NAME, object_name)

        # Generate a presigned URL to access the file from S3 that is available forever
        s3_file_url = self._s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._BUCKET_NAME, "Key": object_name},
        )

        # not sure if we want to return the file name to be found later or the S3 file URL
        return s3_file_url

    def download_file(self, file_url: str, destination_path: Union[Path, str]) -> None:
        """
        download a file from AWS S3 and save it to the specified path on local storage

        making a simple GET request to the URL that would download the file

        Parameters
        ----------
        file_url: str
            AWS S3 file name with the extension e.g. "my_file_name.txt
            the file is then searched within "Data/{file_name}" and saved to local storage
        destination_path: str
            please provide a path with file name of where you would like the file to be saved
            on local storage after retrieved and downloaded from AWS S3

        Examples
        --------
        ```python
        desktop_path = (Path(__file__) / Path("../../../../../test_file_upload/my_downloaded_file.txt")).resolve()
        cript_api.download_file(file_url=my_file_url, destination_path=desktop_path)
        ```

        Raises
        ------
        FileNotFoundError
            In case the file could not be found because the file does not exist

        Returns
        -------
        None
            just downloads the file to the specified path
        """

        response = requests.get(url=file_url)

        # if the status of the response is other than HTTP 200, raise an error
        if response.status_code != 200:
            raise FileDownloadError(error_message=response.json())

        file_contents: bytes = response.content

        # convert str or Path object to Path object to be flexible in accepting user input
        destination_file_path = Path(destination_path).resolve()

        with open(destination_file_path, "wb") as file:
            file.write(file_contents)

    # TODO reset to work with real nodes node_type.node and node_type to be PrimaryNode
    def search(
        self,
        node_type: BaseNode,
        search_mode: SearchModes,
        value_to_search: Union[None, str],
    ) -> Paginator:
        """
        This method is used to perform search on the CRIPT platform.

        Examples
        --------
        ```python
        # search by node type
        materials_paginator = cript_api.search(
            node_type=cript.Material,
            search_mode=cript.SearchModes.NODE_TYPE,
            value_to_search=None,
        )
        ```

        Parameters
        ----------
        node_type : PrimaryBaseNode
            Type of node that you are searching for.
        search_mode : SearchModes
            Type of search you want to do. You can search by name, `UUID`, `EXACT_NAME`, etc.
            Refer to [valid search modes](../search_modes)
        value_to_search : Union[str, None]
            What you are searching for can be either a value, and if you are only searching for
            a `NODE_TYPE`, then this value can be empty or `None`

        Returns
        -------
        Paginator
            paginator object for the user to use to flip through pages of search results
        """

        # get node typ from class
        node_type = node_type.node_type.lower()

        # always putting a page parameter of 0 for all search URLs
        page_number = 0

        # requesting a page of some primary node
        if search_mode == SearchModes.NODE_TYPE:
            api_endpoint: str = f"{self._host}/{node_type}"

        elif search_mode == SearchModes.CONTAINS_NAME:
            api_endpoint: str = f"{self._host}/search/{node_type}"

        elif search_mode == SearchModes.EXACT_NAME:
            api_endpoint: str = f"{self._host}/search/exact/{node_type}"

        elif search_mode == SearchModes.UUID:
            api_endpoint: str = f"{self._host}/{node_type}/{value_to_search}"
            # putting the value_to_search in the URL instead of a query
            value_to_search = None

        # TODO error handling if none of the API endpoints got hit
        return Paginator(http_headers=self._http_headers, api_endpoint=api_endpoint, query=value_to_search, current_page_number=page_number)
