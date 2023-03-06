import json
import warnings

from src.exceptions import ConnectionError
from src.nodes.primary_nodes import PrimaryNode
from src.nodes.primary_nodes.project import project
from src.nodes.supporting_nodes.group import Group
from src.nodes.supporting_nodes.user import User


class API:
    host: str
    _token: str
    _db_schema: json

    def __init__(self, host: str, token: str) -> None:
        """
        initialize object with host and token
        if host is using "http" then give a warning

        Args:
            host (str): CRIPT host to connect to such as "https://criptapp.org"
            token (str): CRIPT API Token used to connect to CRIPT
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

    def save(node: PrimaryNode) -> None:
        pass

    def get_my_groups() -> Group:
        pass

    def get_my_projects() -> project:
        pass

    def delete(node: PrimaryNode, no_input: bool = False) -> None:
        """ "
        This method can be called when the user wants to delete a node.
        By default it will prompt the user with "are you sure you want to delete this node?",
        however, this can be silenced by setting the no_input parameter to True.

        Args:
            node (PrimaryNode): node to delete

            no_input (boolean): by default before deleting a node it asks the user if they are sure they want to delete this node.
            However, if the user wants to delete nodes without being prompted they can set the no_input = True
            and the the API object will delete the node without prompting the user

        Returns:
            None
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

        # if no_input is True or it got passed the confirmation then send an http request to delete the node
        print(f"deleting {node}")
        # TODO http request to delete the node in JSON form

    def get_my_user() -> User:
        """
        This method can be called to get the user node associated with your account.

        Returns:
            User (User): The user associated with your account
        """
        # TODO send http request to get user node in JSON
        # convert user JSON into user node
        # return user node
        # or just print out the json, and that should work for the first version
        return

    def search(node_type, search_mode, value_to_search) -> PrimaryNode:
        pass


if __name__ == "__main__":
    api = API("http://criptapp.org", "123456")
