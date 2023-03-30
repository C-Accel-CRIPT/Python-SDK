from dataclasses import dataclass, field, replace
from typing import Any, List

from cript.nodes.core import BaseNode


class Group(BaseNode):
    """
    [Group Node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)

    Notes
    ----
    * Group node cannot be created or edited via the Python SDK
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Group attributes
        """

        node: str = "Group"
        name: str = ""
        # TODO add type hints later, currently avoiding circular import
        admins: List[Any] = field(default_factory=list)
        users: List[Any] = field(default_factory=list)
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, admins: List[Any], users: List[Any] = None, **kwargs):
        """
        constructor for a Group node

        Parameters
        ----------
        name: str
            group name
        admins: Any
            administrator of this group
        users: List[Any]
            list of users that are in this Group

        Returns
        -------
        None
        """
        super().__init__(node="Group")
        self._json_attrs = replace(self._json_attrs, name=name, admins=admins, users=users)
        self.validate()

    # ------------------ Properties ------------------

    # Group name
    @property
    def name(self) -> str:
        """
        name property getter method

        Returns
        -------
        name: str
            group name
        """
        return self._json_attrs.name

    # admins
    @property
    def admins(self) -> List[Any]:
        """
        name property getter method

        Returns
        -------
        admins: List[Any]
            an admin or list of admins
        """
        return self._json_attrs.admins

    @property
    def users(self) -> List[Any]:
        """
        users that belong to this group

        Returns
        -------
        List[Any]
            list of users that belong to this group
        """
        return self._json_attrs.users

    @property
    def notes(self) -> str:
        """
        groups notes

        Returns
        -------
        str
            groups notes
        """
        return self._json_attrs.notes
