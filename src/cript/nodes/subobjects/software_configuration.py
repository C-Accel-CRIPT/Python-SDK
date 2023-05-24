from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.algorithm import Algorithm
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.software import Software


class SoftwareConfiguration(BaseNode):
    """
    ## Definition

    The [software_configuration](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=24)
    sub-object includes software and the set of algorithms to execute computation or computational_process.

    ---

    ## Can Be Added To:
    * [Computation](../../primary_nodes/computation)
    * [Computation_Process](../../primary_nodes/computation_process)

    ## Available sub-objects:
    * [Algorithm](../algorithm)
    * [Citation](../citation)

    ---

    ## Attributes

    | keys                                             | type            | example | description                                                      | required | vocab |
    |--------------------------------------------------|-----------------|---------|------------------------------------------------------------------|----------|-------|
    | software                                         | Software        |         | software used                                                    | True     |       |
    | algorithms                                       | list[Algorithm] |         | algorithms used                                                  |          |       |
    | notes                                            | str             |         | miscellaneous information, or custom data structure (e.g.; JSON) |          |       |
    | citation                                         | list[Citation]  |         | reference to a book, paper, or scholarly work                    |          |       |


    ## JSON Representation
    ```json

    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        software: Union[Software, None] = None
        algorithm: List[Algorithm] = field(default_factory=list)
        notes: str = ""
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, software: Software, algorithm: Union[List[Algorithm], None] = None, notes: str = "", citation: Union[List[Citation], None] = None, **kwargs):
        """
        Create Software_Configuration sub-object


        Parameters
        ----------
        software : Software
            Software node used for the Software_Configuration
        algorithm : Union[List[Algorithm], None], optional
            algorithm used for the Software_Configuration, by default None
        notes : str, optional
            plain text notes, by default ""
        citation : Union[List[Citation], None], optional
            list of Citation sub-object, by default None

        Examples
        ---------
        ```python
        import cript

        my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")

        my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        ```

        Returns
        -------
        None
            Create Software_Configuration sub-object
        """
        if algorithm is None:
            algorithm = []
        if citation is None:
            citation = []
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, software=software, algorithm=algorithm, notes=notes, citation=citation)
        self.validate()

    @property
    def software(self) -> Union[Software, None]:
        """
        Software used

        Examples
        --------
        ```python
        my_software = cript.Software(
            name="my software name", version="v1.0.0", source="https://myurl.com"
        )

        my_software_configuration.software = my_software
        ```

        Returns
        -------
        Union[Software, None]
            Software node used
        """
        return self._json_attrs.software

    @software.setter
    def software(self, new_software: Union[Software, None]) -> None:
        """
        set the Software used

        Parameters
        ----------
        new_software : Union[Software, None]
            new Software node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, software=new_software)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def algorithm(self) -> List[Algorithm]:
        """
        list of Algorithms used

        Examples
        --------
        ```python
        my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")

        my_software_configuration.algorithm = [my_algorithm]
        ```

        Returns
        -------
        List[Algorithm]
            list of algorithms used
        """
        return self._json_attrs.algorithm.copy()

    @algorithm.setter
    def algorithm(self, new_algorithm: List[Algorithm]) -> None:
        """
        set the list of Algorithms

        Parameters
        ----------
        new_algorithm : List[Algorithm]
            list of algorithms

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, algorithm=new_algorithm)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def notes(self) -> str:
        """
        miscellaneous information, or custom data structure (e.g.; JSON). Notes can be written in plain text or JSON

        Examples
        --------
        ### Plain Text
        ```json
        my_software_configuration.notes = "these are my awesome notes!"
        ```

        ### JSON Notes
        ```python
        my_software_configuration.notes = "{'notes subject': 'notes contents'}"
        ```

        Returns
        -------
        str
            notes
        """
        return self._json_attrs.notes

    @notes.setter
    def notes(self, new_notes: str) -> None:
        """
        set notes for Software_configuration

        Parameters
        ----------
        new_notes : str
            new notes in plain text or JSON

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, notes=new_notes)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Citation]:
        """
        list of Citation sub-objects for the Software_Configuration

        Examples
        --------
        ```python
        title = "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        title += "SOft coarse grained Monte-Carlo Acceleration (SOMA)"

        # create reference node
        my_reference = cript.Reference(
            type"journal_article",
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

        # create citation sub-object and add reference to it
        my_citation = Citation("reference", my_reference)

        # add citation to algorithm node
        my_software_configuration.citation = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            list of Citations
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]) -> None:
        """
        set the Citation sub-object

        Parameters
        ----------
        new_citation : List[Citation]
            new list of Citation sub-objects

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
