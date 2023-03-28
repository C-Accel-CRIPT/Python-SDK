from dataclasses import dataclass, replace
from typing import List, Any

from cript.nodes.core import BaseNode
from cript.nodes.exceptions import UneditableAttributeError


# TODO add type hints later, currently avoiding circular import
# from cript import User


class Group(BaseNode):
    """
    CRIPT Group node as described in the CRIPT data model
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Group attributes
        """

        node: str = "Group"
        name: str = ""
        admins: List[Any] = None
        users: List[Any] = None
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

    def validate(self) -> None:
        """
        validates Group node

        Returns
        -------
        None

        Raises
        ------
        CRIPTNodeSchemaError
        """
        pass

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

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Setter for the group name

        User cannot set the name for any nodes.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        new_name: str
            new group name

        Returns
        -------
        None

        Raises
        ------
        UneditableAttributeError
            If user attempts to set this property
        """
        raise UneditableAttributeError

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

    @admins.setter
    def admins(self, new_admins: List[Any]) -> None:
        """
        sets admins for the Group node

        User cannot set the admins of the group node.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        new_admins

        Returns
        -------
        None

        Raises
        ------
        UneditableAttributeError
            If user attempts to set this property
        """
        raise UneditableAttributeError

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

    @users.setter
    def users(self, new_users: List[Any]) -> None:
        """
        sets the users for this group

        User cannot set the notes for any nodes.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        new_users
            new user list to override

        Returns
        -------
        None

        Raises
        ------
        UneditableAttributeError
            If user attempts to set this property
        """
        raise UneditableAttributeError

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

    @notes.setter
    def notes(self, new_notes: str) -> None:
        """
        set notes for group

        User cannot set the notes for any nodes.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        new_notes
            new user list to override

        Returns
        -------
        None

        Raises
        ------
        UneditableAttributeError
            If user attempts to set this property
        """
        raise UneditableAttributeError
