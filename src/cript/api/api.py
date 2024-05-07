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
from deepdiff import DeepDiff

import cript.nodes.primary_nodes as PrimaryNodes
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
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.project import Project
from cript.nodes.util import load_nodes_from_json

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


class LastModifiedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order = list(self.keys())

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

    def keys_sorted_by_last_modified(self):
        order = []
        for key in self._order:
            if key in self:
                order.append(key)
        return order


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

    @staticmethod
    def remove_keys_from_dict(
        dictionary,
        keys_to_remove=[
            "admin",
            "uuid",
            "updated_by",
            "created_by",
            "member",
            "experiment_count",
            "inventory_count",
            "public",
            "created_at",
            "email",
            "model_version",
            "orcid",
            "uid",
            "updated_at",
            "username",
            "admin_count",
            "collection_count",
            "locked",
            "material_count",
            "member_count",
            "component_count",
            "computational_forcefield_count",
            "identifier_count",
            "computation_count",
            "component_count",
            "citation_count",
            "condition_count",
            "sample_preparation_count",
            "property_count",
        ],
    ):
        """Recursively remove keys from a dictionary."""
        if not isinstance(dictionary, dict):
            return dictionary
        for key in keys_to_remove:
            dictionary.pop(key, None)
        for key, value in list(dictionary.items()):  # Use list() to avoid RuntimeError during iteration
            if isinstance(value, dict):
                API.remove_keys_from_dict(value, keys_to_remove)
            elif isinstance(value, list):
                for item in value:
                    API.remove_keys_from_dict(item, keys_to_remove)
        return dictionary

    @staticmethod
    def rearrange_materials(data):
        if type(data) != dict:
            data = json.loads(data)
        # Extract UID references from the top-level material key
        original_materials = data.get("material", [])
        uid_refs = {mat["uid"]: {} for mat in original_materials}

        # Helper function to replace material details and collect those details
        def process_node(node):
            if isinstance(node, dict):
                for key, value in list(node.items()):
                    if key == "material" and "uid" in value and value["uid"] in uid_refs:
                        # Copy the full material details to the corresponding UID entry in uid_refs
                        uid_refs[value["uid"]].update(value)
                        # Replace the material entry with uid-only
                        node[key] = {"uid": value["uid"]}
                    else:
                        process_node(value)
            elif isinstance(node, list):
                for item in node:
                    process_node(item)

        # Process the data starting from the top-level 'node' if it matches 'Project'
        if "node" in data and data["node"][0] == "Project":
            process_node(data)

        # Update the top-level material list with the detailed information collected
        updated_materials = [details for details in uid_refs.values() if details]
        # Ensure material list is never empty; revert to original if no updates found
        data["material"] = updated_materials if updated_materials else original_materials
        return data

    @staticmethod
    def extract_differences(new_data, old_data):
        if isinstance(new_data, dict) and isinstance(old_data, dict):
            diff = {}
            for key in new_data:
                if key in old_data:
                    if isinstance(new_data[key], (dict, list)) and isinstance(old_data[key], (dict, list)):
                        result = API.extract_differences(new_data[key], old_data[key])
                        if result:
                            diff[key] = result
                    elif new_data[key] != old_data[key]:
                        diff[key] = new_data[key]
                else:
                    diff[key] = new_data[key]
            return diff
        elif isinstance(new_data, list) and isinstance(old_data, list):
            # Assuming lists are of dicts which are records that need full comparison
            diff = []
            for item in new_data:
                # Find an item in old_data that matches based on a deep comparison
                matched_item = next((subitem for subitem in old_data if API.extract_differences(item, subitem) == {}), None)
                if not matched_item:
                    diff.append(item)
            return diff
        return new_data if new_data != old_data else {}

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

    # _no_condense_uuid is either active or not
    def save(self, new_node):
        self._internal_save(new_node, _no_condense_uuid=True)

        self._internal_save(new_node, _no_condense_uuid=False)

        print(new_node)

    def _internal_save(self, new_node: PrimaryBaseNode, _no_condense_uuid: bool) -> None:
        data = new_node.get_json(_no_condense_uuid=_no_condense_uuid).json

        data = json.dumps(data)

        node_class_name = new_node.node_type.capitalize()
        NodeClass = getattr(PrimaryNodes, node_class_name)

        """
        on the second time around, shouldn't it be picked up here 
        therefore not get to theStopIteration Exception below ?
        """

        old_node_paginator = self.search(node_type=NodeClass, search_mode=SearchModes.UUID, value_to_search=str(new_node.uuid))
        old_node_paginator.auto_load_nodes = False

        try:
            old_node_json = next(old_node_paginator)

        except StopIteration:  # New Project do POST instead
            # Do the POST request call. only on project
            # or else its a patch handled by previous node

            if new_node.node_type.lower() == "project":
                data = new_node.get_json(_no_condense_uuid=_no_condense_uuid).json

                # tried this, doesnt work
                data = API.rearrange_materials(data)

                print(data)
                """
                if there is an outter node , make sure the outter one is the full node and the inner node is the uuid 
                def rearrange_uuid:
                search where the uuid exists , make sure the full node is the 
                """

                data = json.dumps(data)

                response = self._capsule_request(url_path="/project/", method="POST", data=data)

                if response.status_code in [200, 201]:
                    """
                    try returning a true vs false kinda thing to see if we need to do "internal save" again
                    """
                    return  # Return here, since we successfully Posting,

                else:  # debug for now
                    res = response.json()

                    raise Exception(f"APIError {res}")

        old_project, old_uuid_map = load_nodes_from_json(nodes_json=old_node_json, _use_uuid_cache={})

        if new_node.deep_equal(old_project):
            return  # No save necessary, since nothing changed

        delete_uuid = []

        master_delete_uuid_dict = {}

        patch_map = LastModifiedDict()

        # Iterate the new project in DFS
        for node in new_node:
            try:
                old_node = old_uuid_map[node.uuid]
            except KeyError:
                print("key error but passing ?")
                # This node only exists in the new new project,
                # But it has a parent which patches it in, so no action needed
                pass

            # do we need to delete any children, that existed in the old node, but don't exit in the new node.

            # node.find_children that means node is the parent !!
            # just search depth = 1
            node_child_map = {child.uuid: child for child in node.find_children({}, search_depth=1)}

            old_child_map = {child.uuid: child for child in old_node.find_children({}, search_depth=1)}

            for old_uuid in old_child_map:
                # need to keep track of node type I think

                if old_uuid not in node_child_map:
                    if old_uuid not in delete_uuid:
                        delete_uuid += [old_uuid]  # we wanna delete old_uuid

                        del_node_type = old_child_map[old_uuid].node_type_snake_case

                        # node is the parent
                        parent_node_type = node.node_type.capitalize()
                        parent_node_uuid = node.uuid
                        url_parent = f"/{parent_node_type.lower()}/{parent_node_uuid}"

                        if del_node_type.lower() != "user":
                            # key will be the edge to remove,
                            # value will be the immediate parent node url

                            if url_parent not in master_delete_uuid_dict:
                                # Create a new empty data dictionary if not present
                                master_delete_uuid_dict[url_parent] = {"node": [parent_node_type]}  # Initialize with the node type

                            # Reference the data dictionary for this URL
                            data = master_delete_uuid_dict[url_parent]

                            # Check if the del_node_type exists in the data dictionary
                            if del_node_type in data:
                                # Append a new UUID dictionary to existing list
                                data[del_node_type].append({"uuid": old_uuid})
                            else:
                                # Create a new key with a list containing the UUID dictionary
                                data[del_node_type] = [{"uuid": old_uuid}]

                            master_delete_uuid_dict[url_parent] = data

            # check if the current new node needs a patch

            if not node.shallow_equal(old_node):
                patch_map[node.uuid] = node

        for uuid_ in reversed(patch_map.keys_sorted_by_last_modified()):
            """
            so , i think for example, we are comparing some nodes where just the _uid is different
            maybe need to implement deep diff and ignore _uid
            """

            node = patch_map[uuid_]

            child_known_uuids = list(patch_map.keys())

            child_known_uuids.remove(str(node.uuid))

            url_path = f"/{node.node_type_snake_case}/{node.uuid}"

            data = node.get_json(is_patch=True).json

            try:
                old_node = old_uuid_map[node.uuid]
            except KeyError:
                pass

            #############
            if _no_condense_uuid:  # first case
                node_dict = json.loads(node.get_json(is_patch=True).json)

                old_node_dict = json.loads(old_node.get_json(is_patch=True).json)

            else:
                node_dict = json.loads(node.get_json(is_patch=True, known_uuid=child_known_uuids).json)

                old_node_dict = json.loads(old_node.get_json(is_patch=True, known_uuid=child_known_uuids).json)

            # Extract differences
            data_diff = API.extract_differences(node_dict, old_node_dict)

            if data_diff != {}:
                # add node back here
                data_diff["node"] = node_dict["node"]
                print("data_diff_inside")
                print(data_diff)
                res = self._capsule_request(url_path=url_path, method="PATCH", data=json.dumps(data_diff))  # maybe dumps or load

            """
            make a clause where if we do the diff and it does or doesn't make sense (i.e. like just _uid as difference)
            then ... we gotta ya know
            thats why deep diff might be worth it 
            """

        for key, value in master_delete_uuid_dict.items():
            url_path = key
            unlink_payload = value
            res = self._capsule_request(url_path=url_path, method="DELETE", data=json.dumps(unlink_payload))
            if res.status_code in [200]:
                print("\n we_deleted_nodes!")
        ################################################################################

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
        page_number: Union[int, None] = None

        if search_mode == SearchModes.NODE_TYPE:
            api_endpoint = f"/search/{node_type}"
            page_number = 0

        elif search_mode == SearchModes.CONTAINS_NAME:
            api_endpoint = f"/search/{node_type}"
            page_number = 0

        elif search_mode == SearchModes.EXACT_NAME:
            api_endpoint = f"/search/exact/{node_type}"
            page_number = None

        elif search_mode == SearchModes.UUID:
            api_endpoint = f"/{node_type}/{value_to_search}"
            # putting the value_to_search in the URL instead of a query
            value_to_search = ""
            page_number = None

        elif search_mode == SearchModes.BIGSMILES:
            api_endpoint = "/search/bigsmiles/"
            page_number = 0

        # error handling if none of the API endpoints got hit
        else:
            raise RuntimeError("Internal Error: Failed to recognize any search modes. Please report this bug on https://github.com/C-Accel-CRIPT/Python-SDK/issues.")

        return Paginator(api=self, url_path=api_endpoint, page_number=page_number, query=value_to_search)

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
