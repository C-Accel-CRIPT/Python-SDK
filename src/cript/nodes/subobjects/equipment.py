from dataclasses import dataclass, field, replace
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.condition import Condition
from cript.nodes.supporting_nodes.file import File
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Equipment(UUIDBaseNode):
    """
    ## Definition
    An [Equipment](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=23)
    sub-object specifies the physical instruments, tools, glassware, etc. used in a process.

    ---

    ## Can Be Added To:
    * [Process node](../../primary_nodes/process)

    ## Available sub-objects:
    * [Condition](../condition)
    * [Citation](../citation)

    ---

    ## Attributes

    | attribute   | type            | example                                       | description                                                                    | required | vocab |
    |-------------|-----------------|-----------------------------------------------|--------------------------------------------------------------------------------|----------|-------|
    | key         | str             | hot plate                                     | material                                                                       | True     | True  |
    | description | str             | Hot plate with silicon oil bath with stir bar | additional details about the equipment                                         |          |       |
    | condition   | list[Condition] |                                               | conditions under which the property was measured                               |          |       |
    | files       | list[File]      |                                               | list of file nodes to link to calibration or equipment specification documents |          |       |
    | citation    | list[Citation]  |                                               | reference to a book, paper, or scholarly work                                  |          |       |

    ## JSON Representation
    ```json
    {
       "node":["Equipment"],
       "description": "my equipment description",
       "key":"burner",
       "uid":"_:19708284-1bd7-42e4-b8b2-da7ea0bc2ac9",
       "uuid":"19708284-1bd7-42e4-b8b2-da7ea0bc2ac9"
    }
    ```

    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        description: str = ""
        condition: List[Union[Condition, UIDProxy]] = field(default_factory=list)
        file: List[Union[File, UIDProxy]] = field(default_factory=list)
        citation: List[Union[Citation, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, key: str, description: str = "", condition: Optional[List[Union[Condition, UIDProxy]]] = None, file: Optional[List[Union[File, UIDProxy]]] = None, citation: Optional[List[Union[Citation, UIDProxy]]] = None, **kwargs) -> None:
        """
        create equipment sub-object

        Parameters
        ----------
        key : str
            Equipment key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/equipment_key)
        description : str, optional
            additional details about the equipment, by default ""
        condition : Union[List[Condition], None], optional
            Conditions under which the property was measured, by default None
        file : Union[List[File], None], optional
            list of file nodes to link to calibration or equipment specification documents, by default None
        citation : Union[List[Citation], None], optional
            reference to a scholarly work, by default None

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")

        Returns
        -------
        None
            instantiate equipment sub-object
        """
        if condition is None:
            condition = []
        if file is None:
            file = []
        if citation is None:
            citation = []
        super().__init__(**kwargs)
        new_json_attrs = replace(self._json_attrs, key=key, description=description, condition=condition, file=file, citation=citation)
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def key(self) -> str:
        """
        scientific instrument

        Equipment key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/equipment_key)

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")
        >>> my_equipment.key = "hot_plate"

        Returns
        -------
        Equipment: str
        """
        return self._json_attrs.key

    @key.setter
    @beartype
    def key(self, new_key: str) -> None:
        """
        set the equipment key

        Parameters
        ----------
        new_key : str
            equipment sub-object key

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def description(self) -> str:
        """
        description of the equipment

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")
        >>> my_equipment.description = "additional details about the equipment"

        Returns
        -------
        str
            additional description of the equipment
        """
        return self._json_attrs.description

    @description.setter
    @beartype
    def description(self, new_description: str) -> None:
        """
        set this equipments description

        Parameters
        ----------
        new_description : str
            equipment description

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, description=new_description)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def condition(self) -> List[Union[Condition, UIDProxy]]:
        """
        conditions under which the property was measured

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_equipment.condition = [my_condition]

        Returns
        -------
        List[Condition]
            list of Condition sub-objects
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    @beartype
    def condition(self, new_condition: List[Union[Condition, UIDProxy]]) -> None:
        """
        set a list of Conditions for the equipment sub-object

        Parameters
        ----------
        new_condition : List[Condition]
            list of Condition sub-objects

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, condition=new_condition)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def file(self) -> List[Union[File, UIDProxy]]:
        """
        list of file nodes to link to calibration or equipment specification documents

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
        ...     type="calibration",
        ...     extension=".pdf",
        ... )
        >>> my_equipment.file = [my_file]

        Returns
        -------
        List[File]
            list of file nodes
        """
        return self._json_attrs.file.copy()

    @file.setter
    @beartype
    def file(self, new_file: List[Union[File, UIDProxy]]) -> None:
        """
        set the file node for the equipment subobject

        Parameters
        ----------
        new_file : List[File]
            list of File nodes

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, file=new_file)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def citation(self) -> List[Union[Citation, UIDProxy]]:
        """
        reference to a book, paper, or scholarly work

        Examples
        --------
        >>> import cript
        >>> my_equipment = cript.Equipment(key="burner")
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     type="journal_article",
        ...     title=title,
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="reference", reference=my_reference)
        >>> my_equipment.citation = [my_citation]

        Returns
        -------
        List[Citation]
            list of Citation subobjects
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    @beartype
    def citation(self, new_citation: List[Union[Citation, UIDProxy]]) -> None:
        """
        set the citation subobject for this equipment subobject

        Parameters
        ----------
        new_citation : List[Citation]
            list of Citation subobjects

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
