from dataclasses import dataclass, field, replace
from typing import Any, List

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Data(PrimaryBaseNode):
    """
    ## Definition
    A  [Data node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=13)
     node contains the meta-data to describe raw data that is beyond a single value, (i.e. n-dimensional data).
     Each `Data` node must be linked to a single `Experiment` node.

    ## Available Sub-Objects
    * [Citation](../../subobjects/citation)

    ## Attributes
    | Attribute             | Type                                                | Example                    | Description                                                                             | Required |
    |-----------------------|-----------------------------------------------------|----------------------------|-----------------------------------------------------------------------------------------|----------|
    | experiment            | [Experiment](experiment.md)                         |                            | Experiment the data belongs to                                                          | True     |
    | name                  | str                                                 | `"my_data_name"`           | Name of the data node                                                                   | True     |
    | type                  | str                                                 | `"nmr_h1"`                 | Pick from [CRIPT data type controlled vocabulary](https://criptapp.org/keys/data-type/) | True     |
    | file                 | List[[File](../supporting_nodes/file.md)]           | `[file_1, file_2, file_3]` | list of file nodes                                                                      | False    |
    | sample_preparation    | [Process](process.md)                               |                            |                                                                                         | False    |
    | computation          | List[[Computation](computation.md)]                 |                            | data produced from this Computation method                                              | False    |
    | computation_process | [Computational Process](./computational_process.md) |                            | data was produced from this computation process                                         | False    |
    | material             | List[[Material](./material.md)]                     |                            | materials with attributes associated with the data node                                 | False    |
    | process               | List[[Process](./process.md)]                       |                            | processes with attributes associated with the data node                                 | False    |
    | citation             | [Citation](../subobjects/citation.md)               |                            | reference to a book, paper, or scholarly work                                           | False    |

    Example
    --------
    ```python
    # list of file nodes
    my_files_list = [
        # create file node
        cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )
    ]

    # create data node with required arguments
    my_data = cript.Data(name="my data name", type="afm_amp", file=[simple_file_node])
    ```

    ## JSON
    ```json
    "data": [
        {
        "node": "Data",
        "name": "WPI unheated film FTIR",
        "type": "null"
        }
    ]
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Data attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        file: List[Any] = field(default_factory=list)
        sample_preparation: Any = field(default_factory=list)
        computation: List[Any] = field(default_factory=list)
        computation_process: Any = field(default_factory=list)
        material: List[Any] = field(default_factory=list)
        process: List[Any] = field(default_factory=list)
        citation: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        file: List[Any],
        sample_preparation: Any = None,
        computation: List[Any] = None,
        computation_process: Any = None,
        material: List[Any] = None,
        process: List[Any] = None,
        citation: List[Any] = None,
        notes: str = "",
        **kwargs
    ):
        super().__init__(name=name, notes=notes, **kwargs)

        if file is None:
            file = []

        if sample_preparation is None:
            sample_preparation = []

        if computation is None:
            computation = []

        if computation_process is None:
            computation_process = []

        if material is None:
            material = []

        if process is None:
            process = []

        if citation is None:
            citation = []

        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            file=file,
            sample_preparation=sample_preparation,
            computation=computation,
            computation_process=computation_process,
            material=material,
            process=process,
            citation=citation,
        )

        self.validate()

    # ------------------ Properties ------------------
    @property
    def type(self) -> str:
        """
        Type of data node. The data type must come from [CRIPT data type vocabulary]()

        Example
        -------
        ```python
        data.type = "afm_height"
        ```

        Returns
        -------
        data type: str
            data type for the data node must come from CRIPT controlled vocabulary
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_data_type: str) -> None:
        """
        set the data type.
        The data type must come from [CRIPT data type vocabulary]()

        Parameters
        ----------
        new_data_type: str
            new data type to replace the current data type

        Returns
        -------
        None
        """
        # TODO validate that the data type is valid from CRIPT controlled vocabulary
        new_attrs = replace(self._json_attrs, type=new_data_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def file(self) -> List[Any]:
        """
        get the list of files for this data node

        Examples
        --------
        ```python
        create a list of file nodes
        my_new_files = [
            # file with link source
            cript.File(
                source="https://pubs.acs.org/doi/10.1021/acscentsci.3c00011",
                type="computation_config",
                extension=".pdf",
                data_dictionary="my second file data dictionary",
            ),
        ]

        data_node.file = my_new_files
        ```

        Returns
        -------
        List[File]
            list of files for this data node
        """
        return self._json_attrs.file.copy()

    @file.setter
    def file(self, new_file_list: List[Any]) -> None:
        """
        set the list of file for this data node

        Parameters
        ----------
        new_files_list: List[File]
            new list of file nodes to replace the current list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, file=new_file_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def sample_preparation(self) -> Any:
        """
        The sample preperation for this data node

        Returns
        -------
        sample_preparation: Process
            sample preparation for this data node
        """
        return self._json_attrs.sample_preparation

    @sample_preparation.setter
    def sample_preparation(self, new_sample_preparation: Any) -> None:
        """
        set sample_preparation

        Parameters
        ----------
        new_sample_preparation: Process
            new_sample_preparation to replace the current one for this node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, sample_preparation=new_sample_preparation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computation(self) -> List[Any]:
        """
        list of computation nodes for this material node

        Returns
        -------
        None
            list of computation nodes
        """
        return self._json_attrs.computation.copy()

    @computation.setter
    def computation(self, new_computation_list: List[Any]) -> None:
        """
        set list of computation  for this data node

        Parameters
        ----------
        new_computation_list: List[Computation]
            new computation list to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation=new_computation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computation_process(self) -> Any:
        """
        The computation_process for this data node

        Returns
        -------
        ComputationalProcess
            computational process node for this data node
        """
        return self._json_attrs.computation_process

    @computation_process.setter
    def computation_process(self, new_computation_process: Any) -> None:
        """
        set the computational process

        Parameters
        ----------
        new_computation_process: ComputationalProcess

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation_process=new_computation_process)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def material(self) -> List[Any]:
        """
        List of materials for this node

        Returns
        -------
        List[Material]
            list of material
        """
        return self._json_attrs.material.copy()

    @material.setter
    def material(self, new_material_list: List[Any]) -> None:
        """
        set the list of materials for this data node

        Parameters
        ----------
        new_material_list: List[Material]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, material=new_material_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def process(self) -> List[Any]:
        """
        list of [Process nodes](./process.md) for this data node

        Notes
        -----
        Please note that while the process attribute of the data node is currently set to `Any`
        the software still expects a Process node in the data's process attribute
        > It is currently set to `Any` to avoid the circular import error

        Returns
        -------
        List[Process]
            list of process for the data node
        """
        return self._json_attrs.process.copy()

    @process.setter
    def process(self, new_process_list: List[Any]) -> None:
        """
        set the list of process for this data node

        Parameters
        ----------
        new_process_list: List[Process]
            new list of Process

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, process=new_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Any]:
        """
        List of [citation](../supporting_nodes/citations.md) within the data node

        Example
        -------
        ```python
        # create a reference node
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

        # create a citation list to house all the reference nodes
        my_citation = cript.Citation(type="derived_from", reference=my_reference)

        # add citations to data node
        my_data.citation = my_citations
        ```

        Returns
        -------
        List[Citation]
            list of citations for this data node
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Any]) -> None:
        """
        set the list of citation

        Parameters
        ----------
        new_citation_list: List[Citation]
            new list of citation to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)
