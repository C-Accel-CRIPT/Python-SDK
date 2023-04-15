from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Process, Computation, ComputationalProcess, Data, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Experiment(PrimaryBaseNode):
    """
    ## Definition
    An
    [Experiment node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=9)
    is nested inside a [Collection](../collection) node.

    An [Experiment node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=9)
    can be thought as a folder/bucket that can hold:

    * [Process](../process)
    * [Computations](../computation)
    * [Computational_Process](../computational_process)
    * [Data](../data)
    * [Funding](../funding)
    * [Citations](../citation)

    ---

    Warnings
    --------
    !!! warning "Experiment names"
        Experiment names **MUST** be unique within a [Collection](../collection)

    ---

    <!-- TODO consider adding a JSON of an experiment node -->
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        process: List[Any] = field(default_factory=list)
        computation: List[Any] = field(default_factory=list)
        computational_process: List[Any] = field(default_factory=list)
        data: List[Any] = field(default_factory=list)
        funding: List[str] = field(default_factory=list)
        citation: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
            self,
            name: str,
            process: List[Any] = None,
            computation: List[Any] = None,
            computational_process: List[Any] = None,
            data: List[Any] = None,
            funding: List[str] = None,
            citation: List[Any] = None,
            notes: str = "",
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
        notes: str default=""
            notes for the experiment node


        Examples
        --------
        ```python
        # create an experiment node with all possible arguments
        my_experiment: cript.Experiment = cript.Experiment(
            name="my experiment name",
            process=[simple_process_node],
            computation=[simple_computation_node],
            computational_process=[simple_computational_process_node],
            data=[simple_data_node],
            funding=["National Science Foundation", "IRIS", "NIST"],
            citation=[simple_citation_node],
            notes="my experiment notes"
        )
        ```

        Returns
        -------
        None
            Instantiate an Experiment node
        """

        if process is None:
            process = []
        if computation is None:
            computation = []
        if computational_process is None:
            computational_process = []
        if data is None:
            data = []
        if funding is None:
            funding = []
        if citation is None:
            citation = []

        super().__init__(node="Experiment", name=name, notes=notes)

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            process=process,
            computation=computation,
            computational_process=computational_process,
            data=data,
            funding=funding,
            citation=citation,
            notes=notes,
        )

        # check if the code is still valid
        self.validate()

    # ------------------ Properties ------------------
    @property
    def process(self) -> List[Any]:
        """
        List of process for experiment

        ```python
        my_process = cript.Process(name="my process name", type="affinity_pure")

        my_experiment.process = [my_process]
        ```

        Returns
        -------
        List[Process]
            List of process that were performed in this experiment
        """
        return self._json_attrs.process.copy()

    @process.setter
    def process(self, new_process_list: List[Any]) -> None:
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
    def computation(self) -> List[Any]:
        """
        List of the [computations](../computation) in this experiment

        Examples
        --------
        ```python
        my_computation = cript.Computation(name="my computation name", type="analysis")

        simple_experiment_node.computation = [simple_computation_node]
        ```

        Returns
        -------
        List[Computation]
            List of [computations](../computation) for this experiment
        """
        return self._json_attrs.computation.copy()

    @computation.setter
    def computation(self, new_computation_list: List[Any]) -> None:
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
    def computational_process(self) -> List[Any]:
        """
        List of [computational_process](../computational_process) for this experiment

        Examples
        --------
        ```python
        my_computational_process = cript.ComputationalProcess(
            name="my computational process name",
            type=my_computational_process_type,
            input_data=[input_data],
            ingredients=[ingredients],
        )

        my_experiment.computational_process = [my_computational_process]
        ```

        Returns
        -------
        List[ComputationalProcess]
            computational process that were performed in this experiment
        """
        return self._json_attrs.computational_process.copy()

    @computational_process.setter
    def computational_process(self, new_computational_process_list: List[Any]) -> None:
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
        new_attrs = replace(self._json_attrs, computational_process=new_computational_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> List[Any]:
        """
        List of [data nodes](../data) for this experiment

        Examples
        --------
        ```python
        my_data = cript.Data(name="my data name", type="afm_amp", files=[simple_file_node])

        my_experiment.data = my_data
        ```

        Returns
        -------
        List[Data]
            list of [data nodes](../data) that belong to this experiment
        """
        return self._json_attrs.data.copy()

    @data.setter
    def data(self, new_data_list: List[Any]) -> None:
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
        List of strings of all the funders for this experiment

        Examples
        --------
        ```python
        my_experiment.funding = ["National Science Foundation", "IRIS", "NIST"]
        ```

        Returns
        -------
        List[str]
            List of funders for this experiment
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
    def citation(self) -> List[Any]:
        """
        get the list of citations for this experiment

        Returns
        -------
        List[Citation]
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Any]) -> None:
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
