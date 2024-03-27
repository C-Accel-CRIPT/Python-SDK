from dataclasses import dataclass, field, replace
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.subobjects.algorithm import Algorithm
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.software import Software
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class SoftwareConfiguration(UUIDBaseNode):
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
    {
       "node":["SoftwareConfiguration"],
       "uid":"_:f0dc3415-635d-4590-8b1f-cd65ad8ab3fe"
       "software":{
          "name":"SOMA",
          "node":["Software"],
          "source":"https://gitlab.com/InnocentBug/SOMA",
          "uid":"_:5bf9cb33-f029-4d1b-ba53-3602036e4f75",
          "uuid":"5bf9cb33-f029-4d1b-ba53-3602036e4f75",
          "version":"0.7.0"
       }
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        software: Optional[Union[Software, UIDProxy]] = None
        algorithm: List[Union[Algorithm, UIDProxy]] = field(default_factory=list)
        notes: str = ""
        citation: List[Union[Citation, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, software: Union[Software, UIDProxy], algorithm: Optional[List[Union[Algorithm, UIDProxy]]] = None, notes: str = "", citation: Union[List[Union[Citation, UIDProxy]], None] = None, **kwargs):
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
        >>> import cript
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)

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
        new_json_attrs = replace(self._json_attrs, software=software, algorithm=algorithm, notes=notes, citation=citation)
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def software(self) -> Union[Software, None, UIDProxy]:
        """
        Software used

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        >>> my_software_configuration.software = my_software

        Returns
        -------
        Union[Software, None]
            Software node used
        """
        return self._json_attrs.software

    @software.setter
    @beartype
    def software(self, new_software: Union[Software, None, UIDProxy]) -> None:
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
    @beartype
    def algorithm(self) -> List[Union[Algorithm, UIDProxy]]:
        """
        list of Algorithms used

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        >>> my_software_configuration.algorithm = [my_algorithm]

        Returns
        -------
        List[Algorithm]
            list of algorithms used
        """
        return self._json_attrs.algorithm.copy()

    @algorithm.setter
    @beartype
    def algorithm(self, new_algorithm: List[Union[Algorithm, UIDProxy]]) -> None:
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
    @beartype
    def notes(self) -> str:
        """
        miscellaneous information, or custom data structure (e.g.; JSON). Notes can be written in plain text or JSON

        Examples
        --------
        ### Plain Text
        ```json
        my_software_configuration.notes = "these are my awesome notes!"
        ```

        Examples
        -------
        >>> import cript
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        >>> my_software_configuration.notes = "{'notes subject': 'notes contents'}"

        Returns
        -------
        str
            notes
        """
        return self._json_attrs.notes

    @notes.setter
    @beartype
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
    @beartype
    def citation(self) -> List[Union[Citation, UIDProxy]]:
        """
        list of Citation sub-objects for the Software_Configuration

        Examples
        --------
        >>> import cript
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
        >>> my_citation = Citation("reference", my_reference)
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        >>> my_software_configuration.citation = [my_citation]

        Returns
        -------
        List[Citation]
            list of Citations
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    @beartype
    def citation(self, new_citation: List[Union[Citation, UIDProxy]]) -> None:
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
