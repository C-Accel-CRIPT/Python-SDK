from dataclasses import dataclass
from typing import List

from cript.nodes.core import BaseNode
from cript.nodes.supporting_nodes.group import Group


class User:
    """
    The User node as described in the CRIPT data model

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

    # ------------------ properties ------------------

    @property
    def username(self) -> str:
        return self._json_attrs.username

    @property
    def email(self) -> str:
        return self._json_attrs.email

    @property
    def orcid(self) -> str:
        return self._json_attrs.orcid
