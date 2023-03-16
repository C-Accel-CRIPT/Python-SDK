from dataclasses import dataclass, replace
from typing import List, Union, Any

from cript.nodes.core import BaseNode
from cript.nodes.supporting_nodes.user import User


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
        admins: Union[User, List[User], List[str]] = None
        users: Union[User, List[User]] = None
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
            self,
            name: str,
            admin: Union[User, List[User]],
            user: Union[User, List[User]] = None,
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
    def name(self, new_name: str):
        """
        Setter for the group name

        Parameters
        ----------
        new_name: str
            new group name

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    def _set_node_or_list(self, field_name: str, new_node: Union[Any, List[Any]]):
        """
        This method sets a field that is a list of node or a single node for this project.
        The user can pass in either a node (such as collection, material, or file )
        to be appended to the list of collections
        or the user can pass in a list of collections to replace the old list of collections.
        This method works by checking if the argument is a list or a single node and
        then behaves accordingly.

        Parameters
        ----------
        field_name: str
            field name within the dataclass JsonAttributes

        new_node: Union[BaseNode, List[BaseNode]
            new node to append to node list
            or new list of nodes to replace the current list

        Returns
        -------
        None
        """
        if isinstance(new_node, list):
            # replace the old list with the new list
            # TODO see if you can write **{field_name: new_node} in a better way
            new_attrs = replace(self._json_attrs, **{field_name: new_node})
            # TODO this needs a more DRY way of handling this
            self._update_json_attrs_if_valid(new_attrs)

        # if appending a single node to the list
        # get the old list, append the node, and replace the field
        else:
            # TODO see if you can write this better
            new_list: List[BaseNode] = getattr(self._json_attrs, field_name)
            new_list.append(new_node)
            new_attrs = replace(self._json_attrs, **{field_name: new_list})
            self._update_json_attrs_if_valid(new_attrs)

    # admins
    @property
    def admins(self) -> Union[User, List]:
        """
        name property getter method

        Returns
        -------
        admins: Union[User, List]
            an admin or list of admins
        """
        return self._json_attrs.admins

    @admins.setter
    def admins(self, new_admins:Union[str, List[str]]):
        self._set_node_or_list("admins", new_admins)
