import copy
import json
import os
import warnings
from typing import List, Literal, Union

import requests
from jsonschema import validate as json_validate

from cript.api._valid_search_modes import _VALID_SEARCH_MODES
from cript.api.exceptions import (
    CRIPTAPIAccessError,
    CRIPTConnectionError,
    InvalidVocabulary,
    InvalidVocabularyCategory,
)
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


class API:
    _host: str = ""
    _token: str = ""
    _vocabulary: dict = {}
    _schema: dict = {}

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

        # strip ending slash to make host always uniform
        host = host.rstrip("/")

        # if host is using unsafe "http://" then give a warning
        if host.startswith("http://"):
            warnings.warn("HTTP is an unsafe protocol please consider using HTTPS.")

        # check that api can connect to CRIPT with host and token
        try:
            # TODO send an http request to check connection with host and token
            pass
        except Exception as exc:
            raise CRIPTConnectionError(host, token) from exc

        # Only assign to class after the connection is made
        self._host = host
        self._token = token

        self._get_and_set_vocab()
        self._load_db_schema()

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

    def _get_and_set_vocab(self) -> dict:
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
            return self._vocabulary

        # TODO get all controlled vocabulary from an API endpoint instead of having it statically
        # vocabulary cache is empty and need to get the entire controlled vocabulary
        # all the controlled vocabulary categories
        all_categories_of_controlled_vocab = [
            "algorithm_key",
            "algorithm_type",
            "building_block",
            "citation_type",
            "computation_type",
            "computational_forcefield_key",
            "computational_process_property_key",
            "computational_process_type",
            "condition_key",
            "data_license",
            "data_type",
            "equipment_key",
            "file_type",
            "ingredient_keyword",
            "material_identifier_key",
            "material_keyword",
            "material_property_key",
            "parameter_key",
            "process_keyword",
            "process_property_key",
            "process_type",
            "property_method",
            "quantity_key",
            "reference_type",
            "set_type",
            "uncertainty_type",
        ]

        # loop through all vocabulary categories and make a request to each vocabulary category
        # and put them all inside of self._vocab with the keys being the vocab category name
        for category in all_categories_of_controlled_vocab:
            response = requests.get(f"{self.host}/api/v1/cv/{category}").json()["data"]
            self._vocabulary[category] = response

        return self._vocabulary

    def get_vocabulary(self) -> dict:
        """
        get the entire controlled vocabulary for the user to use

        Returns
        -------
        dict
        controlled vocabulary
        """

        # return a copy because we don't want anyone being able to accidentally change the private attribute
        return copy.deepcopy(self._vocabulary)

    def is_vocab_valid(
        self, vocab_category: str, vocab_value: str
    ) -> Union[bool, InvalidVocabulary, InvalidVocabularyCategory]:
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
        vocab_value: str
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
        if vocab_value.startswith("+"):
            return True

        # Raise Exeption if invalid category
        controlled_vocabulary = self.get_vocabulary(vocab_category)

        if vocab_value in controlled_vocabulary:
            return True
        # if the vocabulary does not exist in a given category
        raise InvalidVocabulary(vocab_value, controlled_vocabulary)

    def _load_db_schema(self):
        """
        Sends a GET request to CRIPT to get the database schema and returns it.
        The database schema can be used for validating the JSON request
        before submitting it to CRIPT.

        Makes a request to get it from CRIPT.
        After successfully getting it from CRIPT, it sets the class variable
        """
        # TODO figure out the version
        response = requests.get(f"{self.host}/api/v1/schema/").json()
        # TODO error checking
        # TODO check that we support that version
        self._schema = response

    def is_node_valid(self, node_json: str) -> bool:
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
        if json_validate(node_dict, self._schema):
            return True
        else:
            return False

    @property
    def schema(self):
        """
        Access the CRIPTSchema that is associated with this API connection.
        This can be used to validate node JSON.
        """
        return copy.copy(self._schema)

    @property
    def host(self):
        """
        Read only access to the currently connected host.
        If the connection to a new host is desired, create a new API object.
        """
        return self._host

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
        # TODO create a giant JSON from the primary node given and send that to
        #   the backend with a POST request
        #   the user will just hit save and the program needs to figure out
        #   the saving of new or updating
        #   save is POST request and update would be PATCH request
        pass

    def delete(self, node: PrimaryBaseNode, ask_confirmation: bool = True) -> None:
        """ "
        Deletes the given node.

        Parameters
        ----------
        node : PrimaryBaseNode
            The node to delete.
        ask_confirmation : bool, optional, default=True
            If True, the function will delete the node without prompting the user
            for confirmation (default is False).

        Returns
        -------
        NoneType
            None

        Notes
        -----
        By default, this function prompts the user with "are you sure you want to
        delete this node?" before proceeding with the deletion. If the `ask_confirmation`
        parameter is set to False, the prompt will be suppressed and the node will be
        deleted without confirmation.
        """
        # ask for confirmation before deleting the node
        if ask_confirmation:
            # get the user input and convert it to lowercase
            confirm: str = input(f"are you sure you want to delete {node}? (y/n): ").lower()

            # if confirmation is anything other than yes then cancel the delete
            if confirm not in ["y", "yes"]:
                print(f"Deletion cancelled for node: {node}")
                return

        # if no_input is True or it got passed the confirmation then send a http request to delete the node
        print(f"deleting {node}")
        # TODO http request to delete the node in JSON form
        pass

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
        search_mode: Literal[_VALID_SEARCH_MODES],
        value_to_search: str,
    ):
        """
        This is the method used to perform a search on the CRIPT platform.

        Parameters
        ----------
        node_type : PrimaryBaseNode
            Type of node that you are searching for.
        search_mode : str
            Type of search you want to do. You can search by name, UUID, URL, etc.
        value_to_search : str
            What you are searching for.

        Returns
        -------
        List[BaseNode]
            List of nodes that matched the search.
        """
        # TODO send search query and get the result back
        pass
