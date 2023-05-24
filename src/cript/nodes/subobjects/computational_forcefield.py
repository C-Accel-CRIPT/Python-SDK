from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.data import Data
from cript.nodes.subobjects.citation import Citation


class ComputationalForcefield(BaseNode):
    """
    ## Definition
    A [Computational Forcefield Subobject](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=23)
    is a mathematical model that describes the forces between atoms and molecules.
    It is used in computational chemistry and molecular dynamics simulations to predict the behavior of materials.
    Forcefields are typically based on experimental data or quantum mechanical calculations,
    and they are often used to study the properties of materials such as their structure, dynamics, and reactivity.

    ## Attributes
    | attribute              | type           | example                                                                | description                                                              | required | vocab |
    |------------------------|----------------|------------------------------------------------------------------------|--------------------------------------------------------------------------|----------|-------|
    | key                    | str            | CHARMM27                                                               | type of forcefield                                                       | True     | True  |
    | building_block         | str            | atom                                                                   | type of building block                                                   | True     | True  |
    | coarse_grained_mapping | str            | SC3 beads in MARTINI forcefield                                        | atom to beads mapping                                                    |          |       |
    | implicit_solvent       | str            | water                                                                  | Name of implicit solvent                                                 |          |       |
    | source                 | str            | package in GROMACS                                                     | source of forcefield                                                     |          |       |
    | description            | str            | OPLS forcefield with partial charges calculated via the LBCC algorithm | description of the forcefield and any modifications that have been added |          |       |
    | data                   | Data           |                                                                        | details of mapping schema and forcefield parameters                      |          |       |
    | citation               | list[Citation] |                                                                        | reference to a book, paper, or scholarly work                            |          |       |


    ## Can be Added To Primary Node:
    * Material node

    ## JSON Representation
    ```json
    {
        "node": ["ComputationalForcefield"],
        "key": "opls_aa",
        "building_block": "atom",
        "coarse_grained_mapping": "atom -> atom",
        "implicit_solvent": "no implicit solvent",
        "source": "local LigParGen installation",
        "description": "this is a test forcefield",
        "data": {
            "node":["Data"],
            "name":"my data name",
            "type":"afm_amp",
            "file":[
                {
                    "node":["File"],
                    "type":"calibration",
                    "source":"https://criptapp.org",
                    "extension":".csv",
                    "data_dictionary":"my file's data dictionary"
                }
            ]
        },
        "citation": {
            "node": ["Citation"],
            "type": "reference"
            "reference": {
                "node": ["Reference"],
                "type": "journal_article",
                "title": "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: SOft coarse grained Monte-Carlo Acceleration (SOMA)",
                "author": ["Ludwig Schneider", "Marcus Müller"],
                "journal": "Computer Physics Communications",
                "publisher": "Elsevier",
                "year": 2019,
                "pages": [463, 476],
                "doi": "10.1016/j.cpc.2018.08.011",
                "issn": "0010-4655",
                "website": "https://www.sciencedirect.com/science/article/pii/S0010465518303072",
            }
    }


    ```

    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        building_block: str = ""
        coarse_grained_mapping: str = ""
        implicit_solvent: str = ""
        source: str = ""
        description: str = ""
        data: List[Data] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, building_block: str, coarse_grained_mapping: str = "", implicit_solvent: str = "", source: str = "", description: str = "", data: List[Data] = None, citation: Union[List[Citation], None] = None, **kwargs):
        """
        instantiate a computational_forcefield subobject

        Parameters
        ----------
        key : str
            type of forcefield key must come from [CRIPT Controlled Vocabulary]()
        building_block : str
            type of computational_forcefield building_block must come from [CRIPT Controlled Vocabulary]()
        coarse_grained_mapping : str, optional
            atom to beads mapping, by default ""
        implicit_solvent : str, optional
            Name of implicit solvent, by default ""
        source : str, optional
            source of forcefield, by default ""
        description : str, optional
            description of the forcefield and any modifications that have been added, by default ""
        data : List[Data], optional
            details of mapping schema and forcefield parameters, by default None
        citation : Union[List[Citation], None], optional
            reference to a book, paper, or scholarly work, by default None


        Examples
        --------
        ```python
        my_computational_forcefield = cript.ComputationalForcefield(
            key="opls_aa",
            building_block="atom",
        )
        ```

        Returns
        -------
        None
            Instantiate a computational_forcefield subobject
        """
        if citation is None:
            citation = []
        super().__init__(**kwargs)

        if data is None:
            data = []

        self._json_attrs = replace(
            self._json_attrs,
            key=key,
            building_block=building_block,
            coarse_grained_mapping=coarse_grained_mapping,
            implicit_solvent=implicit_solvent,
            source=source,
            description=description,
            data=data,
            citation=citation,
        )
        self.validate()

    @property
    def key(self) -> str:
        """
        type of forcefield

        > Computational_Forcefield key must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_computational_forcefield.key = "amber"
        ```

        Returns
        -------
        str
            type of forcefield
        """
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str) -> None:
        """
        set key for this computational_forcefield

        Parameters
        ----------
        new_key : str
            computational_forcefield key

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def building_block(self) -> str:
        """
        type of building block

        > Computational_Forcefield building_block must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_computational_forcefield.building_block = "atom"
        ```

        Returns
        -------
        str
            type of building block
        """
        return self._json_attrs.building_block

    @building_block.setter
    def building_block(self, new_building_block: str) -> None:
        """
        type of building block

        Parameters
        ----------
        new_building_block : str
            new type of building block

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, building_block=new_building_block)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def coarse_grained_mapping(self) -> str:
        """
        atom to beads mapping

        Examples
        --------
        ```python
        my_computational_forcefield.coarse_grained_mapping = "SC3 beads in MARTINI forcefield"
        ```

        Returns
        -------
        str
            coarse_grained_mapping
        """
        return self._json_attrs.coarse_grained_mapping

    @coarse_grained_mapping.setter
    def coarse_grained_mapping(self, new_coarse_grained_mapping: str) -> None:
        """
        atom to beads mapping

        Parameters
        ----------
        new_coarse_grained_mapping : str
            new coarse_grained_mapping

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, coarse_grained_mapping=new_coarse_grained_mapping)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def implicit_solvent(self) -> str:
        """
        Name of implicit solvent

        Examples
        --------
        ```python
        my_computational_forcefield.implicit_solvent = "water"
        ```

        Returns
        -------
        str
            _description_
        """
        return self._json_attrs.implicit_solvent

    @implicit_solvent.setter
    def implicit_solvent(self, new_implicit_solvent: str) -> None:
        """
        set the implicit_solvent

        Parameters
        ----------
        new_implicit_solvent : str
            new implicit_solvent
        """
        new_attrs = replace(self._json_attrs, implicit_solvent=new_implicit_solvent)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def source(self) -> str:
        """
        source of forcefield

        Examples
        --------
        ```python
        my_computational_forcefield.source = "package in GROMACS"
        ```

        Returns
        -------
        str
            source of forcefield
        """
        return self._json_attrs.source

    @source.setter
    def source(self, new_source: str) -> None:
        """
        set the computational_forcefield

        Parameters
        ----------
        new_source : str
            new source of forcefield
        """
        new_attrs = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def description(self) -> str:
        """
        description of the forcefield and any modifications that have been added

        Examples
        --------
        ```python
        my_computational_forcefield.description = "OPLS forcefield with partial charges calculated via the LBCC algorithm"
        ```

        Returns
        -------
        str
            description of the forcefield and any modifications that have been added
        """
        return self._json_attrs.description

    @description.setter
    def description(self, new_description: str) -> None:
        """
        set this computational_forcefields description

        Parameters
        ----------
        new_description : str
            new computational_forcefields description

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, description=new_description)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> List[Data]:
        """
        details of mapping schema and forcefield parameters

        Examples
        --------
        ```python
        # create file nodes for the data node
        my_file = cript.File(
            source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
            type="calibration",
            extension=".pdf",
        )

        # create data node and add the file node to it
        my_data = cript.Data(
            name="my data node name",
            type="afm_amp",
            file=my_file,
        )

        # add data node to computational_forcefield subobject
        my_computational_forcefield.data = [my_data]
        ```

        Returns
        -------
        List[Data]
            list of data nodes for this computational_forcefield subobject
        """
        return self._json_attrs.data.copy()

    @data.setter
    def data(self, new_data: List[Data]) -> None:
        """
        set the data attribute of this computational_forcefield node

        Parameters
        ----------
        new_data : List[Data]
            new list of data nodes

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data=new_data)
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
            "journal_article",
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

        my_computational_forcefield.citation = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            computational_forcefield list of citations
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]) -> None:
        """
        set the citation subobject of the computational_forcefield subobject

        Parameters
        ----------
        new_citation : List[Citation]
            new citation subobject
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
