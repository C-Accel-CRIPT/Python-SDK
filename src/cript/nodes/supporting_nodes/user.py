from dataclasses import dataclass, field, replace
from typing import Any, List

import cript
from cript.nodes.core import BaseNode


class User(BaseNode):
    """
    [User node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)

    | attribute  | type        | example                    | description                                | required | vocab |
    |------------|-------------|----------------------------|--------------------------------------------|----------|-------|
    | url        | str         |                            | unique ID of the node                      | True     |       |
    | username   | str         | "john_doe"                 | User’s name                                | True     |       |
    | email      | str         | "user@cript.com"           | email of the user                          | True     |       |
    | orcid      | str         | "0000-0000-0000-0000"      | ORCID ID of the user                       | True     |       |
    | groups     | List[Group] |                            | groups you belong to                       |          |       |
    | updated_at | datetime*   | 2023-03-06 18:45:23.450248 | last date the node was modified (UTC time) | True     |       |
    | created_at | datetime*   | 2023-03-06 18:45:23.450248 | date it was created (UTC time)             | True     |       |


    ## JSON
    ```json
    {
        "node": "User",
        "username": "my username",
        "email": "user@email.com",
        "orcid": "0000-0000-0000-0001",
    }
    ```

    Warning:
        * A User cannot be created or modified using the Python SDK.
        * A User node is a **read-only** node that can only be deserialized from API JSON response to Python node.
        * The User node cannot be instantiated and within the Python SDK.
        * Attempting to edit the user node will result in an `Attribute Error`

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
        # TODO add type hints later, currently avoiding circular import error
        groups: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, username: str, email: str, orcid: str, groups: List[Any] = None, **kwargs):
        """
        Json from CRIPT API to be converted to a node
        optionally the group can be None if the user doesn't have a group

        Args:
            username (str): user username
            email (str): user email
            orcid (str): user ORCID
            groups: (List[Group): groups that this user belongs to

        """
        if groups is None:
            groups = []
        super().__init__(node="User")
        self._json_attrs = replace(self._json_attrs, username=username, email=email, orcid=orcid, groups=groups)
        self.validate()

    # ------------------ properties ------------------

    @property
    def username(self) -> str:
        """
        username of the User node

        Raises:
            AttributeError

        Returns:
            username of the User node
        """
        return self._json_attrs.username

    @property
    def email(self) -> str:
        """
        user's email

        Raises:
            AttributeError

        Returns:
            User node email
        """
        return self._json_attrs.email

    @property
    def orcid(self) -> str:
        """
        users [ORCID](https://orcid.org/)

        Raises:
            AttributeError

        Returns:
            user's ORCID
        """
        return self._json_attrs.orcid

    @property
    def groups(self) -> List[Any]:
        """
        gets the list of group nodes that the user belongs in

        Raises:
            AttributeError

        Returns:
            List of Group nodes that the user belongs in
        """
        return self._json_attrs.groups
