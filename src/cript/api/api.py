import copy
import json
import logging
import os
import re
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Union

import boto3
import requests
from beartype import beartype
from deepdiff import DeepDiff

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
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
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

    # ==========================================================

    @staticmethod
    def remove_keys_from_dict(
        dictionary,
        keys_to_remove=[
            "admin",
            # "uuid",
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

    @classmethod
    def add_to_dict(cls, dictionary, key=None, value=None):
        # Check if the key exists in the dictionary
        if key in dictionary:
            # Check if the value is a list
            if isinstance(value, list):
                # Value is a list, extend the existing list with the new one
                dictionary[key].extend(value)
            else:
                # Value is not a list, append it to the list
                dictionary[key].append(value)
        else:
            # Key does not exist, create a new list with the value
            # If the value is a list, use it directly; otherwise, create a list with one element
            dictionary[key] = value if isinstance(value, list) else [value]

    # ================================== ADD EXISTING NODES-NAMES===================================
    # @staticmethod
    def send_api_patch_existing_nodes_by_name(
        self,
        # parent_node: PrimaryBaseNode,
        parent_node,  # : str,
        parent_uuid,  #: str,
        child_class_type,  #: str,
        existing_child_node_names,  #: list,  # must be list of strings
    ):
        """
        this function will take a list of exact names and add them by uuid
        takes in Parent Node, child class type as a str i.e. "material" or "Material" (either work)

        """

        print("are we here in funktion")

        # child_class_type = child_node.node[0]
        child_class_object = globals().get(child_class_type.capitalize(), None)

        print("child_class_object ", child_class_object)

        # Check if the class exists
        if child_class_object is None:
            # raise ValueError(f"Class {child_class_type} not found")
            return f"Class {child_class_type} not found"

        # go through the list of names and create the payload :
        # parent_node_type = parent_node.node[0].lower()
        url_path = f"/{parent_node}/{parent_uuid}"

        entity_name = f"{child_class_type.lower()}"
        uuid_link_payload = {"node": [parent_node.capitalize()], entity_name: []}

        print("\n hallo")
        print(uuid_link_payload)
        # quit()
        print("existing_child_node_names")
        print(existing_child_node_names[0:2])

        for name in existing_child_node_names:
            # print(name.strip())
            # name = name.strip()
            print("HEREEEE")
            try:
                this = self.search(child_class_object, search_mode=SearchModes.EXACT_NAME, value_to_search=name)
                print(next(this))
            except Exception as e:
                print(e)

            print("---++++++---")
            existing_node = next(self.search(child_class_object, search_mode=SearchModes.EXACT_NAME, value_to_search=name))
            print(existing_node)

            existing_uuid = str(existing_node.uuid)
            print(existing_uuid)

            # parent_node_type = parent_node.node[0].lower()

            print("\n\nuuid_link_payload")
            print(uuid_link_payload)
            # quit()

            API.add_to_dict(uuid_link_payload, key=entity_name, value={"uuid": f"{existing_uuid}"})

        print(" disss uuid_link_payload")
        print(uuid_link_payload)
        # quit()

        patch_response = self._capsule_request(url_path=url_path, method="PATCH", data=json.dumps(uuid_link_payload))

        print("---did this work", patch_response.json())

        return patch_response
        # if patch_response.status_code in [200, 201]:
        #     # print("worked")
        #     # print(patch_response.json())
        #     return patch_response
        # else:
        #     # raise ("error in patching existing item")
        #     return f"error in patching existing item"

    def remove_nodes_by_name(
        self,
        parent_node: PrimaryBaseNode,
        child_class_type: str,
        existing_child_node_names: list,
    ):
        """
        this function will take a list of exact names and add them by uuid
        takes in Parent Node, child class type as a str i.e. "material" or "Material" (either work)

        """

        # child_class_type = child_node.node[0]
        child_class_object = globals().get(child_class_type.capitalize(), None)

        # Check if the class exists
        if child_class_object is None:
            raise ValueError(f"Class {child_class_type} not found")

        # go through the list of names and create the payload :
        parent_node_type = parent_node.node[0].lower()
        url_path = f"/{parent_node_type}/{parent_node.uuid}"

        entity_name = f"{child_class_type.lower()}"
        uuid_link_payload = {"node": parent_node.node, entity_name: []}

        for name in existing_child_node_names:
            # print(name.strip())
            name = name.strip().lower()

            existing_node = next(
                self.search(
                    child_class_object,
                    search_mode=SearchModes.EXACT_NAME,
                    value_to_search=name.strip(),
                )
            )
            existing_uuid = str(existing_node.uuid)

            parent_node_type = parent_node.node[0].lower()

            API.add_to_dict(uuid_link_payload, key=entity_name, value={"uuid": f"{existing_uuid}"})

        del_response = self._capsule_request(url_path=url_path, method="DELETE", data=json.dumps(uuid_link_payload))

        if del_response.status_code in [200, 201]:
            # print("delete worked")
            # print(del_response.json())
            return del_response
        else:
            raise ("error in patching existing item")

    @staticmethod
    def get_value_by_path(data_dict, path_list):
        value = data_dict
        for key in path_list:
            if isinstance(value, dict):
                # Access dictionary
                value = value[key]
            elif isinstance(value, list):
                # Access list
                value = value[int(key)]  # Convert key to int because it's an index in a list
            else:
                # In case the path is invalid or does not correspond to the structure
                raise ValueError("Invalid path or data structure.")
        return value

    # ===========================

    ###########################################################################################
    ###########################################################################################

    @staticmethod
    def build_uuid_map(obj, path=None, uuid_map=None):
        if path is None:
            path = []
        if uuid_map is None:
            uuid_map = {}

        # If the object is a dictionary and has a 'uuid' key, add the path to the map
        if isinstance(obj, dict):
            if "uuid" in obj:
                uuid_map[obj["uuid"]] = path

            for key, value in obj.items():
                new_path = path + [key]
                API.build_uuid_map(value, new_path, uuid_map)

        # If the object is a list or a tuple, iterate over its elements
        elif isinstance(obj, (list, tuple)):
            for index, value in enumerate(obj):
                new_path = path + [index]
                API.build_uuid_map(value, new_path, uuid_map)

        return uuid_map

    ###########################################################################################

    @staticmethod  # OK  pretty good actually - return patches
    def extract_patches(data, cleaned_modified=None):
        parent_node0 = cleaned_modified["node"][0].lower()
        parent_uuid0 = cleaned_modified.get("uuid")  # "123proj456"

        patches = {
            "parent_node": parent_node0,
            "parent_uuid": parent_uuid0,
            "payload_json_patch": {},
        }
        pattern = re.compile(r"root(\['\w+'\]\[\d+\])+\['(\w+)'\]")

        print(
            """this is gonna be a big test ya know where if we get unchanged uuids

            then we need to go into clean modified and just change attributes for it
            this coulda been easier like was a uuid ever mentioned twice ??
            they are either an add or remove, so the values associated
            unchanged_uuids but thats more rigorous
            unchanged_uuids"""
        )

        # ------------------------//-------------------------
        # Handle values_changed first
        if "values_changed" in data:
            for path, change in data["values_changed"].items():
                # patches = {"diff": "values_changed"}
                match = pattern.match(path)
                if match:
                    nested_path = match.group(1)
                    attribute = match.group(2)

                    child_match = re.search(r"\['(\w+)'\]\[(\d+)\]$", nested_path)
                    if child_match:
                        child_node, index_str = child_match.groups()
                        index = int(index_str)  # Convert index to integer

                        # Initialize or update the patch structure
                        if child_node not in patches["payload_json_patch"]:
                            patches["payload_json_patch"][child_node] = [{} for _ in range(index + 1)]
                        elif index >= len(patches["payload_json_patch"][child_node]):
                            patches["payload_json_patch"][child_node].extend([{} for _ in range(index + 1 - len(patches["payload_json_patch"][child_node]))])

                        # Update the specific attribute
                        patches["payload_json_patch"][child_node][index][attribute] = change["new_value"]

                        # Ensure 'node' attribute is present
                        if "node" not in patches["payload_json_patch"][child_node][index]:
                            patches["payload_json_patch"][child_node][index]["node"] = ["Material"]

        # Handle dictionary_item_added for non-indexed additions

        for path in data.get("dictionary_item_added", []):
            tree_path = path.replace("root", "modified")
            print(tree_path)
            # patches = {"diff": "dictionary_item_added"}
            child_entity_match = re.search(r"root\['(\w+)'\]", path)
            if child_entity_match:
                child_node = child_entity_match.group(1)
                tree_path = path.replace("root", "modified")

                # Check if the child_node is in cleaned_modified to add/update it in the patch
                if child_node in cleaned_modified:
                    # patches["payload_json_patch"][child_node].append(cleaned_modified[child_node])
                    API.add_to_dict(patches["payload_json_patch"], "material", cleaned_modified[child_node])
                    # patches["payload_json_patch"].setdefault(child_node, []).append(cleaned_modified[child_node])

        # Handle iterable_item_added
        for path, item in data.get("iterable_item_added", {}).items():
            child_match = re.search(r"root\['(\w+)'\]\[(\d+)\]", path)
            if child_match:
                child_node, index_str = child_match.groups()
                index = int(index_str)

                # Initialize or update the patch structure for the child node
                if child_node not in patches["payload_json_patch"]:
                    patches["payload_json_patch"][child_node] = [{} for _ in range(index + 1)]
                elif index >= len(patches["payload_json_patch"][child_node]):
                    patches["payload_json_patch"][child_node].extend([{} for _ in range(index + 1 - len(patches["payload_json_patch"][child_node]))])

                # Append the new item to the specific child node list
                patches["payload_json_patch"][child_node][index] = item

        return patches

    @staticmethod  # OK  default - return removes
    def extract_removes(data, cleaned_modified=None):
        parent_node0 = cleaned_modified["node"][0].lower()
        parent_uuid0 = cleaned_modified.get("uuid")  # "123proj456"

        removes = {"parent_node": parent_node0, "parent_uuid": parent_uuid0, "payload_json_removes": {}}

        pattern = re.compile(r"root(\['\w+'\]\[\d+\])+\['(\w+)'\]")

        # ----------------------------------------
        data_ = data
        cleaned_modified_ = cleaned_modified

        added_uuids = []
        removed_uuids = []

        """
        # idea is if the uuid was on both the added and removed list then it was not changed but just moved in index
        # and then we would find the uuid in the new tree or where it is a "new value" store that path
        # we need to know if dictionary item removed corresponds to uuid that gets changed, then we will ignore
        # or dictionary item added corresponds to a path of a uuid that gets changed , then we can also ignore and just update the whole node corresponding to uuid

        # but say , if dictionary item added correspond to uuid that are registered as eihter "unchanged" or "unchanged but moved"
        # then we need to handle changing these attributes
        # like if "root['material'][0]['chem_formula']" was removed but
        # root['material'][0]['uuid'] is not found in the keys of values_changed
        """

        # Track UUID changes
        # OK IN EVERY SINGLE ONE ITS

        # in values_changed
        pattern_uuid_change = re.compile(r"root\['(\w+)'\]\[(\d+)\]\['uuid'\]")
        for path, change in data_.get("values_changed", {}).items():
            match = pattern_uuid_change.match(path)
            if match:
                # print(change["old_value"])
                removed_uuids.append(change["old_value"])

                # print(change["new_value"])
                added_uuids.append(change["new_value"])

        # Handle iterable_item_added
        pattern_iterable_item = re.compile(r"root\['(\w+)'\]\[(\d+)\]")
        iterable_items = data_.get("iterable_item_added", {}).items()
        # if isinstance(item, dict):  # Check if the item is a dictionary and has a 'path' key
        for k, v in iterable_items:
            match = pattern_iterable_item.match(k)
            if match:
                # if k matches the regex str
                if "uuid" in v:  # v itself is a dict so if uuid in v
                    added_uuids.append(v["uuid"])

        # Handle iterable_item_removed
        for item in data_.get("iterable_item_removed", []):
            if isinstance(item, dict):  # Check if the item is a dictionary and has a 'path' key
                for k, v in item:
                    if re.match(r"root\['(\w+)'\]\[\d+\]", k):
                        # if k matches the regex str
                        if "uuid" in v:  # v itself is a dict so if uuid in v
                            removed_uuids.append(v["uuid"])

                            # child_node = match.group(1)
                            # # this = {"node":[parent_node0], child_node: [{"uuid": }]
                            this = {"uuid": v["uuid"]}
                            API.add_to_dict(removes["payload_json_removes"], child_node, this)

        # ----------//---------
        # Handle dictionary_item_added
        for item in data_.get("dictionary_item_added", []):
            # if re.match(r"root\['(\w+)'\]", item):
            #     pass # this doesnt take a uuid
            pattern = re.compile(r"root\['(\w+)'\]\[(\d+)\]\['uuid'\]")
            match = pattern.match(item)
            if match:
                # if k matches the regex str
                # if "uuid" in v:  # v itself is a dict so if uuid in v
                add_uuid = cleaned_modified_[match.group(1)][match.group(2)]["uuid"]
                added_uuids.append(add_uuid)

            pattern = re.compile(r"root\['(\w+)'\]")
            match = pattern.match(item)
            if match:
                # if k matches the regex str
                # if "uuid" in v:  # v itself is a dict so if uuid in v

                # add_uuid = cleaned_modified_[match.group(1)][match.group(2)]["uuid"]
                added_entity = cleaned_modified_[match.group(1)]
                if isinstance(added_entity, list):
                    # added_uuids.append(item["uuid"])
                    for node in cleaned_modified_[match.group(1)]:
                        added_uuids.append(node["uuid"])

        # Handle dictionary_item_removed
        for item in data_.get("dictionary_item_removed", []):
            pattern = re.compile(r"root\['(\w+)'\]\[(\d+)\]\['uuid'\]")
            match = pattern.match(item)
            if match:
                # if k matches the regex str
                # if "uuid" in v:  # v itself is a dict so if uuid in v
                rem_uuid = cleaned_modified_[match.group(1)][match.group(2)]["uuid"]
                removed_uuids.append(rem_uuid)
                # COME BACK TO WIP HERE
                child_node = match.group(1)
                # this = {"node":[parent_node0], child_node: [{"uuid": }]
                this = {"uuid": rem_uuid}
                API.add_to_dict(removes["payload_json_removes"], child_node, this)

        # Identify unchanged UUIDs
        unchanged_uuids = set(added_uuids).intersection(removed_uuids)
        # right now we need to test if attributes are there

        # print("removed_uuids and added uuids")
        print("added_uuids")
        print(added_uuids)

        # removes["payload_json_removes"] = removed_uuids
        print("removed_uuids")
        print(removed_uuids)

        return removes

    ###########################################################################################
    @staticmethod
    def generate_patch_removes(dict_obj1, obj2):
        """
        dict_obj1 is the object we map
        obj2 is the object we walk
        here we get the two objects and take a diff
        """
        exclude_regex_paths = [
            # r"root(\[.*\])?\['uuid'\]",
            r"root(\[.*\])?\['uid'\]",
            r"root\['\w+_count'\]",  # All the attributes that end with _count
            r"root(\[.*\])?\['\w+_count'\]",  # All the attributes that end with _count
            r"root(\[.*\])?\['locked'\]",
            r"root(\[.*\])?\['admin'\]",
            r"root(\[.*\])?\['created_at'\]",
            r"root(\[.*\])?\['created_by'\]",
            r"root(\[.*\])?\['updated_at'\]",
            r"root(\[.*\])?\['updated_by'\]",
            r"root(\[.*\])?\['public'\]",
            r"root(\[.*\])?\['notes'\]",
            r"root(\[.*\])?\['model_version'\]",
        ]

        # map of first object
        # uuid_map1 = API.build_uuid_map(obj1)

        print("\n\nobj2 ")
        print(obj2)
        print(type(obj2))

        # print("\n\nobj2 get json ")
        # print(obj2.get_json())
        # print(type(obj2.get_json()))

        print("\n\ndict_obj1")
        print(dict_obj1)
        print(type(dict_obj1))

        print("\n\n********* STARTING EVERYTH ***********")
        # print("basically we know the two are vastly different ")
        # print(" but i think this is working properly and we just need")
        # print(" our two objects to be similar")
        # print("\nwe need to figure out if we can create an object and then  ")
        # print(" send it to the API with a uuid")

        uuid_map1 = API.build_uuid_map(dict_obj1)
        # uuid_map2 = API.build_uuid_map(obj2)
        print("uuid_map1")
        print(uuid_map1)
        # print("uuid_map2")
        # print(uuid_map2)
        # map 2 has no map because its

        print("********** 2 walking the second obj **********")
        # walking the second obj
        for node in obj2:
            node2_uuid = node.uuid

            if node2_uuid not in uuid_map1:
                print("---222situation where this node is not in map")
                print(f"this node: {node2_uuid} was added in a patch to an earleir node so had no comparison")
                continue
            else:  # if in uuid
                # compare "node" and the node from the map
                # node.get_json() and dict_obj1['collection'][0]
                # that would get passed into the shit
                # generate shit
                print(" we got into a map!")

                path = uuid_map1[node2_uuid]
                cleaned_original = API.get_value_by_path(dict_obj1, path)
                cleaned_original = API.remove_keys_from_dict(cleaned_original)

                # cleaned_modified = node.get_json().json
                # print(cleaned_modified)

                modified = json.loads(node.get_json().json)  # Assuming this is already a dictionary

                # cleaned_original = self.remove_keys_from_dict(original)
                cleaned_modified = API.remove_keys_from_dict(modified)

                diff_ = DeepDiff(cleaned_original, cleaned_modified, exclude_regex_paths=exclude_regex_paths)  # ignore_order=True, group_by = id)
                diff_dict = diff_.to_dict()

                # print("\ncleaned_original")
                # print(cleaned_original)
                # print("\ncleaned_original keys")
                # print(cleaned_original.keys())

                # print("\ncleaned_modified")
                # print(cleaned_modified)
                # print("\ncleaned_modified keys")
                # print(cleaned_modified.keys())

                print("diff_dict")
                print(diff_dict)

                data = dict(diff_dict)
                print("*0o0o0o0o*******************")
                # print("data")
                # print(data)
                if data:
                    # print("data")
                    # print(data)
                    patches = API.extract_patches(data, cleaned_modified=cleaned_modified)
                    print(patches)
                    print(" 5555patches WE ARE HERE \n\n\n ------")

                    removes = API.extract_removes(data, cleaned_modified=cleaned_modified)
                    print(removes)
                    print(" 5555removes WE ARE HERE \n\n\n ------")

                    print("\n we should do a groupby on the removes and patches ")

                    data = [patches, removes]

                    grouped_data = {}

                    for item in data:
                        parent_node0 = item["parent_node"]
                        parent_uuid0 = item["parent_uuid"]
                        key = (parent_node0, parent_uuid0)
                        if key not in grouped_data:
                            grouped_data[key] = {"parent_node": parent_node0, "parent_uuid": parent_uuid0, "payload_json_patch": {}, "payload_json_removes": {}}

                        if "payload_json_patch" in item:
                            grouped_data[key]["payload_json_patch"].update(item["payload_json_patch"])
                        if "payload_json_removes" in item:
                            grouped_data[key]["payload_json_removes"].update(item["payload_json_removes"])

                    # Since we know there is only one group in this example, we can directly transform it to the desired output
                    final_data = next(iter(grouped_data.values()))

                    # return the final structure
                    return final_data

        # print("********************")

        # uuid_map1 = API.build_uuid_map(obj1)
        # uuid_map2 = API.build_uuid_map(obj2)
        # print("uuid_map1")
        # print(uuid_map1)
        # print("uuid_map2")
        # print(uuid_map2)

        quit()

        node1 = dict_obj1[path]

        diff_ = DeepDiff(node1, node, exclude_regex_paths=exclude_regex_paths)  # ignore_order=True, group_by = id)
        diff_dict = diff_.to_dict()

    ###########################################################################################

    # @staticmethod
    def send_patches_to_api(self, list_of_patches_and_removes, link_existing=True):  # can toggle this
        # payload_remove = entities_to_remove_dict  # remove_list
        # payload_patch = entities_to_patch_dict

        # print("\n\n____payload_patch_remove")
        # print(payload_remove)

        # print("\n____payload_patch_add")
        # print(payload_patch)
        """
        here we go through the list of patches and removes and send them to the API
        from last to first in the order they were registered

        we got into a SENDPATCH"]
        list_of_patches_and_removes
        we want to go through the bottom first"
        and we go through patches for each node first, then removes for each node
        """
        for item in reversed(list_of_patches_and_removes):
            parent_node0 = item["parent_node"]
            parent_uuid0 = item["parent_uuid"]
            url_path = f"/{parent_node0}/{parent_uuid0}"
            payload_patch = item["payload_json_patch"]
            print(url_path)
            print("payload_patch", json.dumps(payload_patch))
            API.add_to_dict(payload_patch, "node", [parent_node0.capitalize()])
            print("payload_patch2", json.dumps(payload_patch))
            try:
                patch_response = self._capsule_request(url_path=url_path, method="PATCH", data=json.dumps(payload_patch))  # json.dumps(payload_patch))
                print(patch_response.json())
                if patch_response.status_code in [400, 409]:
                    print("""take the things that exist and link it , then resend the other materials""")

                    if link_existing is True:
                        print(patch_response.json())
                        print(patch_response.json().get("error"))

                        child_class_type = patch_response.json().get("error").split("names")[1].split("in")[1].strip().lower()
                        text = patch_response.json().get("error")

                        print("this needs to be refactored with regex also eval needs to be ast lietral")

                        # Regex pattern to match anything inside square brackets
                        pattern = r"\[.*?\]"

                        # Using re.search() to find the first occurrence of the pattern in the text
                        match = re.search(pattern, text)

                        # Extracting the matched content if found
                        if match:
                            matched_content = match.group(0)
                            print("Found content:", matched_content)
                            matched_content = matched_content.replace("'", '"')
                            # eval_names = eval(matched_content.strip())
                            # print(eval_names)
                            # names_list = [name["name"].lower() for name in eval_names]
                            names_list = json.loads(matched_content)
                            print("names_list")
                            for item in names_list:
                                print(item)
                        else:
                            print("No match found")

                        # quit()
                        # names_list_of_dicts = patch_response.json().get("error").split("names")[1].split("in")[0]

                        # child_class_type = patch_response.json().get("error").split("names")[1].split("in")[1].strip().lower()

                        # print(child_class_type)
                        # print("-----//-----")

                        # eval_names = eval(names_list_of_dicts)
                        # print(eval_names)
                        # names_list = [name["name"].lower() for name in eval_names]
                        # print("names_list")

                        if names_list:
                            # print("we are about to send")
                            # print(parent_node0)
                            # print(parent_uuid0)
                            # print(child_class_type)
                            # print(names_list)

                            link_response = self.send_api_patch_existing_nodes_by_name(  # self.send_api_patch_existing_nodes_by_name(
                                parent_node=parent_node0,
                                parent_uuid=parent_uuid0,
                                child_class_type=child_class_type,
                                existing_child_node_names=names_list,
                            )
                            # print("---link_response")
                            # print(link_response)

                            # need to retry for collection
                            payload_patch.pop(child_class_type)  # we just sent the stuff to api above so now pop it off the resposne
                            retry_patch_response2 = self._capsule_request(url_path=url_path, method="PATCH", data=json.dumps(payload_patch))
                            # retry_patch_json = retry_patch_response2.json()

                            print("\n\n___retry_patch_response2")
                            print(retry_patch_response2.json())
                            # maybe return now - NO because of removal
                            # if retry_patch_response2.status_code in [200, 201]:
                            #     return

                if patch_response.status_code in [200]:
                    print("got 200")

            except:
                print("could not add nor retry")
                pass

        for item in reversed(list_of_patches_and_removes):
            url_path = f"/{parent_node0}/{parent_uuid0}"
            payload_removes = item["payload_json_removes"]
            print("payload_removes")
            print(payload_removes)
            if payload_removes != {}:
                try:
                    # payload_remove needs --- {"node": new_node.node}:
                    API.add_to_dict(payload_removes, key="node", value=[parent_node0.capitalize()])
                    remove_response = self._capsule_request(url_path=url_path, method="PATCH", data=json.dumps(payload_removes))
                    print("remove_response")
                    print(remove_response)
                except:
                    print("could not remove")
                    pass

    # basically I need to write tests for it now ...

    ###########################################################################################
    # """
    # ok the way this would work is if I would take in two objects ,
    #  - first i map put the paths of the first object, all uuids
    #  - then I iterate of all uuids in the second object (I'm walking here)
    #  - then with each uuid I encounter in the second walker node
    #  - i find up in the lookup table and do a compare on that as the root , right ?
    #     - basically that path would be the spot to get to in the object
    #     - and i would record the patches and removes on each node
    #     - I guess I could log it all to a list and maybe eventually do a group by on it

    #  - if I don't find the uuid in the lookup table then it was added
    #  - also I would need to make sure theres "visited" aspect in the iterator
    #  - also since this object is just a map , it doesnt matter the order
    #  - we will still probably get it in DFS because thats how iterator is

    # """
    def save_node(self, new_node: PrimaryBaseNode, link_existing=True):
        # ================trying
        list_of_patches_and_removes = []

        node_type = new_node.node_type.lower()
        # print("---ARE WE HERE")

        # try to get or else create
        try:
            # print("---ARE WE HERE1")
            # node_type = new_node.node[0].lower()
            get_url = f"/{node_type}/{new_node.uuid}"
            # print("get_url---", get_url)
            # quit()
            try:
                original = self._capsule_request(url_path=get_url, method="GET").json()
                original = original["data"][0]
                # print("----", original)
                # print("\noriginal 1: ", original)

            except Exception as e:  # except if we could not load by uuid
                original = None
                # raise ValueError(f"No data available in response {response}")

                if node_type == "project":  # only project node is name unique
                    klass = globals().get(node_type.capitalize(), None)

                    # i think this should be next()
                    # existing_uuid = next(self.search(node_type=klass, search_mode=SearchModes.EXACT_NAME, value_to_search=new_node.name))  # "return uuid with next"  # self.object_exists(node=node_type, name=new_node.name):

                    paginator = self.search(node_type=klass, search_mode=SearchModes.EXACT_NAME, value_to_search=new_node.name)  # value["name"])
                    # paginator.auto_load_nodes = False
                    klass_json = next(paginator)

                    # print("22222new_node name", new_node.name)
                    # no results, great !
                    # print("existing_uuid", klass_json)

                    if (original is None) and klass_json:
                        # print("original node and bla bla")
                        # print("should we get the object with name from other uuid?")

                        raise ValueError("this name already exists stored under a different uuid")

        except Exception as e:
            # print("---ARE WE HERE 2")
            # no uuid or name match on project, make a new one
            if node_type == "project":  # all other nodes must already exist
                # i think we need to pass in "new_node.json" and i'm not sure why this seems like old code

                # data = {
                #     "node": new_node.node,
                #     "name": new_node.name,
                # }  # , "material": [{"node": ["Material"], "name": Config.material_name}]}  # , "public": Config.is_public}

                data = new_node.get_json().json
                # print("-------")
                # print(type(data))
                # print("---lodz-data---")
                # print(type(json.loads(data)))
                data0 = API.remove_keys_from_dict(json.loads(data))
                data = json.dumps(data0)
                print(data)
                print(type(data))
                # quit()

                response = self._capsule_request(url_path="/project/", method="POST", data=data)  # json.dumps(data))
                if response.json()["code"] in [400]:
                    # print("---0-data---")
                    # print(type(json.loads(data)))
                    # data = API.remove_keys_from_dict(json.loads(data))
                    # print(data)
                    # raise ValueError(f"malformed json data - check string into dumps{response.json()}")
                    print("\nmalformed json data - check string into dumps", response.json())
                    quit()
                elif response.json()["code"] in [409]:
                    print("already exists", response.json())
                elif response.json()["code"] in [401]:
                    print("signature", response.json())
                    return
                elif response.json()["code"] == 200:
                    print("we created a project!")
                    original_dict = response.json()["data"]["result"][0]
                    original = original_dict
                    # print("\noriginal 2: ", original)
                    # print("returning now.\n\n")
                    # we created a new node,
                    # asserted it was created, now we can return
                    return

            else:
                # this would have been fetched above for a non project node
                print(f"couldn't create or fetch data for {new_node.node}")

        ####################################

        # modified = json.loads(new_node.get_json().json)  # Assuming this is already a dictionary

        cleaned_original = self.remove_keys_from_dict(original)
        # cleaned_modified = self.remove_keys_from_dict(modified)

        # modified stuff gets handled inside patch remove

        # here we can probably do a function generate patch_removes

        #  generate_patch_removes
        patch_removes = API.generate_patch_removes(cleaned_original, new_node)  # cleaned_modified)
        print("patch_removes")
        print(patch_removes)
        print(" now we append patch removes to a list ")
        print(" then at the end we will do the patch removes by last first ")
        # API.send_patch_removes()

        list_of_patches_and_removes.append(patch_removes)

        # so thats just for generating the patch removes for a node
        # then we will send all these and thats where we will have a flag for link existing

        self.send_patches_to_api(list_of_patches_and_removes=list_of_patches_and_removes, link_existing=link_existing)

        return get_url

    ###########################################################################################
    ###########################################################################################

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
