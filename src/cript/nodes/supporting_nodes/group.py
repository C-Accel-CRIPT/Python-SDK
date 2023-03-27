from dataclasses import dataclass, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.exceptions import UneditableAttributeError
from cript import User


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
        admins: List[User] = None
        users: List[User] = None
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        admin: List[User],
        user: List[User] = None,
        **kwargs
    ):
        """
        constructor for a Group node

        Parameters
        ----------
        name: str
            group name
        admin: User
            administrator of this group
        users: User
            user or list of users that are in this Group

        Returns
        -------
        None
        """
        super().__init__(node="Group")
        self._json_attrs = replace(
            self._json_attrs, name=name, admins=admin, users=user
        )
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
    def admins(self) -> List[User]:
        """
        name property getter method

        Returns
        -------
        admins: List[User]
            an admin or list of admins
        """
        return self._json_attrs.admins

    @admins.setter
    def admins(self, new_admins: List[User]) -> None:
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
    def users(self) -> List[User]:
        """
        users that belong to this group

        Returns
        -------
        List[User]
            users that belong to this group
        """
        return self._json_attrs.users

    @users.setter
    def users(self, new_user: List[User]) -> None:
        """
        sets the users for this group

        User cannot set the notes for any nodes.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        new_user
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
    def notes(self, value: str) -> None:
        """
        set notes for group

        User cannot set the notes for any nodes.
        Attempt to do so will raise an UneditableAttributeError

        Parameters
        ----------
        value
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
