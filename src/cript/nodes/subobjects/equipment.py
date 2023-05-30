from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.condition import Condition
from cript.nodes.supporting_nodes.file import File


class Equipment(BaseNode):
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
    | condition  | list[Condition] |                                               | conditions under which the property was measured                               |          |       |
    | files       | list[File]      |                                               | list of file nodes to link to calibration or equipment specification documents |          |       |
    | citation   | list[Citation]  |                                               | reference to a book, paper, or scholarly work                                  |          |       |

    ## JSON Representation
    ```json

    ```

    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        description: str = ""
        condition: List[Condition] = field(default_factory=list)
        file: List[File] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, description: str = "", condition: Union[List[Condition], None] = None, file: Union[List[File], None] = None, citation: Union[List[Citation], None] = None, **kwargs) -> None:
        """
        create equipment sub-object

        Parameters
        ----------
        key : str
            Equipment key must come from [CRIPT Controlled Vocabulary]()
        description : str, optional
            additional details about the equipment, by default ""
        condition : Union[List[Condition], None], optional
            Conditions under which the property was measured, by default None
        file : Union[List[File], None], optional
            list of file nodes to link to calibration or equipment specification documents, by default None
        citation : Union[List[Citation], None], optional
            reference to a scholarly work, by default None

        Example
        -------
        ```python
        my_equipment = cript.Equipment(key="burner")
        ```

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
        self._json_attrs = replace(self._json_attrs, key=key, description=description, condition=condition, file=file, citation=citation)
        self.validate()

    @property
    def key(self) -> str:
        """
        scientific instrument

        > Equipment key must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_equipment = cript.Equipment(key="burner")
        ```

        Returns
        -------
        Equipment: str

        """
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str) -> None:
        """
        set the equipment key

        > Equipment key must come from [CRIPT Controlled Vocabulary]()

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
    def description(self) -> str:
        """
        description of the equipment

        Examples
        --------
        ```python
        my_equipment.description = "additional details about the equipment"
        ```

        Returns
        -------
        str
            additional description of the equipment
        """
        return self._json_attrs.description

    @description.setter
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
    def condition(self) -> List[Condition]:
        """
        conditions under which the property was measured

        Examples
        --------
        ```python
        # create a Condition sub-object
        my_condition = cript.Condition(
            key="temperature",
            type="value",
            value=22,
            unit="C",
        )

        # add Condition sub-object to Equipment sub-object
        my_equipment.condition = [my_condition]
        ```

        Returns
        -------
        List[Condition]
            list of Condition sub-objects
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition: List[Condition]) -> None:
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
    def file(self) -> List[File]:
        """
        list of file nodes to link to calibration or equipment specification documents

        Examples
        --------
        ```python
        # create a file node to be added to the equipment sub-object
        my_file = cript.File(
            source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
            type="calibration",
            extension=".pdf",
        )

        # add file node to equipment sub-object
        my_equipment.file = [my_file]

        ```

        Returns
        -------
        List[File]
            list of file nodes
        """
        return self._json_attrs.file.copy()

    @file.setter
    def file(self, new_file: List[File]) -> None:
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
    def citation(self) -> List[Citation]:
        """
        reference to a book, paper, or scholarly work

        Examples
        --------
        ```python
        # create reference node for the citation node
        title = "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        title += "SOft coarse grained Monte-Carlo Acceleration (SOMA)"

        my_reference = cript.Reference(
            type="journal_article",
            title=title,
            author=["Ludwig Schneider", "Marcus Müller"],
            journal="Computer Physics Communications",
            publisher="Elsevier",
            year=2019,
            pages=[463, 476],
            doi="10.1016/j.cpc.2018.08.011",
            issn="0010-4655",
            website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        )

        # create citation node and add reference node to it
        my_citation = cript.Citation(type="reference", reference=my_reference)

        # add citation subobject to equipment
        my_equipment.citation = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            list of Citation subobjects
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]) -> None:
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
