from dataclasses import dataclass, field
from typing import Any, List

from cript.nodes.core import BaseNode
from cript.nodes.exceptions import UneditableAttributeError

# TODO add type hints later, currently avoiding circular import error


class User(BaseNode):
    """
    [User node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)

    Notes
    -----
    * A user cannot be created or modified using the SDK.
    This object is for read-only purposes only.

    * type hinting some places that should be Group type as any to avoid circular import error
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
        groups: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, username: str, email: str, orcid: str, groups: List[Any] = None, **kwargs):
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
        self.validate()

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

    @property
    def groups(self):
        """
        gets the list of group nodes that the user belongs in

        Returns
        -------
        List[Any]
            List of Group nodes that the user belongs in
        """
        return self._json_attrs.groups
