from dataclasses import dataclass, replace
from typing import List

from cript import Process, Computation, ComputationalProcess, Data, Citation
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Experiment(PrimaryBaseNode):
    """
    Experiment node

    as defined in the [data model](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=9)
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        node: str = "Experiment"
        process: List[Process] = None
        computation: List[Computation] = None
        computational_process: List[ComputationalProcess] = None
        data: List[Data] = None
        funding: List[str] = None
        citation: List[Citation] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        process: List[Process] = None,
        computation: List[Computation] = None,
        computational_process: List[ComputationalProcess] = None,
        data: List[Data] = None,
        funding: List[str] = None,
        citation: List[Citation] = None,
        **kwargs
    ):
        """
        create an Experiment node

        Parameters
        ----------
        name: str
            name of Experiment

        process: List[Process]
            list of Process nodes for this Experiment

        computation: List[Computation]
            list of computation nodes for this Experiment

        computational_process: List[ComputationalProcess]
            list of computational_process nodes for this Experiment

        data: List[Data]
            list of data nodes for this experiment

        funding: List[str]
            list of the funders names for this Experiment

        citation: List[Citation]
            list of Citation nodes for this experiment

        Returns
        -------
        None
        """
        super().__init__(node="Experiment")
        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            process=process,
            computation=computation,
            computational_process=computational_process,
            data=data,
            funding=funding,
            citation=citation,
        )

        # check if the code is still valid
        self.validate()

    @property
    def process(self) -> List[Process]:
        """
        get the list of process for this experiment

        Returns
        -------
        List[Process]
        """
        return self._json_attrs.process.copy()

    @process.setter
    def process(self, new_process_list: List[Process]) -> None:
        """
        set the list of process for this experiment

        Parameters
        ----------
        new_process_list: List[Process]
            new process list to replace the current process list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, process=new_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computation(self) -> List[Computation]:
        """
        get a list of the computations in this experiment

        Returns
        -------
        List[Computation]
        """
        return self._json_attrs.computation.copy()

    @computation.setter
    def computation(self, new_computation_list: List[Computation]) -> None:
        """
        set the list of computations for this experiment

        Parameters
        ----------
        new_computation_list: List[Computation]
            new list of computations to replace the current list of experiments

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation=new_computation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computational_process(self) -> List[ComputationalProcess]:
        """
        get the list of computational_process for this experiment

        Returns
        -------
        List[ComputationalProcess]
        """
        return self._json_attrs.computational_process.copy()

    @computational_process.setter
    def computational_process(
        self, new_computational_process_list: List[ComputationalProcess]
    ) -> None:
        """
        set the list of computational_process for this experiment

        Parameters
        ----------
        new_computational_process_list: List[ComputationalProcess]
            new list of computations to replace the current for the experiment

        Returns
        -------
        None
        """
        new_attrs = replace(
            self._json_attrs, computational_process=new_computational_process_list
        )
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> List[Data]:
        """
        get the list of data for this experiment

        Returns
        -------
        List[Data]
        """
        return self._json_attrs.data.copy()

    @data.setter
    def data(self, new_data_list: List[Data]) -> None:
        """
        set the list of data for this experiment

        Parameters
        ----------
        new_data_list: List[Data]
            new list of data to replace the current list for this experiment

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data=new_data_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def funding(self) -> List[str]:
        """
        return a list of strings of all the funders for this experiment

        Returns
        -------
        List[str]
        """
        return self._json_attrs.funding.copy()

    @funding.setter
    def funding(self, new_funding_list: List[str]) -> None:
        """
        set the list of funders for this experiment

        Parameters
        ----------
        new_funding_list: List[str]
            replace the current list of funders

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, funding=new_funding_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Citation]:
        """
        get the list of citations for this experiment

        Returns
        -------
        List[Citation]
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Citation]) -> None:
        """
        set the list of citations for this experiment

        Parameters
        ----------
        new_citation_list: List[Citation]
            replace the list of citations for this experiment with a new list of citations

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)
