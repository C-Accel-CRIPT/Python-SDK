from dataclasses import dataclass, replace

from beartype import beartype

from cript.nodes.uuid_base import UUIDBaseNode


class Software(UUIDBaseNode):
    """
    ## Definition

    The [Software](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=16)
    node contains metadata for a computation tool, code, programming language, or software package.

    Similar to the [reference](../../primary_nodes/reference) node, the software node does not contain the base
    attributes and is meant to always be public and static.

    ---

    ## Can Be Added To:
    * [Software_Configuration](../../subobjects/software_configuration)

    ## Available sub-objects
    * None

    ---

    ## Attributes

    | attribute | type | example    | description                   | required | vocab |
    |-----------|------|------------|-------------------------------|----------|-------|
    | name      | str  | LAMMPS     | type of literature            | True     |       |
    | version   | str  | 23Jun22    | software version              | True     |       |
    | source    | str  | lammps.org | source of software            |          |       |

    ## JSON Representation
    ```json
    {
       "name":"SOMA",
       "node":["Software"],
       "version":"0.7.0"
       "source":"https://gitlab.com/InnocentBug/SOMA",
       "uid":"_:f2ec4bf2-96aa-48a3-bfbc-d1d3f090583b",
       "uuid":"f2ec4bf2-96aa-48a3-bfbc-d1d3f090583b",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        name: str = ""
        version: str = ""
        source: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, name: str, version: str, source: str = "", **kwargs):
        """
        create Software node

        Parameters
        ----------
        name : str
            Software name
        version : str
            Software version
        source : str, optional
            Software source, by default ""

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(
        ...     name="my software name", version="v1.0.0", source="https://myurl.com"
        ... )

        Returns
        -------
        None
            create Software node
        """
        super().__init__(**kwargs)

        new_json_attrs = replace(self._json_attrs, name=name, version=version, source=source)
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def name(self) -> str:
        """
        Software name

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(
        ...     name="my software name", version="v1.0.0", source="https://myurl.com"
        ... )
        >>> my_software.name = "my software name"

        Returns
        -------
        str
            Software name
        """
        return self._json_attrs.name

    @name.setter
    @beartype
    def name(self, new_name: str) -> None:
        """
        set the name of the Software node

        Parameters
        ----------
        new_name : str
            new Software name

        Returns
        -------
        None
        """
        new_attr = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attr)

    @property
    @beartype
    def version(self) -> str:
        """
        Software version

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(
        ...     name="my software name", version="v1.0.0", source="https://myurl.com"
        ... )
        >>> my_software.version = "1.2.3"

        Returns
        -------
        str
            Software version
        """
        return self._json_attrs.version

    @version.setter
    @beartype
    def version(self, new_version: str) -> None:
        """
        set the Software version

        Parameters
        ----------
        new_version : str
            new Software version

        Returns
        -------
        None
        """
        new_attr = replace(self._json_attrs, version=new_version)
        self._update_json_attrs_if_valid(new_attr)

    @property
    @beartype
    def source(self) -> str:
        """
        Software source

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(
        ...     name="my software name", version="v1.0.0", source="https://myurl.com"
        ... )
        >>> my_software.source = "https://myNewWebsite.com"

        Returns
        -------
        str
            Software source
        """
        return self._json_attrs.source

    @source.setter
    @beartype
    def source(self, new_source: str) -> None:
        """
        set the Software source

        Parameters
        ----------
        new_source : str
            new Software source

        Returns
        -------
        None
        """
        new_attr = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attr)
