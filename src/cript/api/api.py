import copy
import json
import os
import warnings
from typing import List, Union

import requests
from jsonschema import validate as json_validate
from urllib.parse import quote

from cript.api.valid_search_modes import SearchModes
from cript.api.exceptions import (
    CRIPTAPIAccessError,
    CRIPTConnectionError,
    InvalidVocabulary,
    InvalidVocabularyCategory,
    CRIPTAPISaveError,
    InvalidSearchModeError,
)
from cript.api.vocabulary_categories import all_controlled_vocab_categories
from cript.nodes.exceptions import CRIPTNodeSchemaError
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.project import Project
from cript.nodes.supporting_nodes.group import Group
from cript.nodes.supporting_nodes.user import User

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


def _prepare_host(host: str) -> str:
    """
    prepares the host and gets it ready to be used within the api client

    1. removes any trailing spaces from the left or right side
    1. removes "/" from the end so that it is always uniform
    1. adds "/api", so all queries are sent directly to the API

    Parameters
    ----------
    host: str
        api host

    Returns
    -------
    host: str
    """
    # strip any empty spaces on left or right
    host = host.strip()

    # strip ending slash to make host always uniform
    host = host.rstrip("/")

    # if host is using unsafe "http://" then give a warning
    if host.startswith("http://"):
        warnings.warn("HTTP is an unsafe protocol please consider using HTTPS.")

    return host


class API:
    _host: str = ""
    _token: str = ""
    _vocabulary: dict = {}
    _db_schema: dict = {}
    _http_headers: dict = {}

    def __init__(self, host: Union[str, None], token: [str, None]):
        """
        Initialize object with host and token.
        It is necessary to use a `with` context manager with the API like so:
        ```
        with cript.API('https://criptapp.org', 'secret_token') as api:
           # node creation, api.save(), etc.
        ```

        Parameters
        ----------
        host : str, None
            CRIPT host to connect to such as "https://criptapp.org"
            if host ends with a "/" such as "https://criptapp.org/"
            then it strips it to always be uniform.
            This host address is the same that use to login to cript website.

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
            If `host` is using "http".

        Raises
        ------
        ConnectionError
            If it cannot connect to CRIPT with the provided host and token

        Returns
        -------
        None
        """

        # if host and token is none then it will grab host and token from user's environment variables
        if host is None:
            host = os.environ.get("CRIPT_HOST")
            if host is None:
                raise RuntimeError(
                    "API initilized with `host=None` but environment variable `CRIPT_HOST` not found.\n"
                    "Set the environment variable (preferred) or specify the host explictly at the creation of API."
                )
        if token is None:
            token = os.environ.get("CRIPT_TOKEN")
            if token is None:
                raise RuntimeError(
                    "API initilized with `token=None` but environment variable `CRIPT_TOKEN` not found.\n"
                    "Set the environment variable (preferred) or specify the token explictly at the creation of API."
                )

        host = _prepare_host(host=host)

        # assign headers
        self._http_headers = {"Authorization": self._token, "Content-Type": "application/json"}

        # check that api can connect to CRIPT with host and token
        try:
            # TODO send an http request to check connection with host and token
            token = f"Bearer {token}"
        except Exception as exc:
            raise CRIPTConnectionError(host, token) from exc

        # Only assign to class after the connection is made
        self._host = host
        self._token = token

        self.get_vocab()
        self._get_db_schema()

    def __enter__(self):
        self.connect()

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
        Access the CRIPTSchema that is associated with this API connection.
        This can be used to validate node JSON.
        """
        return copy.copy(self._db_schema)

    @property
    def host(self):
        """
        Read only access to the currently connected host.
        If the connection to a new host is desired, create a new API object.
        """
        return self._host

    # TODO this needs a better name because the current name is unintuitive if you are just getting vocab
    def get_vocab(self) -> dict:
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
        if bool(self._vocabulary):
            return copy.deepcopy(self._vocabulary)

        # TODO this needs to be converted to a dict of dicts instead of dict of lists
        #  because it would be faster to find needed vocab word within the vocab category
        # loop through all vocabulary categories and make a request to each vocabulary category
        # and put them all inside of self._vocab with the keys being the vocab category name
        for category in all_controlled_vocab_categories:
            response = requests.get(f"{self.host}/api/v1/cv/{category}").json()["data"]
            self._vocabulary[category] = response

        return copy.deepcopy(self._vocabulary)

    def is_vocab_valid(self, vocab_category: str, vocab_word: str) -> Union[bool, InvalidVocabulary, InvalidVocabularyCategory]:
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
            controlled_vocabulary = self.get_vocab()
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
            response = requests.get(f"{self.host}/api/v1/schema/").json()

            self._db_schema = response["data"]["$defs"]
            return self._db_schema

    # TODO should this throw an error if invalid?
    def is_node_schema_valid(self, node_json: str) -> Union[bool, CRIPTNodeSchemaError]:
        """
        checks a node JSON schema against the db schema to return if it is valid or not.
        This function does not take into consideration vocabulary validation.
        For vocabulary validation please check `is_vocab_valid`

        Parameters
        ----------
        node:
            a node in JSON form

        Returns
        -------
        bool
            whether the node JSON is valid or not
        """

        # TODO currently validate says every syntactically valid JSON is valid
        # TODO do we want invalid schema to raise an exception?
        node_dict = json.loads(node_json)

        if json_validate(instance=node_dict, schema=self._db_schema):
            return True
        else:
            return False

    def save(self, node: PrimaryBaseNode) -> None:
        """
        This method takes a primary node, serializes the class into JSON
        and then sends the JSON to be saved to the API

        Parameters
        ----------
        node: primary node
            the Primary Node that the user wants to save

        Returns
        -------
        None
        """
        response = requests.post(self._host, headers=self._http_headers).json()

        # if htt response is not 200 then show the API error to the user
        if response.status_code != 200:
            raise CRIPTAPISaveError(api_host_domain=self._host, api_response=response["error"])

    # TODO delete method will come later when the API supports it
    # def delete(self, node: PrimaryBaseNode, ask_confirmation: bool = True) -> None:
    #     """ "
    #     Deletes the given node.
    #
    #     Parameters
    #     ----------
    #     node : PrimaryBaseNode
    #         The node to delete.
    #     ask_confirmation : bool, optional, default=True
    #         If True, the function will delete the node without prompting the user
    #         for confirmation (default is False).
    #
    #     Returns
    #     -------
    #     NoneType
    #         None
    #
    #     Notes
    #     -----
    #     By default, this function prompts the user with "are you sure you want to
    #     delete this node?" before proceeding with the deletion. If the `ask_confirmation`
    #     parameter is set to False, the prompt will be suppressed and the node will be
    #     deleted without confirmation.
    #     """
    #     # ask for confirmation before deleting the node
    #     if ask_confirmation:
    #         # get the user input and convert it to lowercase
    #         confirm: str = input(f"are you sure you want to delete {node}? (y/n): ").lower()
    #
    #         # if confirmation is anything other than yes then cancel the delete
    #         if confirm not in ["y", "yes"]:
    #             print(f"Deletion cancelled for node: {node}")
    #             return
    #
    #     # if no_input is True or it got passed the confirmation then send a http request to delete the node
    #     print(f"deleting {node}")
    #     # TODO http request to delete the node in JSON form
    #     pass

    def get_my_user(self) -> User:
        """
        Returns the user node associated with the user's account using the token.

        Returns
        -------
        User: User
            The user node associated with the user's account.

        Notes
        -----
        This function retrieves the user node associated with the user's account.
        """
        # TODO send http request to get user node in JSON
        # convert user JSON into user node
        # return user node
        # or just print out the json, and that should work for the first version
        pass

    def get_my_groups(self) -> List[Group]:
        # TODO send http request to backend to get all of the users Groups
        pass

    def get_my_projects(self) -> List[Project]:
        # TODO send http request to backend to get all of the users Projects
        pass

    def search(
        self,
        node_type: PrimaryBaseNode,
        search_mode: SearchModes,
        value_to_search: str,
    ):
        """
        This is the method used to perform a search on the CRIPT platform.

        since we are using Enum here we don't even need to check if the search mode is valid
        because if the search mode is invalid then it would throw an AttributeError

        checks which mode the search is asking for, creates the api_endpoint URL for it
        and at the end it sends the request to the API and returns the API response to the user

        Parameters
        ----------
        node_type : PrimaryBaseNode
            Type of node that you are searching for.
        search_mode : SearchModes
            Type of search you want to do. You can search by name, UUID, URL, etc.
        value_to_search : Union[str, None]
            What you are searching for can be either a value, and if you are only searching for
            a node type, then this value can be empty

        Raises
        -------
        InvalidSearchModeError
            In case none of the search modes were fulfilled

        Returns
        -------
        List[BaseNode]
            List of nodes that matched the search.
        """

        # requesting a page of some primary node
        if search_mode == SearchModes.NODE_TYPE:
            page_number = 1
            api_endpoints: str = f"{self._host}/{node_type.node}/?page={page_number}"

        # requesting a node by UUID
        elif search_mode == SearchModes.UUID:
            api_endpoint: str = f"{self._host}/{node_type.node}/{value_to_search}"

        # skipping this for now because don't understand what its needed or does exactly, but still done
        # find a node by its UUID and return only all of its children, excluding the parent
        # elif search_mode == SearchModes.UUID_CHILDREN:
        #     api_endpoint: str = f"{self._host}/{node_type.node}/{value_to_search}/"

        elif search_mode == SearchModes.CONTAINS_NAME:
            # URL encode value to search
            value_to_search = quote(value_to_search)
            api_endpoint: str = f"{self._host}/search/{node_type.node}/?q={value_to_search}"

        elif search_mode == SearchModes.EXACT_NAME:
            value_to_search = quote(value_to_search)
            api_endpoint: str = f"{self._host}/search/{node_type.node}/?q={value_to_search}"

        try:
            response = requests.get(
                url=api_endpoint,
                headers=self._http_headers,
            ).json()

            return response

        # if none of the search_modes were able to capture and create an api_endpoint variable
        # then an InvalidSearchModeError is raised
        except NameError:
            raise InvalidSearchModeError(invalid_search_mode=search_mode)
