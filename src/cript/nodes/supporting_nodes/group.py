from dataclasses import dataclass, replace
from typing import List, Union

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
        url: str = ""
        name: str = ""
        admins: Union[User, List[User]] = None
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
        self._json_attrs = replace(self._json_attrs, name=name, admins=admin, users=user)
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
