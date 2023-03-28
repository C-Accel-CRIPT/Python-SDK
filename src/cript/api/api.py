import copy
import os
import warnings
from typing import List, Literal, Union

from cript.api._valid_search_modes import _VALID_SEARCH_MODES
from cript.api.exceptions import CRIPTAPIAccessError, CRIPTConnectionError
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.project import Project
from cript.nodes.supporting_nodes.group import Group
from cript.nodes.supporting_nodes.user import User

_global_cached_api = None


def _get_global_cached_api():
    """
    Read-Only access to the globally cached API object.
    Raises an exception if no global API object is cached yet.
    """
    if _global_cached_api is None:
        raise CRIPTAPIAccessError
    return copy.copy(_global_cached_api)


class API:
    _host: str = ""
    _token: str = ""

    def __init__(self, host: Union[str, None], token: [str, None]) -> None:
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

    def __enter__(self):
        # Store the last active global API (might be None)
        global _global_cached_api
        self._previous_global_cached_api = copy.copy(_global_cached_api)
        _global_cached_api = self
        return self

    def __exit__(self, type, value, traceback):
        # Restore the previously active global API (might be None)
        global _global_cached_api
        _global_cached_api = self._previous_global_cached_api

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
