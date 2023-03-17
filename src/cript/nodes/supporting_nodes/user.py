from dataclasses import dataclass
from typing import List, Union, Any

from cript.nodes.core import BaseNode
from cript.nodes.supporting_nodes.group import Group
from cript.nodes.exceptions import UneditableAttributeError


class User(BaseNode):
    """
    The User node

    Note: A user cannot be created or modified using the SDK.
    This object is for read-only purposes only.
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all User attributes
        """

        node: str = "User"
        username: str = ""
        email: str = ""
        orcid: str = ""
        groups = List[Group]

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        username: str,
        email: str,
        orcid: str,
        groups: Union[Group, List[Group]] = None,
    ):
        """
        Json from CRIPT API to be converted to a node
        optionally the group can be None if the user doesn't have a group

        Parameters
        ----------
        username
        email
        orcid
        groups
        """
        super().__init__(node="User")
        pass

    # ------------------ properties ------------------

    @property
    def username(self) -> str:
        """
        username of the User node

        Returns
        -------
        str
            username of the User node
        """
        return self._json_attrs.username

    @username.setter
    def username(self, value: Any) -> None:
        """
        User cannot set the username for the user node.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        value

        Returns
        -------
        None
        """
        raise UneditableAttributeError

    @property
    def email(self) -> str:
        """
        email of the user node

        Returns
        -------
        str
            User node email
        """
        return self._json_attrs.email

    @email.setter
    def email(self, value: Any) -> None:
        """
        User cannot set the email for the user node.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        value

        Returns
        -------
        None
        """
        raise UneditableAttributeError

    @property
    def orcid(self) -> str:
        """
        users ORCID

        Returns
        -------
        str
            users ORCID
        """
        return self._json_attrs.orcid

    @orcid.setter
    def orcid(self, value: Any) -> None:
        """
        User cannot set the orcid for the user node.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        value

        Returns
        -------
        None
        """
        raise UneditableAttributeError

    @property
    def groups(self):
        """
        gets the list of group nodes that the user belongs in

        Returns
        -------
        List[Group]
            List of Group nodes that the user belongs in
        """
        return self._json_attrs.groups

    @groups.setter
    def groups(self, value: Any):
        """
        User cannot set the group for the user node.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        value

        Returns
        -------
        None
        """
        raise UneditableAttributeError
