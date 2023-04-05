from dataclasses import dataclass, field, replace
from typing import Any, List

from cript.nodes.core import BaseNode


class Group(BaseNode):
    """
    ## Definition

    The [group node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)
    represents a grouping of users collaborating on a common project.
    It serves as the main permission control node and has ownership of data.
    Groups are the owners of data as most research groups have changing membership,
    and the data is typically owned by the organization and not the individuals

    | attribute  | type       | example                    | description                                                | required | vocab |
    |------------|------------|----------------------------|------------------------------------------------------------|----------|-------|
    | url        | str        |                            | unique ID of the node                                      | True     |       |
    | name       | str        | CRIPT development team     | descriptive label                                          | True     |       |
    | notes      | str        |                            | miscellaneous information, or custom<br><br>data structure |          |       |
    | admins     | List[User] |                            | group administrators                                       | True     |       |
    | users      | List[User] |                            | group members                                              | True     |       |
    | updated_by | User       |                            | user that last updated the node                            | True     |       |
    | created_by | User       |                            | user that originally created the node                      | True     |       |
    | updated_at | datetime   | 2023-03-06 18:45:23.450248 | last date the node was modified (UTC time)                 | True     |       |
    | created_at | datetime   | 2023-03-06 18:45:23.450248 | date it was created (UTC time)                             | True     |       |

    Warning:
        * A Group cannot be created or modified using the Python SDK.
        * A Group node is a **read-only** node that can only be deserialized from API JSON response to Python node.
        * The Group node cannot be instantiated and within the Python SDK.
        * Attempting to edit the Group node will result in an `Attribute Error`

    ## JSON
    ```json
    {
      "node": "Group",
      "name": "my group name",
      "notes": "my group notes",
      "admins": [
        {
          "node": "User",
          "username": "my admin username",
          "email": "admin_email@email.com",
          "orcid": "0000-0000-0000-0001"
        }
      ],
      "users": [
        {
          "node": "User",
          "username": "my username",
          "email": "user@email.com",
          "orcid": "0000-0000-0000-0002"
        }
      ]
    }
    ```
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
        Group node

        Parameters
        ----------
        name: str
            Group name
        admins: List[User]
            List of administrators for this group
        users: List[User])
            List of users in this group
        """
        super().__init__(node="Group")
        self._json_attrs = replace(self._json_attrs, name=name, admins=admins, users=users)
        self.validate()

    # ------------------ Properties ------------------

    @property
    def name(self) -> str:
        """
        Name of the group

        Returns
        -------
         group name: str
            name of the group node
        """
        return self._json_attrs.name

    @property
    def admins(self) -> List[Any]:
        """
        list of admins (user nodes) for this group

        Returns
        -------
        admin list: List[Any]
            list of admins (user nodes) for the Group
        """
        return self._json_attrs.admins

    @property
    def users(self) -> List[Any]:
        """
        users that belong to this group

        Returns
        -------
         users list: List[Any]
            list of users that belong to this group
        """
        return self._json_attrs.users

    @property
    def notes(self) -> str:
        """
        groups notes

        Returns
        -------
        group notes: str
            Notes attached to this group node
        """
        return self._json_attrs.notes
