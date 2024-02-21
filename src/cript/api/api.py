import copy
import json
import logging
import os
import uuid
import warnings
from pathlib import Path
from typing import Any, Dict, Optional, Union
from deepdiff import DeepDiff
import cript

# from deepdiff import DeepDiff

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
    InvalidHostError,
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
from cript.nodes.core import BaseNode


# Do not use this directly! That includes devs.
# Use the `_get_global_cached_api for access.
_global_cached_api = None


# load from .env
class Config:
    host = os.getenv("HOST")
    api_token = os.getenv("API_KEY")
    storage_token = os.getenv("STORAGE_KEY")
    object_name0 = "P2"
    object_name = "try444"  # "project0110"  # "P2A3DAA"
    is_public = False  # True


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
    _verbose: bool = True
    logger: logging.Logger = None  # type: ignore

    _host: str = ""
    _api_token: str = ""
    _storage_token: str = ""
    _http_headers: dict = {}
    _db_schema: Optional[DataSchema] = None
    _api_prefix: str = "api"
    _api_version: str = "v1"

    # trunk-ignore-begin(cspell)
    # AWS S3 constants
    _REGION_NAME: str = "us-east-1"
    _IDENTITY_POOL_ID: str = "us-east-1:9426df38-994a-4191-86ce-3cb0ce8ac84d"
    _COGNITO_LOGIN_PROVIDER: str = "cognito-idp.us-east-1.amazonaws.com/us-east-1_SZGBXPl2j"
    _BUCKET_NAME: str = "cript-user-data"
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

        self._host = self._prepare_host(host=host)  # type: ignore
        self._api_token = api_token  # type: ignore
        self._storage_token = storage_token  # type: ignore

        # add Bearer to token for HTTP requests
        self._http_headers = {"Authorization": f"Bearer {self._api_token}", "Content-Type": "application/json"}

        # check that api can connect to CRIPT with host and token
        self._check_initial_host_connection()

        # set a logger instance to use for the class logs
        self._set_logger()
        self._db_schema = DataSchema(self.host)

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
        CRIPT API Client - Host URL: 'https://api.criptapp.org/api/v1'

        Returns
        -------
        str
        """
        return f"CRIPT API Client - Host URL: '{self.host}'"

    def _set_logger(self, verbose: bool = True) -> None:
        """
        Prepare and configure the logger for the API class.

        This function creates and configures a logger instance associated with the current module (class).

        Parameters
        ----------
        verbose: bool default True
            set if you want `cript.API` to give logs to console or not

        Returns
        -------
        logging.Logger
            The configured logger instance.
        """
        # Create a logger instance associated with the current module
        logger = logging.getLogger(__name__)

        # Set the logger's level based on the verbose flag
        if verbose:
            logger.setLevel(logging.INFO)  # Display INFO logs
        else:
            logger.setLevel(logging.CRITICAL)  # Display no logs

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Create a formatter for log messages (customize the format as desired)
        formatter = logging.Formatter("%(levelname)s: %(message)s")

        # Associate the formatter with the console handler
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        # set logger for the class
        self.logger = logger

    @property
    def verbose(self) -> bool:
        """
        A boolean flag that controls whether verbose logging is enabled or not.

        When `verbose` is set to `True`, the class will provide additional detailed logging
        to the terminal. This can be useful for debugging and understanding the internal
        workings of the class.

        ```bash
        INFO: Validating Project graph...
        ```

        When `verbose` is set to `False`, the class will only provide essential logging information,
        making the terminal output less cluttered and more user-friendly.

        Examples
        --------
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...     # turn off the terminal logs
        ...     api.verbose = False

        Returns
        -------
        bool
            verbose boolean value
        """
        return self._verbose

    @verbose.setter
    def verbose(self, new_verbose_value: bool) -> None:
        """
        sets the verbose value and then sets a new logger for the class

        Parameters
        ----------
        new_verbose_value: bool
            new verbose value to turn the logging ON or OFF

        Returns
        -------
        None
        """
        self._verbose = new_verbose_value
        self._set_logger(verbose=new_verbose_value)

    @beartype
    def _prepare_host(self, host: str) -> str:
        """
        Takes the host URL provided by the user during API object construction (e.g., `https://api.criptapp.org`)
        and standardizes it for internal use. Performs any required string manipulation to ensure uniformity.

        Parameters
        ----------
        host: str
            The host URL specified during API initialization, typically in the form `https://api.criptapp.org`.

        Warnings
        --------
        If the specified host uses the unsafe "http://" protocol, a warning will be raised to consider using HTTPS.

        Raises
        ------
        InvalidHostError
            If the host string does not start with either "http" or "https", an InvalidHostError will be raised.
            Only HTTP protocol is acceptable at this time.

        Returns
        -------
        str
            A standardized host string formatted for internal use.

        """
        # strip ending slash to make host always uniform
        host = host.rstrip("/")
        host = f"{host}/{self._api_prefix}/{self._api_version}"

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
        https://api.criptapp.org/api/v1
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

    # ================ helpers ==============
    @classmethod
    def object_exists(cls, node: str, name: str):
        host = Config.host
        token = Config.api_token

        # FOR NOW : hard code brilis proj name
        # object_name = "P2A3DAA" # not used

        api_url = f"{host}/api/v1/search/exact/{node}/?q={name}"  # Ensure this URL lists all objects of the type
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.get(api_url, headers=headers)

            data = response.json()["data"]
            print("\nlength should be 1: ", len(data.get("result")))

            if len(data.get("result")) == 1:
                item = data.get("result")[0]

                return True, item.get("uuid")

            return False, None

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return False, None

    @staticmethod
    def fetch_object_data(object_type: str, uuid: str):
        host = Config.host
        token = Config.api_token
        get_url = f"{host}/api/v1/{object_type.lower()}/{uuid}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()
        if response.json()["data"]:
            return response.json()["data"][0]  # Assuming the first item is the desired one
        else:
            return "Error"  # Consider raising an exception or returning None instead

    @classmethod
    def get_or_create(cls, node: str, name: str, parent_uuid: str = "", parent_node_type: str = "", is_public=Config.is_public, **kwargs):
        host = Config.host
        token = Config.api_token

        if hasattr(cript, node.capitalize()):
            node_class = getattr(cript, node.capitalize())

            object_exists, uuid = cls.object_exists(node=node, name=name)

            print("----\n  print object_exists, uuid ??")
            print(object_exists, uuid)

            if object_exists:
                print(f"Object exists, fetching data for {node} with UUID: {uuid}")
                node_data = cls.fetch_object_data(node, uuid)
                # print(f"Fetched data for {node}: {node_data}")

                # Define the list of child node types
                child_node_list = [
                    "collection",
                    "material",
                    "property",
                    "process",
                    # Add other node types as needed
                ]

                for key in child_node_list:
                    if key in node_data:
                        if isinstance(node_data[key], list) and all(isinstance(item, dict) for item in node_data[key]):
                            # All items are dictionaries, proceed with instantiation
                            child_class_name = key.capitalize()
                            child_class = getattr(cript, child_class_name, None)
                            if child_class:
                                node_data[key] = [child_class._from_json(item) for item in node_data[key]]
                            else:
                                print(f"Warning: Child class {child_class_name} not found for key {key}.")
                        elif all(isinstance(item, cript.nodes.primary_nodes.material.Material) for item in node_data[key]):
                            # Items are already instances of Material, no action needed
                            print(f"Info: {key} already contains instantiated objects.")
                        else:
                            # Mixed or unexpected types, handle accordingly
                            print(f"Warning: Unexpected data format for {key}.")

                # Use the dynamically updated node_data to instantiate the node using its _from_json method
                return node_class._from_json(node_data)

            else:
                print(f"Object does not exist, creating {node} named {name} ...now will create .... do a post and then fetch")

                if node == "project":
                    url = f"{host}/api/v1/{node}"
                    data = {"node": [node.capitalize()], "name": name, "public": is_public}
                    data.update(kwargs)

                    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

                    response = requests.post(url, json=data, headers=headers)
                    print("++++ ::::: response")
                    print(response.json())

                    if response.status_code == 200:  # response for us when created
                        print("---here here")
                        uuid = response.json()["data"]["result"][0].get("uuid")
                        node_data = cls.fetch_object_data(node, uuid)

                        return node_class(**node_data)  # , **kwargs)
                else:
                    api_url = f"{host}/api/v1/{parent_node_type}/{parent_uuid}"  # Ensure this URL lists all objects of the type
                    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

                    data = {"node": [f"{parent_node_type.capitalize()}"], f"{node.lower()}": [{"node": [f"{node.capitalize()}"], "name": f"{name}"}]}  # probably luss kwargs

                    print(data)

                    try:
                        response = requests.patch(
                            api_url,
                            json=data,
                            headers=headers,
                        )

                        response.raise_for_status()
                        res = response.json()
                        data = response.json()["data"]

                        if response.status_code == 200:  # response for us when created
                            print("---star star")
                            uuid = response.json()["data"]["result"][0].get("uuid")
                            return node_class(**node_data)  # , **kwargs)

                    except Exception as e:
                        print("here4444")
                        print(e)

        else:
            raise ValueError(f"Invalid node type: {node}")

    @staticmethod
    def load_schema_for_node_type(node_type):
        """
        Load the validation schema for a given node type.

        Args:
            node_type (str): The type of the node (e.g., 'Project', 'Material').

        Returns:
            dict: The loaded schema.
        """
        schema_file_path = f"src/cript/schemas/{node_type.lower()}_schema.json"  # Path to the schema file
        try:
            with open(schema_file_path, "r") as file:
                schema = json.load(file)
            return schema
        except FileNotFoundError:
            print(f"Schema file not found for node type: {node_type}")

        except json.JSONDecodeError:
            print(f"Invalid JSON format in schema file for node type: {node_type}")

    @staticmethod
    def remove_keys_from_dict(
        dictionary,
        keys_to_remove=["uuid", "experiment_count", "inventory_count", "public", "created_at", "email", "model_version", "orcid", "uid", "updated_at", "username", "admin_count", "collection_count", "locked", "material_count", "member_count"],
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
    def remove_duplicates(node_objects, duplicate_list):
        removed_items = []  # To store removed materials
        remaining_items = []  # To store remaining materials after removal

        for item in node_objects:
            if item["name"] in duplicate_list:
                removed_items.append(item)
            else:
                remaining_items.append(item)

        return remaining_items

    @staticmethod
    def send_patch_request_for_entity(parent_node=None, payload=None):  # (self, base_url, entity_uuid, data, auth_token=None):
        """
        Sends a PATCH request to update an entity.
        """

        base_url = Config.host
        parent_uuid = parent_node.uuid
        url = f"{base_url}/api/v1/project/{parent_uuid}"  # if entity_uuid else base_url

        headers = {
            "Content-Type": "application/json",
        }

        headers["Authorization"] = f"Bearer {Config.api_token}"

        data = payload

        # print(data)

        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Entity updated successfully.")
        else:
            print(f"Entity updated Failed. Status code: {response.status_code}, Response: {response.text}")

        return response

    @staticmethod
    def find_uuid_by_name_and_type(self, name, node_type):
        """
        Queries the system to find the UUID of an entity based on its name and type.

        Args:
            name (str): The name of the entity.
            type (str): The type of the entity (e.g., 'Material').

        Returns:
            str: The UUID of the entity if found, None otherwise.
        """
        base_url = "https://lb-stage.mycriptapp.org/api/v1"
        # Adjust the URL construction to fit the required format
        print(name)
        # name = name.strip().replace(" ", "+")
        name = name.strip().replace(" ", "%20")
        print(name)
        print("^^---^^^")
        print(node_type)
        print("-----====")

        search_url = f"{base_url}/search/exact/{node_type.lower()}/?q={name}"
        headers = {
            "Authorization": f"Bearer {Config.api_token}",  # Use your actual API token
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError if the response was an error

            # Assuming the API returns a JSON response with entities, and you're interested in the first one
            found_node = response.json()
            if found_node:
                if found_node["data"]["result"]:
                    print(len(found_node["data"]["result"]))
                    return found_node["data"]["result"][0]["uuid"]
                else:
                    print("No results found")

            else:
                print(f"Error querying UUID for name '{name}' and type '{node_type}': {e}")
                return None
        except requests.RequestException as e:
            print(f"Error querying UUID for name '{name}' and type '{node_type}': {e}")
            return None

    # ================= SAVE ==================
    @classmethod
    def save_node(self, new_node: PrimaryBaseNode):
        original = self.fetch_object_data(new_node.node_type, new_node.uuid)

        modified = json.loads(new_node.get_json().json)  # Assuming this is already a dictionary

        cleaned_original = self.remove_keys_from_dict(original)
        cleaned_modified = self.remove_keys_from_dict(modified)

        exclude_regex_paths = [
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

        diff0 = DeepDiff(
            cleaned_original,
            cleaned_modified,
            exclude_regex_paths=exclude_regex_paths,
            ignore_order=True,
        )
        diff_dict = diff0.to_dict()

        print("----diff_dict")
        print(diff_dict)
        quit()

        try:
            dictionary_items_added = diff_dict.get("dictionary_item_added", {})  # probably need to be values changed
            values_changed = diff_dict.get("values_changed", {})
            iterable_items_added = diff_dict.get("iterable_item_added", {})
            iterable_items_removed = diff_dict.get("iterable_item_removed", {})

        except Exception as e:
            print(e)

        # 0) REMOVE ITEMS ADDED - UNLINKING

        entities_to_remove_dict = {}
        print("------iterable_items_removed/values_changed-------")
        print(values_changed)
        print(iterable_items_removed)

        for key, value in iterable_items_removed.items():
            # Use split to parse out the entity name from the key
            try:
                entity_name = key.split("['")[1].split("']")[0]
                # print("\nhere return uuid based off of node and name")
                # print(value)

            except IndexError:
                entity_name = None

            # Proceed with the rest of the logic as before
            if entity_name:
                if entity_name not in entities_to_remove_dict:
                    # value['name'], value['node']
                    uuid = new_node.find_uuid_by_name_and_type(value["name"], value["node"][0].lower())
                    entities_to_remove_dict[entity_name] = [{"uuid": uuid}]
                else:
                    # value['name'], value['node']
                    uuid = new_node.find_uuid_by_name_and_type(value["name"], value["node"][0].lower())
                    entities_to_remove_dict[entity_name].append({"uuid": uuid})
            else:
                # If no entity_name could be extracted, add or append to a generic key
                generic_key = "unknown_entities"
                if generic_key not in entities_to_remove_dict:
                    entities_to_remove_dict[generic_key] = [key]
                else:
                    entities_to_remove_dict[generic_key].append(key)

        print("\n======\nentities_to_remove_dict")
        print(entities_to_remove_dict)

        entities_to_remove_dict["node"] = ["Project"]
        payload = entities_to_remove_dict
        print(new_node)
        try:
            print(new_node["uuid"])
        except Exception as e:
            print(e)
        try:
            print(new_node.uuid)
        except Exception as e:
            print(e)

        response = API.send_patch_request_for_entity(parent_node=new_node, payload=payload)
        quit()
        # print(" ---  removing     ")
        # print(response.json())

        # 1) ITERABLE ITEMS ADDED
        print("  1)   ITERABLE ITEMS ADDED ")

        entities_to_patch_dict = {}

        for key, value in iterable_items_added.items():
            # Use split to parse out the entity name from the key
            try:
                entity_name = key.split("['")[1].split("']")[0]
            except IndexError:
                entity_name = None

            # Proceed with the rest of the logic as before
            if entity_name:
                if entity_name not in entities_to_patch_dict:
                    entities_to_patch_dict[entity_name] = [value]
                else:
                    entities_to_patch_dict[entity_name].append(value)
            else:
                # If no entity_name could be extracted, add or append to a generic key
                generic_key = "unknown_entities"
                if generic_key not in entities_to_patch_dict:
                    entities_to_patch_dict[generic_key] = [key]
                else:
                    entities_to_patch_dict[generic_key].append(key)

        # print("======entities_to_patch_dict")
        # print(entities_to_patch_dict)

        # 2) DICT ITEMS ADDED
        print("  2) DICT ITEMS ADDED ")
        # print("dictionary_items_added:  ", dictionary_items_added)

        for path in dictionary_items_added:
            # Strip "root" and square brackets, then remove quotes
            key_name = path.replace("root[", "").replace("]", "").replace("'", "")
            entities_to_patch_dict[key_name] = []

        entities_to_patch_dict_keys_list = list(entities_to_patch_dict.keys())

        #######################
        # this will pacth changes ,
        # retry without duplicates, and relink , and
        ###################

        for item in entities_to_patch_dict_keys_list:
            if isinstance(cleaned_modified[item], list):
                node_objects = cleaned_modified[item]

                try:
                    schema = new_node.load_schema_for_node_type(item)  # Assume load_schema is implemented to fetch the correct schema
                    print("\n-----0 schema")
                    print(schema)
                    print("-----0 schema\n")
                    for obj in node_objects:
                        # Dynamically set the key based on the first element of the 'node' list, converted to lowercase
                        key = obj.get("node")[0].lower() if obj.get("node") else "unknown"

                        # Check if the key exists in the global_patch_dict
                        if key in entities_to_patch_dict:
                            # If key exists, append the current object to the list
                            entities_to_patch_dict[key].append(obj)
                        else:
                            # If key does not exist, create a new list with the current object
                            entities_to_patch_dict[key] = [obj]

                    # print(entities_to_patch_dict)
                except ValidationError as e:
                    print(f"Validation error for {item}: {e}")
                    continue  # Skip patching this entity due to validation failure
                    # Send patch request for the current entity with its objects

                # print(f"VALIDATED list under ENTITY {item}")
                # print("pray we get here")
                entities_to_patch_dict["node"] = new_node.node
                # print(entities_to_patch_dict)

                # print("$$$$$$--00---node_objects")

                # payload = {"node": [self.node_type.capitalize()], item: node_objects}

                payload = entities_to_patch_dict

                response = new_node.send_patch_request_for_entity(payload)
                # print("            77777   (...0.0)     555      ")
                # print(response.json())

                if response.status_code in [200, 204]:
                    print(f"Update successful for {item}.")

                elif response.status_code in [409, 400]:
                    # if there are duplicates, we can relink
                    error_response = response.json()  # Assuming this returns an error message indicating duplicates

                    # print(" NOW SHOULD GET HERE ")
                    # print("-+++++- error_response")
                    # print(error_response["error"])

                    error_message = error_response["error"]
                    # error_message = "duplicate item [{'name': 'yoyo888'}, {'name': 'uwa888'}] for Material"
                    # Extract the JSON-like list of dictionaries as a string
                    try:
                        # print(error_message)
                        name_list_str = error_message.split("[")[1].split("]")[0]
                        try_this = eval("[" + name_list_str + "]")
                        # print("try_this")
                        # print(try_this)
                        # print(type(try_this))
                        # print(type(try_this[0]))
                        duplicate_names = [str(item) for item in try_this]

                        if type(try_this[0]) == dict:
                            # print("AMIHERE")
                            name_list1 = [str(item["name"]) for item in try_this if "name" in item]
                            # print(name_list1)
                            duplicate_names = name_list1

                    except:
                        print("could not parse")
                        # quit()

                    # duplicate_names = [item["name"] for item in name_list]

                    list_without_duplicates = new_node.remove_duplicates(node_objects, duplicate_names)

                    # print("---- !!! trying 1")

                    if len(list_without_duplicates) > 0:
                        # Prepare the original payload minus the duplicates for retry
                        payload_without_duplicates = {"node": [new_node.node_type.capitalize()], item: list_without_duplicates}

                        # print("---- !!! hey !!!  wooooooo")
                        # print(payload_without_duplicates)

                        dedupe_response = new_node.send_patch_request_for_entity(payload_without_duplicates)
                        if dedupe_response.status_code in [200, 204]:
                            print(f"dedupe update successful {dedupe_response.status_code} .")
                        else:
                            print(f"dedupe update failed with status code {dedupe_response.status_code}: {dedupe_response.text}")

                    # print("---- !!! trying 2")

                    if len(duplicate_names) > 0:
                        # Find UUIDs for duplicates and prepare them for relinking
                        uuids_for_relinking = [new_node.find_uuid_by_name_and_type(name, item) for name in duplicate_names]
                        relink_payload = {"node": [new_node.node_type.capitalize()], item: [{"uuid": uuid} for uuid in uuids_for_relinking if uuid]}

                        relink_response = API.send_patch_request_for_entity(new_node, relink_payload)
                        # print("------")
                        print("relink_response", relink_response)

                        if relink_response.status_code in [200, 204]:
                            print(f"Relink update successful for {item} with relinking.")
                        else:
                            print(f"Relink update failed for {item} with status code {relink_response.status_code}: {relink_response.text}")

                    print(" SWEATING !  hopefully here ")

                else:
                    print(f"Update failed for {item} with status code {response.status_code}: {response.text}")

            # ------------------------------------------------------------
            elif isinstance(cleaned_modified[item], dict):
                # Business logic for the dictionary goes here
                print(f"Single dict: {cleaned_modified[item]}")
                # Implement your business logic here
            else:
                # Handle the case where the item is neither a list of dictionaries nor a single dictionary
                print(f"{item} is neither a list of dicts nor a single dict.")

        # this needs more work
        print(" - FINALLY WE GET ALL THE WAY TO THE END ")

    # ====================END SAVE=================================

    # =========================================================================
    def save(self, node: PrimaryBaseNode):  # project: Project) -> str:  # None:
        # kinda broken because only takes in a project and needs to resave an entire project
        # in reality we should just take in a node, find out what kind of node it is , save that node
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
            self._internal_save(node)
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
            test_get_response: Dict = requests.get(url=f"{self._host}/{node.node_type_snake_case}/{str(node.uuid)}/", headers=self._http_headers, timeout=_API_TIMEOUT).json()
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
                response: Dict = requests.patch(url=f"{self._host}/{node.node_type_snake_case}/{str(node.uuid)}/", headers=self._http_headers, data=json_data, timeout=_API_TIMEOUT).json()  # type: ignore
            else:
                response: Dict = requests.post(url=f"{self._host}/{node.node_type_snake_case}/", headers=self._http_headers, data=json_data, timeout=_API_TIMEOUT).json()  # type: ignore
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
        value_to_search: Optional[str],
    ) -> Paginator:
        """
        This method is used to perform search on the CRIPT platform.

        Essentially creates needed resources and passes it to paginator to get results from API
        and display them.

        Examples
        --------
        ???+ Example "Search by Node Type"
            ```python
            materials_paginator = cript_api.search(
                node_type=cript.Material,
                search_mode=cript.SearchModes.NODE_TYPE,
                value_to_search=None
            )
            ```

        ??? Example "Search by Contains name"
            ```python
            contains_name_paginator = cript_api.search(
                node_type=cript.Process,
                search_mode=cript.SearchModes.CONTAINS_NAME,
                value_to_search="poly"
            )
            ```

        ??? Example "Search by Exact Name"
            ```python
            exact_name_paginator = cript_api.search(
                node_type=cript.Project,
                search_mode=cript.SearchModes.EXACT_NAME,
                value_to_search="Sodium polystyrene sulfonate"
            )
            ```

        ??? Example "Search by UUID"
            ```python
            uuid_paginator = cript_api.search(
                node_type=cript.Collection,
                search_mode=cript.SearchModes.UUID,
                value_to_search="75fd3ee5-48c2-4fc7-8d0b-842f4fc812b7"
            )
            ```

        ??? Example "Search by BigSmiles"
            ```python
            paginator = cript_api.search(
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
        value_to_search : Optional[str]
            What you are searching for can be either a value, and if you are only searching for
            a `NODE_TYPE`, then this value can be empty or `None`

        Returns
        -------
        Paginator
            paginator object for the user to use to flip through pages of search results

        Notes
        -----
        To learn more about working with pagination, please refer to our
        [paginator object documentation](../paginator).

        Additionally, you can utilize the utility function
        [`load_nodes_from_json(node_json)`](../../utility_functions/#cript.nodes.util.load_nodes_from_json)
        to convert API JSON responses into Python SDK nodes.

        ???+ Example "Convert API JSON Response to Python SDK Nodes"
            ```python
            # Get updated project from API
            my_paginator = api.search(
                node_type=cript.Project,
                search_mode=cript.SearchModes.EXACT_NAME,
                value_to_search="my project name",
            )

            # Take specific Project you want from paginator
            my_project_from_api_dict: dict = my_paginator.current_page_results[0]

            # Deserialize your Project dict into a Project node
            my_project_node_from_api = cript.load_nodes_from_json(
                nodes_json=json.dumps(my_project_from_api_dict)
            )
            ```
        """

        # get node typ from class
        node_type = node_type.node_type_snake_case

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

        elif search_mode == SearchModes.BIGSMILES:
            api_endpoint = f"{self._host}/search/bigsmiles/"

        # error handling if none of the API endpoints got hit
        else:
            raise RuntimeError("Internal Error: Failed to recognize any search modes. Please report this bug on https://github.com/C-Accel-CRIPT/Python-SDK/issues.")

        return Paginator(http_headers=self._http_headers, api_endpoint=api_endpoint, query=value_to_search, current_page_number=page_number)

    def delete(self, node) -> None:
        """
        Simply deletes the desired node from the CRIPT API and writes a log in the terminal that the node has been
        successfully deleted.

        Examples
        --------
        >>> import cript
        >>> my_material_node = cript.Material(
        ...     name="my component material 1",
        ...     identifier=[{"amino_acid": "component 1 alternative name"}],
        ... )
        >>> api.delete(node=my_material_node) # doctest: +SKIP

        Notes
        -----
        After the node has been successfully deleted, a log is written to the terminal if `cript.API.verbose = True`

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
        After the node has been successfully deleted, a log is written to the terminal if `cript.API.verbose = True`

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
        delete_node_api_url: str = f"{self._host}/{node_type.lower()}/{node_uuid}/"

        response: Dict = requests.delete(headers=self._http_headers, url=delete_node_api_url, timeout=_API_TIMEOUT).json()

        if response["code"] != 200:
            raise APIError(api_error=str(response), http_method="DELETE", api_url=delete_node_api_url)

        self.logger.info(f"Deleted '{node_type.title()}' with UUID of '{node_uuid}' from CRIPT API.")
