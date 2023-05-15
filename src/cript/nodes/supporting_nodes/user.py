from dataclasses import dataclass, replace

from cript.nodes.uuid_base import UUIDBaseNode


class User(UUIDBaseNode):
    """
    The [User node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)
    represents any researcher or individual who interacts with the CRIPT platform.
    It serves two main purposes:
    1. It plays a core role in permissions (access control)
    1. It provides a traceable link to the individual who has contributed or edited data within the database


    | attribute  | type        | example                    | description                                | required | vocab |
    |------------|-------------|----------------------------|--------------------------------------------|----------|-------|
    | url        | str         |                            | unique ID of the node                      | True     |       |
    | username   | str         | "john_doe"                 | User’s name                                | True     |       |
    | email      | str         | "user@cript.com"           | email of the user                          | True     |       |
    | orcid      | str         | "0000-0000-0000-0000"      | ORCID ID of the user                       | True     |       |
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

    Warnings
    -------
    * A User cannot be created or modified using the Python SDK.
    * A User node is a **read-only** node that can only be deserialized from API JSON response to Python node.
    * The User node cannot be instantiated and within the Python SDK.
    * Attempting to edit the user node will result in an `Attribute Error`

    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        """
        all User attributes
        """

        created_at: str = ""
        email: str = ""
        model_version: str = ""
        orcid: str = ""
        picture: str = ""
        updated_at: str = ""
        username: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, username: str, email: str, orcid: str, **kwargs):
        """
        Json from CRIPT API to be converted to a node
        optionally the group can be None if the user doesn't have a group

        Parameters
        ----------
        username: str
            user username
        email: str
            user email
        orcid: str
            user ORCID
        """
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, username=username, email=email, orcid=orcid)

        self.validate()

    # ------------------ properties ------------------

    @property
    def created_at(self) -> str:
        return self._json_attrs.created_at

    @property
    def email(self) -> str:
        """
        user's email

        Raises
        ------
        AttributeError

        Returns
        -------
        user email: str
            User node email
        """
        return self._json_attrs.email

    @property
    def model_version(self) -> str:
        return self._json_attrs.model_version

    @property
    def orcid(self) -> str:
        """
        users [ORCID](https://orcid.org/)

        Raises
        ------
        AttributeError

        Returns
        -------
        ORCID: str
            user's ORCID
        """
        return self._json_attrs.orcid

    @property
    def picture(self) -> str:
        return self._json_attrs.picture

    @property
    def updated_at(self) -> str:
        return self._json_attrs.updated_at

    @property
    def username(self) -> str:
        """
        username of the User node

        Raises
        ------
        AttributeError

        Returns
        -------
        username: str
            username of the User node
        """
        return self._json_attrs.username
