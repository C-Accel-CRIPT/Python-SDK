import copy
import json
import logging
import os
import uuid
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import boto3
import jsonschema
import requests
from beartype import beartype

from cript.api.exceptions import (
    APIError,
    CRIPTAPIRequiredError,
    CRIPTAPISaveError,
    CRIPTConnectionError,
    InvalidHostError,
    InvalidVocabulary,
)
from cript.api.paginator import Paginator
from cript.api.utils.get_host_token import resolve_host_and_token
from cript.api.utils.save_helper import (
    _fix_node_save,
    _get_uuid_from_error_message,
    _identify_suppress_attributes,
    _InternalSaveValues,
)
from cript.api.utils.web_file_downloader import download_file_from_url
from cript.api.valid_search_modes import SearchModes
from cript.api.vocabulary_categories import ControlledVocabularyCategories
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
        raise CRIPTAPIRequiredError()
    return _global_cached_api


class API:
    """
    ## Definition
    API Client class to communicate with the CRIPT API
    """

    # dictates whether the user wants to see terminal log statements or not
    verbose: bool = True

    _host: str = ""
    _api_token: str = ""
    _storage_token: str = ""
    _http_headers: dict = {}
    _vocabulary: dict = {}
    _db_schema: dict = {}
    _api_handle: str = "api"
    _api_version: str = "v1"

    # trunk-ignore-begin(cspell)
    # AWS S3 constants
    _REGION_NAME: str = "us-east-1"
    _IDENTITY_POOL_ID: str = "us-east-1:555e15fe-05c1-4f63-9f58-c84d8fd6dc99"
    _COGNITO_LOGIN_PROVIDER: str = "cognito-idp.us-east-1.amazonaws.com/us-east-1_VinmyZ0zW"
    _BUCKET_NAME: str = "cript-development-user-data"
    _BUCKET_DIRECTORY_NAME: str = "python_sdk_files"
    _internal_s3_client: Any = None  # type: ignore
    # trunk-ignore-end(cspell)

    @beartype
    def __init__(self, host: Union[str, None] = None, api_token: Union[str, None] = None, storage_token: Union[str, None] = None, config_file_path: Union[str, Path] = ""):
        """
        Initialize CRIPT API client with host and token.
        Additionally, you can  use a config.json file and specify the file path.

        !!! note "api client context manager"
            It is necessary to use a `with` context manager for the API

        Examples
        --------
        ### Create API client with host and token
        ```Python
        with cript.API('https://criptapp.org', 'secret_token') as api:
           # node creation, api.save(), etc.
        ```

        ---

        ### Create API client with config.json
        `config.json`
        ```json
        {
            "host": "https://criptapp.org",
            "token": "I am token"
        }
        ```

        `my_script.py`
        ```python
        from pathlib import Path

        # create a file path object of where the config file is
        config_file_path = Path(__file__) / Path('./config.json')

        with cript.API(config_file_path=config_file_path) as api:
            # node creation, api.save(), etc.
        ```

        Parameters
        ----------
        host : str, None
            CRIPT host for the Python SDK to connect to such as `https://criptapp.org`
            This host address is the same address used to login to cript website.
            If `None` is specified, the host is inferred from the environment variable `CRIPT_HOST`.
        api_token : str, None
            CRIPT API Token used to connect to CRIPT and upload all data with the exception to file upload that needs
            a different token.
            You can find your personal token on the cript website at User > Security Settings.
            The user icon is in the top right.
            If `None` is specified, the token is inferred from the environment variable `CRIPT_TOKEN`.
        storage_token: str
            This token is used to upload local files to CRIPT cloud storage when needed
        config_file_path: str
            the file path to the config.json file where the token and host can be found


        Notes
        -----
        * if `host=None` and `token=None`
            then the Python SDK will grab the host from the users environment variable of `"CRIPT_HOST"`
            and `"CRIPT_TOKEN"`

        Warns
        -----
        UserWarning
            If `host` is using "http" it gives the user a warning that HTTP is insecure and the user should use HTTPS

        Raises
        ------
        CRIPTConnectionError
            If it cannot connect to CRIPT with the provided host and token a CRIPTConnectionError is thrown.

        Returns
        -------
        None
            Instantiate a new CRIPT API object
        """

        # if there is a config.json file or any of the parameters are None, then get the variables from file or env vars
        if config_file_path or (host is None or api_token is None or storage_token is None):
            authentication_dict: Dict[str, str] = resolve_host_and_token(host, api_token=api_token, storage_token=storage_token, config_file_path=config_file_path)

            host = authentication_dict["host"]
            api_token = authentication_dict["api_token"]
            storage_token = authentication_dict["storage_token"]

        self._host = self._prepare_host(host=host)  # type: ignore
        self._api_token = api_token  # type: ignore
        self._storage_token = storage_token  # type: ignore

        # add Bearer to token for HTTP requests
        self._http_headers = {"Authorization": f"Bearer {self._api_token}", "Content-Type": "application/json"}

        # check that api can connect to CRIPT with host and token
        self._check_initial_host_connection()

        self._get_db_schema()

    @beartype
    def _prepare_host(self, host: str) -> str:
        # strip ending slash to make host always uniform
        host = host.rstrip("/")
        host = f"{host}/{self._api_handle}/{self._api_version}"

        # if host is using unsafe "http://" then give a warning
        if host.startswith("http://"):
            warnings.warn("HTTP is an unsafe protocol please consider using HTTPS.")

        if not host.startswith("http"):
            raise InvalidHostError()

        return host

    # Use a property to ensure delayed init of s3_client
    @property
    def _s3_client(self) -> boto3.client:  # type: ignore
        """
        creates or returns a fully authenticated and ready s3 client

        Returns
        -------
        s3_client: boto3.client
            fully prepared and authenticated s3 client ready to be used throughout the script
        """

        if self._internal_s3_client is None:
            auth = boto3.client("cognito-identity", region_name=self._REGION_NAME)
            identity_id = auth.get_id(IdentityPoolId=self._IDENTITY_POOL_ID, Logins={self._COGNITO_LOGIN_PROVIDER: self._storage_token})
            # TODO remove this temporary fix to the token, by getting is from back end.
            aws_token = self._storage_token

            aws_credentials = auth.get_credentials_for_identity(IdentityId=identity_id["IdentityId"], Logins={self._COGNITO_LOGIN_PROVIDER: aws_token})
            aws_credentials = aws_credentials["Credentials"]
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_credentials["AccessKeyId"],
                aws_secret_access_key=aws_credentials["SecretKey"],
                aws_session_token=aws_credentials["SessionToken"],
            )
            self._internal_s3_client = s3_client
        return self._internal_s3_client

    def __enter__(self):
        self.connect()
        return self

    @beartype
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
            raise CRIPTConnectionError(self.host, self._api_token) from exc

    def _get_vocab(self) -> dict:
        """
        gets the entire CRIPT controlled vocabulary and stores it in _vocabulary

        1. loops through all controlled vocabulary categories
            1. if the category already exists in the controlled vocabulary then skip that category and continue
            1. if the category does not exist in the `_vocabulary` dict,
            then request it from the API and append it to the `_vocabulary` dict
        1. at the end the `_vocabulary` should have all the controlled vocabulary and that will be returned

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

        # loop through all vocabulary categories and make a request to each vocabulary category
        # and put them all inside of self._vocab with the keys being the vocab category name
        for category in ControlledVocabularyCategories:
            if category in self._vocabulary:
                continue

            self._vocabulary[category.value] = self.get_vocab_by_category(category)

        return self._vocabulary

    @beartype
    def get_vocab_by_category(self, category: ControlledVocabularyCategories) -> List[dict]:
        """
        get the CRIPT controlled vocabulary by category

        Parameters
        ----------
        category: str
            category of

        Returns
        -------
        List[dict]
            list of JSON containing the controlled vocabulary
        """

        # check if the vocabulary category is already cached
        if category.value in self._vocabulary:
            return self._vocabulary[category.value]

        # if vocabulary category is not in cache, then get it from API and cache it
        response = requests.get(f"{self.host}/cv/{category.value}").json()

        if response["code"] != 200:
            # TODO give a better CRIPT custom Exception
            raise Exception(f"while getting controlled vocabulary from CRIPT for {category}, " f"the API responded with http {response} ")

        # add to cache
        self._vocabulary[category.value] = response["data"]

        return self._vocabulary[category.value]

    @beartype
    def _is_vocab_valid(self, vocab_category: ControlledVocabularyCategories, vocab_word: str) -> bool:
        """
        checks if the vocabulary is valid within the CRIPT controlled vocabulary.
        Either returns True or InvalidVocabulary Exception

        1. if the vocabulary is custom (starts with "+")
            then it is automatically valid
        2. if vocabulary is not custom, then it is checked against its category
            if the word cannot be found in the category then it returns False

        Parameters
        ----------
        vocab_category: ControlledVocabularyCategories
            ControlledVocabularyCategories enums
        vocab_word: str
            the vocabulary word e.g. "CAS", "SMILES", "BigSmiles", "+my_custom_key"

        Returns
        -------
        a boolean of if the vocabulary is valid

        Raises
        ------
        InvalidVocabulary
            If the vocabulary is invalid then the error gets raised
        """

        # check if vocab is custom
        # This is deactivated currently, no custom vocab allowed.
        if vocab_word.startswith("+"):
            return True

        # get the entire vocabulary
        controlled_vocabulary = self._get_vocab()
        # get just the category needed
        controlled_vocabulary = controlled_vocabulary[vocab_category.value]

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

    @beartype
    def _is_node_schema_valid(self, node_json: str, is_patch: bool = False) -> bool:
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
        is_patch: bool
            a boolean flag checking if it needs to validate against `NodePost` or `NodePatch`

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
            raise CRIPTJsonNodeError(node_list=node_dict["node"], json_str=json.dumps(node_dict))

        # TODO should use the `_is_node_field_valid()` function from utils.py to keep the code DRY
        # checking the node field "node": "Material"
        if isinstance(node_list, list) and len(node_list) == 1 and isinstance(node_list[0], str):
            node_type = node_list[0]
        else:
            raise CRIPTJsonNodeError(node_list, str(node_list))

        if self.verbose:
            # logging out info to the terminal for the user feedback
            # (improve UX because the program is currently slow)
            logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
            logging.info(f"Validating {node_type} graph...")

        # set the schema to test against http POST or PATCH of DB Schema
        schema_http_method: str

        if is_patch:
            schema_http_method = "Patch"
        else:
            schema_http_method = "Post"

        # set which node you are using schema validation for
        db_schema["$ref"] = f"#/$defs/{node_type}{schema_http_method}"

        try:
            jsonschema.validate(instance=node_dict, schema=db_schema)
        except jsonschema.exceptions.ValidationError as error:
            raise CRIPTNodeSchemaError(node_type=node_dict["node"], json_schema_validation_error=str(error)) from error

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
        A set of extra saved node UUIDs.
            Just sends a `POST` or `Patch` request to the API
        """
        try:
            self._internal_save(project)
        except CRIPTAPISaveError as exc:
            if exc.pre_saved_nodes:
                for node_uuid in exc.pre_saved_nodes:
                    # TODO remove all pre-saved nodes by their uuid.
                    pass
            raise exc from exc

    def _internal_save(self, node, save_values: Optional[_InternalSaveValues] = None) -> _InternalSaveValues:
        """
        Internal helper function that handles the saving of different nodes (not just project).

        If a "Bad UUID" error happens, we find that node with the UUID and save it first.
        Then we recursively call the _internal_save again.
        Because it is recursive, this repeats until no "Bad UUID" error happen anymore.
        This works, because we keep track of "Bad UUID" handled nodes, and represent them in the JSON only as the UUID.
        """

        if save_values is None:
            save_values = _InternalSaveValues()

        # saves all the local files to cloud storage right before saving the Project node
        # Ensure that all file nodes have uploaded there payload before actual save.
        for file_node in node.find_children({"node": ["File"]}):
            file_node.ensure_uploaded(api=self)

        node.validate()

        # Dummy response to have a virtual do-while loop, instead of while loop.
        response = {"code": -1}
        # TODO remove once get works properly
        force_patch = False

        while response["code"] != 200:
            # Keep a record of how the state was before the loop
            old_save_values = copy.deepcopy(save_values)
            # We assemble the JSON to be saved to back end.
            # Note how we exclude pre-saved uuid nodes.
            json_data = node.get_json(known_uuid=save_values.saved_uuid, suppress_attributes=save_values.suppress_attributes).json

            # This checks if the current node exists on the back end.
            # if it does exist we use `patch` if it doesn't `post`.
            test_get_response: Dict = requests.get(url=f"{self._host}/{node.node_type_snake_case}/{str(node.uuid)}", headers=self._http_headers).json()
            patch_request = test_get_response["code"] == 200

            # TODO remove once get works properly
            if not patch_request and force_patch:
                patch_request = True
                force_patch = False
            # TODO activate patch validation
            # node.validate(is_patch=patch_request)

            # If all that is left is a UUID, we don't need to save it, we can just exit the loop.
            if patch_request and len(json.loads(json_data)) == 1:
                response = {"code": 200}
                break

            if patch_request:
                response: Dict = requests.patch(url=f"{self._host}/{node.node_type_snake_case}/{str(node.uuid)}", headers=self._http_headers, data=json_data).json()  # type: ignore
            else:
                response: Dict = requests.post(url=f"{self._host}/{node.node_type_snake_case}", headers=self._http_headers, data=json_data).json()  # type: ignore

            # If we get an error we may be able to fix, we to handle this extra and save the bad node first.
            # Errors with this code, may be fixable
            if response["code"] in (400, 409):
                returned_save_values = _fix_node_save(self, node, response, save_values)
                save_values += returned_save_values

            # Handle errors from patching with too many attributes
            if patch_request and response["code"] in (400,):
                suppress_attributes = _identify_suppress_attributes(node, response)
                new_save_values = _InternalSaveValues(save_values.saved_uuid, suppress_attributes)
                save_values += new_save_values

            # It is only worthwhile repeating the attempted save loop if our state has improved.
            # Aka we did something to fix the occurring error
            if not save_values > old_save_values:
                # TODO remove once get works properly
                if not patch_request and response["code"] == 409 and response["error"].strip().startswith("Duplicate uuid:"):  # type: ignore
                    duplicate_uuid = _get_uuid_from_error_message(response["error"])  # type: ignore
                    if str(node.uuid) == duplicate_uuid:
                        print("force_patch", node.uuid)
                        force_patch = True
                        continue

                break

        if response["code"] != 200:
            raise CRIPTAPISaveError(api_host_domain=self._host, http_code=response["code"], api_response=response["error"], patch_request=patch_request, pre_saved_nodes=save_values.saved_uuid, json_data=json_data)  # type: ignore

        save_values.saved_uuid.add(str(node.uuid))
        return save_values

    def upload_file(self, file_path: Union[Path, str]) -> str:
        # trunk-ignore-begin(cspell)
        """
        uploads a file to AWS S3 bucket and returns a URL of the uploaded file in AWS S3
        The URL is has no expiration time limit and is available forever

        1. take a file path of type path or str to the file on local storage
            * see Example for more details
        1. convert the file path to pathlib object, so it is versatile and
            always uniform regardless if the user passes in a str or path object
        1. get the file
        1. rename the file to avoid clash or overwriting of previously uploaded files
            * change file name to `original_name_uuid4.extension`
                *  `document_42926a201a624fdba0fd6271defc9e88.txt`
        1. upload file to AWS S3
        1. get the link of the uploaded file and return it


        Parameters
        ----------
        file_path: Union[str, Path]
            file path as str or Path object. Path Object is recommended

        Examples
        --------
        ```python
        import cript

        api = cript.API(host, token)

        # programmatically create the absolute path of your file, so the program always works correctly
        my_file_path = (Path(__file__) / Path('../upload_files/my_file.txt')).resolve()

        my_file_s3_url = api.upload_file(absolute_file_path=my_file_path)
        ```

        Raises
        ------
        FileNotFoundError
            In case the CRIPT Python SDK cannot find the file on your computer because the file does not exist
            or the path to it is incorrect it raises
            [FileNotFoundError](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)

        Returns
        -------
        object_name: str
            object_name of the AWS S3 uploaded file to be put into the File node source attribute
        """
        # trunk-ignore-end(cspell)

        # TODO consider using a new variable when converting `file_path` from parameter
        #  to a Path object with a new type
        # convert file path from whatever the user passed in to a pathlib object
        file_path = Path(file_path).resolve()

        # get file_name and file_extension from absolute file path
        # file_extension includes the dot, e.g. ".txt"
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))

        # generate a UUID4 string without dashes, making a cleaner file name
        uuid_str: str = str(uuid.uuid4().hex)

        new_file_name: str = f"{file_name}_{uuid_str}{file_extension}"

        # e.g. "directory/file_name_uuid.extension"
        object_name: str = f"{self._BUCKET_DIRECTORY_NAME}/{new_file_name}"

        # upload file to AWS S3
        self._s3_client.upload_file(Filename=file_path, Bucket=self._BUCKET_NAME, Key=object_name)  # type: ignore

        # return the object_name within AWS S3 for easy retrieval
        return object_name

    @beartype
    def download_file(self, file_source: str, destination_path: str = ".") -> None:
        """
        Download a file from CRIPT Cloud Storage (AWS S3) and save it to the specified path.

        ??? Info "Cloud Storage vs Web URL File Download"

            If the `object_name` does not starts with `http` then the program assumes the file is in AWS S3 storage,
            and attempts to retrieve it via
            [boto3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

            If the `object_name` starts with `http` then the program knows that
            it is a file stored on the web. The program makes a simple
            [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) request to get the file,
            then writes the contents of it to the specified destination.

            > Note: The current version of the program is designed to download files from the web in a straightforward
            manner. However, please be aware that the program may encounter limitations when dealing with URLs that
            require JavaScript or a session to be enabled. In such cases, the download method may fail.

            > We acknowledge these limitations and plan to enhance the method in future versions to ensure compatibility
            with a wider range of web file URLs. Our goal is to develop a robust solution capable of handling any and
            all web file URLs.

        Parameters
        ----------
        file_source: str
            object_name: within AWS S3 the extension e.g. "my_file_name.txt
            the file is then searched within "Data/{file_name}" and saved to local storage
            URL file source: In case of the file source is a URL then it is the file source URL
                starting with "https://"
                example: `https://criptscripts.org/cript_graph_json/JSON/cao_protein.json`
        destination_path: str
            please provide a path with file name of where you would like the file to be saved
            on local storage.
            > If no path is specified, then by default it will download the file
            to the current working directory.

            > The destination path must include a file name and file extension
                e.g.: `~/Desktop/my_example_file_name.extension`

        Examples
        --------
        ```python
        from pathlib import Path

        desktop_path = (Path(__file__).parent / "cript_downloads" / "my_downloaded_file.txt").resolve()
        cript_api.download_file(file_url=my_file_source, destination_path=desktop_path)
        ```

        Raises
        ------
        FileNotFoundError
            In case the file could not be found because the file does not exist or the path given is incorrect

        Returns
        -------
        None
            Simply downloads the file
        """

        # if the file source is a URL
        if file_source.startswith("http"):
            download_file_from_url(url=file_source, destination_path=Path(destination_path).resolve())
            return

        # the file is stored in cloud storage and must be retrieved via object_name
        self._s3_client.download_file(Bucket=self._BUCKET_NAME, Key=file_source, Filename=destination_path)  # type: ignore

    @beartype
    def search(
        self,
        node_type,
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
        node_type = node_type.node_type_snake_case
        print(node_type)

        # always putting a page parameter of 0 for all search URLs
        page_number = 0

        api_endpoint: str = ""

        # requesting a page of some primary node
        if search_mode == SearchModes.NODE_TYPE:
            api_endpoint = f"{self._host}/{node_type}"

        elif search_mode == SearchModes.CONTAINS_NAME:
            api_endpoint = f"{self._host}/search/{node_type}"

        elif search_mode == SearchModes.EXACT_NAME:
            api_endpoint = f"{self._host}/search/exact/{node_type}"

        elif search_mode == SearchModes.UUID:
            api_endpoint = f"{self._host}/{node_type}/{value_to_search}"
            # putting the value_to_search in the URL instead of a query
            value_to_search = None

        assert api_endpoint != ""

        # TODO error handling if none of the API endpoints got hit
        return Paginator(http_headers=self._http_headers, api_endpoint=api_endpoint, query=value_to_search, current_page_number=page_number)
