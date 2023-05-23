import copy
import json
import warnings
from typing import Dict, List, Union

import jsonschema
import requests

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
from cript.api.valid_search_modes import SearchModes
from cript.api.vocabulary_categories import ControlledVocabularyCategories
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
        raise CRIPTAPIRequiredError()
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

    def __init__(self, host: Union[str, None] = None, token: Union[str, None] = None, config_file_path: str = ""):
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

        if config_file_path or (host is None and token is None):
            authentication_dict: Dict[str, str] = resolve_host_and_token(host, token, config_file_path)

            host = authentication_dict["host"]
            token = authentication_dict["token"]

        self._host = self._prepare_host(host=host)
        self._token = token

        # assign headers
        # TODO might need to add Bearer to it or check for it
        self._http_headers = {"Authorization": f"{self._token}", "Content-Type": "application/json"}

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
            raise InvalidHostError()

        return host

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
            raise Exception(f"while getting controlled vocabulary from CRIPT by {category}, " f"the API responded with http {response} ")

        # add to cache
        self._vocabulary[category.value] = response["data"]

        return self._vocabulary[category.value]

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

    # TODO this should later work with both POST and PATCH. Currently, just works for POST
    def _is_node_schema_valid(self, node_json: str) -> bool:
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
            raise CRIPTNodeSchemaError(error_message=str(error) + str(error.context)) from error

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
