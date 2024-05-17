import copy
import json
import logging
import os
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Union

import boto3
import requests
from beartype import beartype

from cript.api.api_config import _API_TIMEOUT
from cript.api.data_schema import DataSchema
from cript.api.exceptions import (
    APIError,
    CRIPTAPIRequiredError,
    CRIPTAPISaveError,
    CRIPTConnectionError,
    CRIPTDuplicateNameError,
)
from cript.api.paginator import Paginator
from cript.api.utils.aws_s3_utils import get_s3_client
from cript.api.utils.get_host_token import resolve_host_and_token
from cript.api.utils.save_helper import (
    _fix_node_save,
    _identify_suppress_attributes,
    _InternalSaveValues,
)
from cript.api.utils.web_file_downloader import download_file_from_url
from cript.api.valid_search_modes import SearchModes
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
    _logger: logging.Logger = None  # type: ignore

    _host: str = ""
    _api_token: str = ""
    _storage_token: str = ""
    _db_schema: Optional[DataSchema] = None
    _api_prefix: str = "api"
    _api_version: str = "v1"
    _api_request_session: Union[None, requests.Session] = None

    # trunk-ignore-begin(cspell)
    # AWS S3 constants
    _REGION_NAME: str = "us-east-1"
    _IDENTITY_POOL_ID: str = "us-east-1:9426df38-994a-4191-86ce-3cb0ce8ac84d"
    _COGNITO_LOGIN_PROVIDER: str = "cognito-idp.us-east-1.amazonaws.com/us-east-1_SZGBXPl2j"
    _BUCKET_NAME: str = "cript-user-data"
    _BUCKET_DIRECTORY_NAME: str = "python_sdk_files"
    _internal_s3_client: Any = None  # type: ignore
    # trunk-ignore-end(cspell)

    extra_api_log_debug_info: bool = False

    @beartype
    def __init__(self, host: Union[str, None] = None, api_token: Union[str, None] = None, storage_token: Union[str, None] = None, config_file_path: Union[str, Path] = "", default_log_level=logging.INFO):
        """
        Initialize CRIPT API client with host and token.
        Additionally, you can  use a config.json file and specify the file path.

        !!! note "api client context manager"
            It is necessary to use a `with` context manager for the API

        Examples
        --------
        ### Create API client with host and token
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...    # node creation, api.save(), etc.
        ...    pass


        ---

        ### Creating API Client
        !!! Warning "Token Security"
            It is **highly** recommended that you store your API tokens in a safe location and read it into your code
            Hard-coding API tokens directly into the code can pose security risks,
            as the token might be exposed if the code is shared or stored in a version control system.
            Anyone that has access to your tokens can impersonate you on the CRIPT platform

        ### Create API Client with Environment Variables

        Another great way to keep sensitive information secure is by using
        [environment variables](https://www.freecodecamp.org/news/python-env-vars-how-to-get-an-environment-variable-in-python/).
        Sensitive information can be securely stored in environment variables and loaded into the code using
        [os.getenv()](https://docs.python.org/3/library/os.html#os.getenv).

        Examples
        --------
        >>> import cript
        >>> import os
        >>> # securely load sensitive data into the script
        >>> cript_host = os.getenv("cript_host")
        >>> cript_api_token = os.getenv("cript_api_token")
        >>> cript_storage_token = os.getenv("cript_storage_token")
        >>> with cript.API(
        ...     host=cript_host, api_token=cript_api_token, storage_token=cript_storage_token
        ... ) as api:
        ...     pass

        ### Create API Client with None
        Alternatively you can configure your system to have an environment variable of
        `CRIPT_TOKEN` for the API token and `CRIPT_STORAGE_TOKEN` for the storage token, then
        initialize `cript.API` `api_token` and `storage_token` with `None`.

        The CRIPT Python SDK will try to read the API Token and Storage token from your system's environment variables.

        ```python
        with cript.API(host=cript_host, api_token=None, storage_token=None) as api:
            # write your script
            pass
        ```

        ### Create API client with config.json
        `config.json`
        ```json
        {
            "host": "https://api.criptapp.org/",
            "api_token": "I am API token",
            "storage_token": "I am storage token"
        }
        ```

        Examples
        --------
        `my_script.py`
        >>> from pathlib import Path
        >>> import cript
        >>> # create a file path object of where the config file is
        >>> config_file_path = Path(__file__) / Path('./config.json')
        >>> with cript.API(config_file_path=config_file_path) as api:   # doctest: +SKIP
        ...     # node creation, api.save(), etc.
        ...     pass

        Parameters
        ----------
        host : str, None
            CRIPT host for the Python SDK to connect to such as https://api.criptapp.org/`
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

        self._host: str = host.rstrip("/")
        self._api_token = api_token  # type: ignore
        self._storage_token = storage_token  # type: ignore

        # set a logger instance to use for the class logs
        self._init_logger(default_log_level)

    def __str__(self) -> str:
        """
        States the host of the CRIPT API client

        Examples
        --------
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...     print(api)
        CRIPT API Client - Host URL: 'https://api.criptapp.org'

        Returns
        -------
        str
        """
        return f"CRIPT API Client - Host URL: '{self.host}'"

    def _init_logger(self, log_level=logging.INFO) -> None:
        """
        Prepare and configure the logger for the API class.

        This function creates and configures a logger instance associated with the current module (class).

        Parameters
        ----------
        log_level: logging.LEVEL default logging.INFO
            set if you want `cript.API` to give logs to console or not

        Returns
        -------
        logging.Logger
            The configured logger instance.
        """
        # Create a logger instance associated with the current module
        logger = logging.getLogger(__name__)

        logger.setLevel(log_level)

        # Activate Warning handling
        logging.captureWarnings(True)

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Create a formatter for log messages (customize the format as desired)
        formatter = logging.Formatter("%(levelname)s: %(message)s")

        # Associate the formatter with the console handler
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        # set logger for the class
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    # Use a property to ensure delayed init of s3_client
    @property
    def _s3_client(self) -> boto3.client:  # type: ignore
        """
        Property to use when wanting to interact with AWS S3.

        Gets a fully authenticated AWS S3 client if it was never created and stash it,
        if the AWS S3 client has been created before, then returns the client that it has

        Returns
        -------
        s3_client: boto3.client
            fully prepared and authenticated s3 client ready to be used throughout the script
        """
        if self._internal_s3_client is None:
            self._internal_s3_client = get_s3_client(region_name=self._REGION_NAME, identity_pool_id=self._IDENTITY_POOL_ID, cognito_login_provider=self._COGNITO_LOGIN_PROVIDER, storage_token=self._storage_token)

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

        Raises
        -------
        CRIPTConnectionError
            raised when the host does not give the expected response
        """

        # Establish a requests session object
        if self._api_request_session:
            self.disconnect()
        self._api_request_session = requests.Session()
        # add Bearer to token for HTTP requests
        self._api_request_session.headers = {"Authorization": f"Bearer {self._api_token}", "Content-Type": "application/json"}

        # As a form to check our connection, we pull and establish the data schema
        try:
            self._db_schema = DataSchema(self)
        except APIError as exc:
            raise CRIPTConnectionError(self.host, self._api_token) from exc

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
        # Disconnect request session
        if self._api_request_session:
            self._api_request_session.close()

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

        The term "host" designates the specific CRIPT instance to which you intend to upload your data.

        For most users, the host will be `https://api.criptapp.org`

        ```yaml
        host: https://api.criptapp.org
        ```

        Examples
        --------
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...    print(api.host)
        https://api.criptapp.org
        """
        return self._host

    @property
    def api_prefix(self):
        return self._api_prefix

    @property
    def api_version(self):
        return self._api_version

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

        node.validate(force_validation=True)

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
            test_get_response: Dict = self._capsule_request(url_path=f"/{node.node_type_snake_case}/{str(node.uuid)}/", method="GET").json()
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

            method = "POST"
            url_path = f"/{node.node_type_snake_case}/"
            if patch_request:
                method = "PATCH"
                url_path += f"{str(node.uuid)}/"

            response: Dict = self._capsule_request(url_path=url_path, method=method, data=json_data).json()  # type: ignore

            # if node.node_type != "Project":
            #     test_success: Dict = requests.get(url=f"{self._host}/{node.node_type_snake_case}/{str(node.uuid)}/", headers=self._http_headers, timeout=_API_TIMEOUT).json()
            #     print("XYZ", json_data, save_values, response, test_success)

            # print(json_data, patch_request, response, save_values)
            # If we get an error we may be able to fix, we to handle this extra and save the bad node first.
            # Errors with this code, may be fixable
            if response["code"] in (400, 409):
                try:
                    returned_save_values = _fix_node_save(self, node, response, save_values)
                except CRIPTAPISaveError as exc:
                    # If the previous error was a duplicated name issue
                    if "duplicate item [{'name':" in str(response["error"]):
                        # And (second condition) the request failed bc of the now suppressed name
                        if "'name' is a required property" in exc.api_response:
                            # Raise a save error, with the nice name related error message
                            raise CRIPTDuplicateNameError(response, json_data, exc) from exc
                    # Else just raise the exception as normal.
                    raise exc
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
                if not patch_request:
                    # and response["code"] == 409 and response["error"].strip().startswith("Duplicate uuid:"):  # type: ignore
                    # duplicate_uuid = _get_uuid_from_error_message(response["error"])  # type: ignore
                    # if str(node.uuid) == duplicate_uuid:
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
        >>> from pathlib import Path
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...     # programmatically create the absolute path of your file, so the program always works correctly
        ...     my_file_path = (Path(__file__) / Path('../upload_files/my_file.txt')).resolve()
        ...     my_file_cloud_storage_source = api.upload_file(file_path=my_file_path)  # doctest: +SKIP

        Notes
        -----
        We recommend using a [Path](https://docs.python.org/3/library/pathlib.html) object for specifying a file path.
        Using the Python [pathlib library](https://docs.python.org/3/library/pathlib.html) provides platform-agnostic approach
        for filesystem operations, ensuring seamless functionality across different operating systems.
        Additionally, [Path](https://docs.python.org/3/library/pathlib.html) objects offer various built-in methods
        for more sophisticated and secure file handling and has a easy to use interface that can make working with it a breeze
        and can help reduce errors.

        Other options include using a raw string for relative/absolute file path,
        or using the [os.path module](https://docs.python.org/3/library/os.path.html).


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

        self.logger.info(f"Uploaded File: '{file_path}' to CRIPT storage")

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
            `object_name`: file downloaded via object_name from cloud storage and saved to local storage
            object_name e.g. `"Data/{file_name}"`
            ---
            `URL file source`: If the file source starts with `http` then it is downloaded via `GET` request and
            saved to local storage
           URL file source e.g. `https://criptscripts.org/cript_graph_json/JSON/cao_protein.json`
        destination_path: str
            please provide a path with file name of where you would like the file to be saved
            on local storage.
            > If no path is specified, then by default it will download the file
            to the current working directory.

            > The destination path must include a file name and file extension
                e.g.: `~/Desktop/my_example_file_name.extension`

        Examples
        --------
        >>> from pathlib import Path
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...     desktop_path = (Path(__file__).parent / "cript_downloads" / "my_downloaded_file.txt").resolve()
        ...     my_file = cript.File(
        ...         name="my file node name",
        ...         source="https://criptapp.org",
        ...         type="calibration",
        ...         extension=".csv",
        ...     )
        ...     api.download_file(file_source=my_file.source, destination_path=str(desktop_path)) # doctest: +SKIP

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
        node_type: Any,
        search_mode: SearchModes,
        value_to_search: str = "",
    ) -> Paginator:
        """
        This method is used to perform search on the CRIPT platform.

        Essentially creates needed resources and passes it to paginator to get results from API
        and display them.

        Examples
        --------
        ???+ Example "Search by Node Type"
            ```python
            materials_iterator = cript_api.search(
                node_type=cript.Material,
                search_mode=cript.SearchModes.NODE_TYPE,
            )
            ```

        ??? Example "Search by Contains name"
            ```python
            contains_name_iterator = cript_api.search(
                node_type=cript.Process,
                search_mode=cript.SearchModes.CONTAINS_NAME,
                value_to_search="poly"
            )
            ```

        ??? Example "Search by Exact Name"
            ```python
            exact_name_iterator = cript_api.search(
                node_type=cript.Project,
                search_mode=cript.SearchModes.EXACT_NAME,
                value_to_search="Sodium polystyrene sulfonate"
            )
            ```

        ??? Example "Search by UUID"
            ```python
            uuid_iterator = cript_api.search(
                node_type=cript.Collection,
                search_mode=cript.SearchModes.UUID,
                value_to_search="75fd3ee5-48c2-4fc7-8d0b-842f4fc812b7"
            )
            ```

        ??? Example "Search by BigSmiles"
            ```python
            iterator = cript_api.search(
                node_type=cript.Material,
                search_mode=cript.SearchModes.BIGSMILES,
                value_to_search="{[][$]CC(C)(C(=O)OCCCC)[$][]}"
            )
            ```

        Parameters
        ----------
        node_type : UUIDBaseNode
            Type of node that you are searching for.
        search_mode : SearchModes
            Type of search you want to do. You can search by name, `UUID`, `EXACT_NAME`, etc.
            Refer to [valid search modes](../search_modes)
        value_to_search : str
            What you are searching for can be either a value, and if you are only searching for
            a `NODE_TYPE`, then this value can be empty or `None`

        Returns
        -------
        Paginator
            An iterator that will present and fetch the results to the user seamlessly

        Notes
        -----
        To learn more about working with pagination, please refer to our
        [paginator object documentation](../paginator).
        """

        # get node typ from class
        node_type = node_type.node_type_snake_case

        api_endpoint: str = ""
        limit_node_fetches: Optional[int] = None
        if search_mode == SearchModes.NODE_TYPE:
            api_endpoint = f"/search/{node_type}"
            value_to_search = ""

        elif search_mode == SearchModes.CONTAINS_NAME:
            api_endpoint = f"/search/{node_type}"

        elif search_mode == SearchModes.EXACT_NAME:
            api_endpoint = f"/search/exact/{node_type}"
            limit_node_fetches = 1

        elif search_mode == SearchModes.UUID:
            api_endpoint = f"/{node_type}/{value_to_search}"
            # putting the value_to_search in the URL instead of a query
            value_to_search = ""
            limit_node_fetches = 1

        elif search_mode == SearchModes.BIGSMILES:
            api_endpoint = "/search/bigsmiles/"

        # error handling if none of the API endpoints got hit
        else:
            raise RuntimeError("Internal Error: Failed to recognize any search modes. Please report this bug on https://github.com/C-Accel-CRIPT/Python-SDK/issues.")

        return Paginator(api=self, url_path=api_endpoint, query=value_to_search, limit_node_fetches=limit_node_fetches)

    def delete(self, node) -> None:
        """
        Simply deletes the desired node from the CRIPT API and writes a log in the terminal that the node has been
        successfully deleted.

        Examples
        --------
        >>> import cript
        >>> my_material_node = cript.Material(
        ...     name="my component material 1",
        ...     names = ["component 1 alternative name"],
        ... )
        >>> api.delete(node=my_material_node) # doctest: +SKIP

        Notes
        -----
        After the node has been successfully deleted, a log is written to the terminal

        ```bash
        INFO: Deleted 'Material' with UUID of '80bfc642-157e-4692-a547-97c470725397' from CRIPT API.
        ```

        ??? info "Implementation Details"
            Under the hood, this method actually calls
            [delete_node_by_uuid](./#cript.api.api.API.delete_node_by_uuid)
            with the node_type and node UUID

        Warnings
        --------
        After successfully deleting a node from the API, keep in mind that your local Project node in your script
        may still contain outdated data as it has not been synced with the API.

        To ensure you have the latest data, follow these steps:

        1. Fetch the newest Project node from the API using the [`cript.API.search()`](./#cript.api.api.API.search) provided by the SDK.
        1. Deserialize the retrieved data into a new Project node using the [`load_nodes_from_json`](../../utility_functions/#cript.nodes.util.load_nodes_from_json) utility function.
        1. Replace your old Project node with the new one in your script for accurate and up-to-date information.

        Parameters
        ----------
        node: UUIDBaseNode
            The node that you want to delete

        Raises
        ------
        APIError
            If the API responds with anything other than HTTP status 200, then the CRIPT Python SDK raises `APIError`
            `APIError` is raised in case the API cannot delete the specified node.
            Such cases can happen if you do not have permission to delete the node
            or if the node is actively being used elsewhere in CRIPT platform and the API cannot delete it.

        Returns
        -------
        None
        """
        self.delete_node_by_uuid(node_type=node.node_type_snake_case, node_uuid=str(node.uuid))

    @beartype
    def delete_node_by_uuid(self, node_type: str, node_uuid: str) -> None:
        """
        Simply deletes the desired node from the CRIPT API and writes a log in the terminal that the node has been
        successfully deleted.

        Examples
        --------
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...      api.delete_node_by_uuid(
        ...         node_type="computation_process",
        ...         node_uuid="2fd3d500-304d-4a06-8628-a79b59344b2f"
        ...     ) # doctest: +SKIP

        ??? "How to get `node_type in snake case`"
               You can get the `node type in snake case` of a node via:
               ```python
                import cript
                print(cript.ComputationProcess.node_type_snake_case)
               computation_process
               ```

               You can also call `api.delete_node_by_uuid()` with
               ```python
               api.delete(
                   node_type=cript.ComputationProcess.node_type_snake_case,
                   node_uuid="2fd3d500-304d-4a06-8628-a79b59344b2f",
               )
               ```

        Notes
        -----
        After the node has been successfully deleted, a log is written

        ```bash
        INFO: Deleted 'Material' with UUID of '80bfc642-157e-4692-a547-97c470725397' from CRIPT API.
        ```

        Warnings
        --------
        After successfully deleting a node from the API, keep in mind that your local Project node in your script
        may still contain outdated data as it has not been synced with the API.

        To ensure you have the latest data, follow these steps:

        1. Fetch the newest Project node from the API using the
        [`cript.API.search()`](./#cript.api.api.API.search) provided by the SDK.
        1. Deserialize the retrieved data into a new Project node using the
        [`load_nodes_from_json`](../../utility_functions/#cript.nodes.util.load_nodes_from_json) utility function.
        1. Replace your old Project node with the new one in your script for accurate and up-to-date information.

        Parameters
        ----------
        node_type: str
           the type of node that you want to delete in snake case
        node_uuid: str
           the UUID of the primary node, supporting node, or sub-object
           that you want to delete from the API

        Raises
        ------
        APIError
            If the API responds with anything other than HTTP status 200, then the CRIPT Python SDK raises `APIError`
            `APIError` is raised in case the API cannot delete the specified node.
            Such cases can happen if you do not have permission to delete the node
            or if the node is actively being used elsewhere in CRIPT platform and the API cannot delete it.

        Returns
        -------
        None
        """

        response: Dict = self._capsule_request(url_path=f"/{node_type.lower()}/{node_uuid}/", method="DELETE").json()

        if response["code"] != 200:
            raise APIError(api_error=str(response), http_method="DELETE", api_url=f"/{node_type.lower()}/{node_uuid}/")

        self.logger.info(f"Deleted '{node_type.title()}' with UUID of '{node_uuid}' from CRIPT API.")

    def _capsule_request(self, url_path: str, method: str, api_request: bool = True, timeout: int = _API_TIMEOUT, **kwargs) -> requests.Response:
        """Helper function that capsules every request call we make against the backend.

        Please *always* use this methods instead of `requests` directly.
        We can log all request calls this way, which can help debugging immensely.

        Parameters
        ----------
        url_path:str
          URL path that we want to request from. So every thing that follows api.host. You can omit the api prefix and api version if you use api_request=True they are automatically added.

        method: str
          One of `GET`, `OPTIONS`, `HEAD`, `POST`, `PUT, `PATCH`, or `DELETE` as this will directly passed to `requests.request(...)`. See https://docs.python-requests.org/en/latest/api/ for details.

        headers: Dict
          HTTPS headers to use for the request.
          If None (default) use the once associated with this API object for authentication.

        timeout:int
          Time out to be used for the request call.

        kwargs
          additional keyword arguments that are passed to `request.request`
        """

        url: str = self.host
        if api_request:
            url += f"/{self.api_prefix}/{self.api_version}"
        url += url_path

        pre_log_message: str = f"Requesting {method} from {url}"
        if self.extra_api_log_debug_info:
            pre_log_message += f" from {traceback.format_stack(limit=4)} kwargs {kwargs}"
        pre_log_message += "..."
        self.logger.debug(pre_log_message)

        if self._api_request_session is None:
            raise CRIPTAPIRequiredError
        response: requests.Response = self._api_request_session.request(url=url, method=method, timeout=timeout, **kwargs)
        post_log_message: str = f"Request return with {response.status_code}"
        if self.extra_api_log_debug_info:
            post_log_message += f" {response.text}"
        self.logger.debug(post_log_message)

        return response
