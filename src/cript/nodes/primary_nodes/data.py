from dataclasses import dataclass, replace
from typing import List

from cript import File, Process, Computation, ComputationalProcess, Material, Citation
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Data(PrimaryBaseNode):
    """
    Data node
    [Data node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=13)
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Data attributes
        """

        node: str = "Data"
        type: str = ""
        files: List[File] = None
        sample_preperation: Process = None
        computations: List[Computation] = None
        computational_process: ComputationalProcess = None
        materials: List[Material] = None
        processes: List[Process] = None
        citations: List[Citation] = None

    def __init__(
        self,
        type: str,
        files: List[File],
        sample_preperation: Process = None,
        computations: List[Computation] = None,
        computational_process: ComputationalProcess = None,
        materials: List[Material] = None,
        processes: List[Process] = None,
        citations: List[Citation] = None,
    ):
        super().__init__(node="Data")

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
        new_attrs = replace(self._json_attrs, data=new_data_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def files(self) -> List[File]:
        """
        get the list of files for this data node

        Returns
        -------
        List[File]
        """
        return self._json_attrs.files

    @files.setter
    def files(self, new_files_list: List[File]) -> None:
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
    def sample_preperation(self) -> Process:
        """
        get the sample preperation for this data node

        Returns
        -------
        None
        """
        return self._json_attrs.data

    @sample_preperation.setter
    def sample_preperation(self, new_sample_preperation: Process) -> None:
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
    def computations(self) -> List[Computation]:
        """
        get a list of computation nodes

        Returns
        -------
        None
        """
        return self._json_attrs.computations

    @computations.setter
    def computations(self, new_computation_list: List[Computation]) -> None:
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
    def computational_process(
        self, new_computational_process_list: List[ComputationalProcess]
    ) -> List[ComputationalProcess]:
        """
        get the computational_process for this data node

        Parameters
        ----------
        new_computational_process_list

        Returns
        -------
        None
        """
        pass

    @property
    def materials(self, new_materials_list: List[Material]) -> List[Material]:
        """
        gets a list of materials for this node

        Parameters
        ----------
        new_materials_list: List[Material]
            new list of materials to replace the current

        Returns
        -------
        List[Material]
        """
        return self._json_attrs.materials

    @materials.setter
    def materials(self, new_materials_list: List[Material]) -> None:
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
    def processes(self) -> List[Process]:
        """
        get a list of processes for this data node

        Returns
        -------
        None
        """
        return self._json_attrs.processes

    @processes.setter
    def processes(self, new_process_list: List[Process]) -> None:
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
    def citations(self) -> List[Citation]:
        """
        get a list of citations for this data node

        Returns
        -------
        List[Citation]
        """
        return self._json_attrs.citations

    @citations.setter
    def citations(self, new_citations_list: List[Citation]) -> None:
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
