from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Data, SoftwareConfiguration, Condition, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Computation(PrimaryBaseNode):
    """
    Computation node

    [Computation Node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=14)
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all computation nodes attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        input_data: List[Any] = field(default_factory=list)
        output_data: List[Any] = field(default_factory=list)
        software_configurations: List[Any] = field(default_factory=list)
        conditions: List[Any] = field(default_factory=list)
        prerequisite_computation: "Computation" = None
        citations: List[Any] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        input_data: List[Any] = None,
        output_data: List[Any] = None,
        software_configurations: List[Any] = None,
        conditions: List[Any] = None,
        prerequisite_computation: "Computation" = None,
        citations: List[Any] = None,
        notes: str = "",
        **kwargs
    ) -> None:

        super().__init__(node="Computation", name=name, notes=notes)

        if input_data is None:
            input_data = []

        if output_data is None:
            output_data = []

        if software_configurations is None:
            software_configurations = []

        if conditions is None:
            conditions = []

        if citations is None:
            citations = []

        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            input_data=input_data,
            output_data=output_data,
            software_configurations=software_configurations,
            conditions=conditions,
            prerequisite_computation=prerequisite_computation,
            citations=citations,
        )

        self.validate()

    # ------------------ Properties ------------------

    @property
    def type(self) -> str:
        """
        get the computation type

        the computation type must come from CRIPT controlled vocabulary

        Returns
        -------
        str
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_computation_type: str) -> None:
        """
        set the computation type

        the computation type must come from CRIPT controlled vocabulary

        Parameters
        ----------
        new_computation_type: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_computation_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def input_data(self) -> List[Any]:
        """
        get the list of input data (data nodes) for this node

        Returns
        -------
        List[Data]
        """
        return self._json_attrs.input_data.copy()

    @input_data.setter
    def input_data(self, new_input_data_list: List[Any]) -> None:
        """
        set the input data list

        Parameters
        ----------
        new_input_data_list: List[Data]
            list of input data (data nodes) to replace the current

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, input_data=new_input_data_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def output_data(self) -> List[Any]:
        """
        get the list of output data (data nodes)

        Returns
        -------
        List[Data]
        """
        return self._json_attrs.output_data.copy()

    @output_data.setter
    def output_data(self, new_output_data_list: List[Any]) -> None:
        """
        set the list of output data (data nodes) for this node

        Parameters
        ----------
        new_output_data_list: List[Data]
            replace the current list of output data for this node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, output_data=new_output_data_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def software_configurations(self) -> List[Any]:
        """
        get the software_configurations for this computation node

        Returns
        -------
        List[SoftwareConfiguration]
        """
        return self._json_attrs.software_configurations.copy()

    @software_configurations.setter
    def software_configurations(self, new_software_configurations_list: List[Any]) -> None:
        """
        set the list of software_configurations for this computation node

        Parameters
        ----------
        new_software_configurations_list: List[software_configurations]
            new_software_configurations_list to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, software_configurations=new_software_configurations_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def conditions(self) -> List[Any]:
        """
        get the list of conditions for this computation node

        Returns
        -------
        List[Condition]
        """
        return self._json_attrs.conditions.copy()

    @conditions.setter
    def conditions(self, new_condition_list: List[Any]) -> None:
        """
        set the list of conditions for this node

        Parameters
        ----------
        new_condition_list: List[Condition]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, conditions=new_condition_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def prerequisite_computation(self) -> "Computation":
        """
        get computation node

        Returns
        -------
        Computation
        """
        return self._json_attrs.prerequisite_computation

    @prerequisite_computation.setter
    def prerequisite_computation(self, new_prerequisite_computation: "Computation") -> None:
        """
        set new prerequisite_computation

        Parameters
        ----------
        new_prerequisite_computation: "Computation"

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, prerequisite_computation=new_prerequisite_computation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Any]:
        """
        get the list of citations for this computation node

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

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citations=new_citations_list)
        self._update_json_attrs_if_valid(new_attrs)
