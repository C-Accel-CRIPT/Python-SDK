import json
import warnings
from src.exceptions import ConnectionError
from src.nodes.primary_nodes import PrimaryNode


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

    def get_my_groups():
        pass

    def get_my_projects():
        pass

    def delete(node: PrimaryNode, no_input: bool = False) -> None:
        """ "
        Args:
            node (PrimaryNode): node to delete

            no_input (boolean): by default before deleting a node it asks the user if they are sure they want to delete this node. However, if the user wants to delete nodes without being prompted they can set the no_input = True and the the API object will delete the node without prompting the user
        """
        # if user did not set no_input mode, then ask the user if they are sure
        if no_input == False:
            # get input and convert it to lowercase for easy/consistent comparison
            confirmation: str = input(
                f"are you sure you want to delete {node}? (y/n): "
            ).lower()

            if confirmation == "y" or confirmation == "yes":
                print("DELETING THE NODE!")


if __name__ == "__main__":
    api = API("http://criptapp.org", "123456")
