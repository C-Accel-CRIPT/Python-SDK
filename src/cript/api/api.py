import json
import warnings
from typing import List, Literal

import requests

from src.cript.api._valid_search_modes import _VALID_SEARCH_MODES
from src.nodes.primary_nodes import PrimaryNode
from src.nodes.primary_nodes.project import Project
from src.nodes.supporting_nodes.group import Group
from src.nodes.supporting_nodes.user import User


class API:
    host: str = ""
    _token: str = ""
    _db_schema: json = None

    def __init__(self, host: str, token: str) -> None:
        """
        Initialize object with host and token.

        Parameters
        ----------
        host : str
            CRIPT host to connect to such as "https://criptapp.org"
        token : str
            CRIPT API Token used to connect to CRIPT

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
        self.host = host
        self._token = token

        # if host is using unsafe "http://" then give a warning
        if self.host.startswith("http://"):
            warnings.warn("HTTP is an unsafe protocol please consider using HTTPS")

        # check that api can connect to CRIPT with host and token
        # try:
        #     # TODO send an http request to check connection with host and token
        #     pass
        # except Exception:
        #     raise ConnectionError

    def _get_db_schema(self) -> json:
        """
        Sends a GET request to CRIPT to get the database schema and returns it.
        The database schema can be used for validating the JSON request
        before submitting it to CRIPT.

        1. Checks if the class variable is already set and if it is then it just returns that.
        2. If db schema is not already saved, then it makes a request to get it from CRIPT
        3. after successfully getting it from CRIPT, it sets the class variable

        Returns
        -------
        json
            The database schema in JSON format.
        """
        # if db_schema is already set then just return it
        if self._db_schema:
            return self._db_schema

        # if db_schema is not already set, then request it
        response = requests.get(f"{self.host}/api/v1/schema/")

        self._db_schema = response.json()
        return self._db_schema

    def save(self, node: PrimaryNode) -> None:
        # TODO create a giant JSON from the primary node given and send that to
        #   the backend with a POST request
        #   the user will just hit save and the program needs to figure out
        #   the saving of new or updating
        #   save is POST request and update would be PATCH request
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
            node_type: PrimaryNode,
            search_mode: Literal[_VALID_SEARCH_MODES],
            value_to_search: str,
    ):
        """
        This is the method used to perform a search on the CRIPT platform.

        Parameters
        ----------
        node_type : PrimaryNode
            Type of node that you are searching for.
        search_mode : str
            Type of search you want to do. You can search by name, UUID, URL, etc.
        value_to_search : str
            What you are searching for.

        Returns
        -------
        List[Node]
            List of nodes that matched the search.
        """
        # TODO send search query and get the result back
        pass

    def delete(self, node: PrimaryNode, no_input: bool = False) -> None:
        """ "
        Deletes the given node.

        Parameters
        ----------
        node : PrimaryNode
            The node to delete.
        no_input : bool, optional, default=False
            If True, the function will delete the node without prompting the user
            for confirmation (default is False).

        Returns
        -------
        NoneType
            None

        Notes
        -----
        By default, this function prompts the user with "are you sure you want to
        delete this node?" before proceeding with the deletion. If the `no_input`
        parameter is set to True, the prompt will be suppressed and the node will be
        deleted without confirmation.
        """
        # ask for confirmation before deleting the node
        if no_input == False:
            # get the user input and convert it to lowercase
            confirm: str = input(
                f"are you sure you want to delete {node}? (y/n): "
            ).lower()

            # if confirmation is not yes then cancel it and continue
            if confirm not in ["y", "yes"]:
                print(f"Deletion cancelled for node: {node}")
                return

        # if no_input is True or it got passed the confirmation then send a http request to delete the node
        print(f"deleting {node}")
        # TODO http request to delete the node in JSON form
        pass
