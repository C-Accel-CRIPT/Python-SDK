from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import File, Process, Computation, ComputationalProcess, Material, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Data(PrimaryBaseNode):
    """
    Data node
    [Data node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=13)
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Data attributes
        """

        node: str = "Data"
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
        get the type of data node

        this attribute must come from the CRIPT controlled vocabulary

        Returns
        -------
        None
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_data_type: str) -> None:
        """
        set the data type

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
        get a list of processes for this data node

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
        get a list of citations for this data node

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
