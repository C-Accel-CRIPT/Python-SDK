from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import File, Process, Computation, ComputationalProcess, Material, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Data(PrimaryBaseNode):
    """
    ## Definition

    A  [Data node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=13)
     node contains the meta-data to describe raw data that is beyond a single value, (i.e. n-dimensional data).
     Each `Data` node must be linked to a single `Experiment` node.

    ## Sub-Objects

    * [Citation](../../subobjects/citation)

    ## Attributes

    | Attribute             | Type                                                | Example                    | Description                                                                             | Required |
    |-----------------------|-----------------------------------------------------|----------------------------|-----------------------------------------------------------------------------------------|----------|
    | experiment            | [Experiment](experiment.md)                         |                            | Experiment the data belongs to                                                          | True     |
    | name                  | str                                                 | `"my_data_name"`           | Name of the data node                                                                   | True     |
    | type                  | str                                                 | `"nmr_h1"`                 | Pick from [CRIPT data type controlled vocabulary](https://criptapp.org/keys/data-type/) | True     |
    | files                 | List[[File](../supporting_nodes/file.md)]           | `[file_1, file_2, file_3]` | list of file nodes                                                                      | False    |
    | sample_preperation    | [Process](process.md)                               |                            |                                                                                         | False    |
    | computations          | List[[Computation](computation.md)]                 |                            | data produced from this Computation method                                              | False    |
    | computational_process | [Computational Process](./computational_process.md) |                            | data was produced from this computation process                                         | False    |
    | materials             | List[[Material](./material.md)]                     |                            | materials with attributes associated with the data node                                 | False    |
    | process               | List[[Process](./process.md)]                       |                            | processes with attributes associated with the data node                                 | False    |
    | citations             | [Citation](../subobjects/citation.md)               |                            | reference to a book, paper, or scholarly work                                           | False    |


    Examples
    --------
    ```python
    # create list of files needed for this data node
    my_files_list = [
        # create file node
            # source could be either a web URL or local file path
        my_file = cript.File(
        source="https://criptapp.org",
        type="calibration",
        extension=".csv",
        data_dictionary="my file's data dictionary"
        )
    ]

    # create a process node
    my_process = cript.Process(name="my process name", type="affinity_pure")




        my_complex_data = cript.Data(
        name="my complex data node name",
        type="afm_amp",
        files=my_files_list,
        sample_preperation=simple_process_node,
        computations=[simple_computation_node],
        computational_process=[simple_computational_process_node],
        materials=[simple_material_node],
        processes=[simple_process_node],
        citations=[simple_citation_node],
    )
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
        files: List[Any] = field(default_factory=list)
        sample_preperation: Any = field(default_factory=list)
        computations: List[Any] = field(default_factory=list)
        computational_process: Any = field(default_factory=list)
        materials: List[Any] = field(default_factory=list)
        processes: List[Any] = field(default_factory=list)
        citations: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        files: List[Any],
        sample_preperation: Any = None,
        computations: List[Any] = None,
        computational_process: Any = None,
        materials: List[Any] = None,
        processes: List[Any] = None,
        citations: List[Any] = None,
        notes: str = "",
        **kwargs
    ):
        super().__init__(node="Data", name=name, notes=notes)

        if files is None:
            files = []

        if sample_preperation is None:
            sample_preperation = []

        if computations is None:
            computations = []

        if computational_process is None:
            computational_process = []

        if materials is None:
            materials = []

        if processes is None:
            processes = []

        if citations is None:
            citations = []

        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            files=files,
            sample_preperation=sample_preperation,
            computations=computations,
            computational_process=computational_process,
            materials=materials,
            processes=processes,
            citations=citations,
        )

        self.validate()

    # ------------------ Properties ------------------
    @property
    def type(self) -> str:
        """
        Type of data node. The data type must come from [CRIPT data type vocabulary]()

        Example
        -------
        #### Get data type
        ```python
        print(data.type)
        ```

        #### Set data type
        ```python
        data.type = "afm_height"
        ```

        Returns
        -------
        data type: str
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
    def files(self) -> List[Any]:
        """
        get the list of files for this data node

        Examples
        --------
        #### Get data.files
        ```python
        print(my_data.file)
        ```
        #### Set data.files
        ```python
        my_new_files = [
            # file with link source
            cript.File(
                source="https://pubs.acs.org/doi/10.1021/acscentsci.3c00011",
                type="computation_config",
                extension=".pdf",
                data_dictionary="my second file data dictionary",
            ),
        ]

        data_node.files = my_new_files
        ```

        Returns
        -------
        List[File]
        """
        return self._json_attrs.files.copy()

    @files.setter
    def files(self, new_files_list: List[Any]) -> None:
        """
        set the list of files for this data node

        Parameters
        ----------
        new_files_list: List[File]
            new list of file nodes to replace the current list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, files=new_files_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def sample_preperation(self) -> Any:
        """
        get the sample preperation for this data node

        Returns
        -------
        None
        """
        return self._json_attrs.sample_preperation

    @sample_preperation.setter
    def sample_preperation(self, new_sample_preperation: Any) -> None:
        """
        set sample_preperation

        Parameters
        ----------
        new_sample_preperation: Process
            new_sample_preperation to replace the current one for this node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, sample_preperation=new_sample_preperation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computations(self) -> List[Any]:
        """
        get a list of computation nodes

        Returns
        -------
        None
        """
        return self._json_attrs.computations.copy()

    @computations.setter
    def computations(self, new_computation_list: List[Any]) -> None:
        """
        set list of computations  for this data node

        Parameters
        ----------
        new_computation_list: List[Computation]
            new computation list to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computations=new_computation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computational_process(self) -> Any:
        """
        get the computational_process for this data node

        Returns
        -------
        None
        """
        return self._json_attrs.computational_process

    @computational_process.setter
    def computational_process(self, new_computational_process: Any) -> None:
        """
        set the computational process

        Parameters
        ----------
        new_computational_process: ComputationalProcess

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computational_process=new_computational_process)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def materials(self) -> List[Any]:
        """
        gets a list of materials for this node

        Returns
        -------
        List[Material]
        """
        return self._json_attrs.materials.copy()

    @materials.setter
    def materials(self, new_materials_list: List[Any]) -> None:
        """
        set the list of materials for this data node

        Parameters
        ----------
        new_materials_list: List[Material]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, materials=new_materials_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def processes(self) -> List[Any]:
        """
        list of [Processes nodes](./process.md) for this data node

        Notes
        -----
        Please note that while the process attribute of the data node is currently set to `Any`
        the software still expects a Process node in the data's process attribute

        > It is currently set to `Any` to avoid the circular import error

        Returns
        -------
        None
        """
        return self._json_attrs.processes.copy()

    @processes.setter
    def processes(self, new_process_list: List[Any]) -> None:
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
        new_attrs = replace(self._json_attrs, processes=new_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Any]:
        """
        List of [citations](../supporting_nodes/citations.md) within the data node

        Example
        -------
        #### Get data.citations
        ```python
        print(my_data.citations)
        ```

        #### Set data.citations
        ```python
        # create a reference node
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

        # create a citation list to house all the reference nodes
        my_citation = cript.Citation(type="derived_from", reference=my_reference)

        # add citations to data node
        my_data.citations = my_citations
        ```

        Returns
        -------
        List[Citation]
        """
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations_list: List[Any]) -> None:
        """
        set the list of citations

        Parameters
        ----------
        new_citations_list: List[Citation]
            new list of citations to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citations=new_citations_list)
        self._update_json_attrs_if_valid(new_attrs)
