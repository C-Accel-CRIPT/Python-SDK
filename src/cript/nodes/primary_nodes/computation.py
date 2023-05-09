from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Data, SoftwareConfiguration, Condition, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Computation(PrimaryBaseNode):
    """
    ## Definition

    The
    [Computation node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=14)
    describes the transformation of data or the creation of a computational data
    set.

    **Common computations for simulations** are energy minimization, annealing, quenching, or
    NPT/NVT (isothermal-isobaric/canonical ensemble) simulations.

    **Common computations for experimental** data include fitting a reaction model to kinetic data
    to determine rate constants, a plateau modulus from a time-temperature-superposition, or calculating radius of
    gyration with the Debye function from small angle scattering data.



    ## Attributes
    | attribute                | type                          | example                               | description                                   | required | vocab |
    |--------------------------|-------------------------------|---------------------------------------|-----------------------------------------------|----------|-------|
    | type                     | str                           | general molecular dynamics simulation | category of computation                       | True     | True  |
    | input_data               | list[Data]                    |                                       | input data nodes                              |          |       |
    | output_data              | list[Data]                    |                                       | output data nodes                             |          |       |
    | software_ configurations | list[Software  Configuration] |                                       | software and algorithms used                  |          |       |
    | condition                | list[Condition]               |                                       | setup information                             |          |       |
    | prerequisite_computation | Computation                   |                                       | prior computation method in chain             |          |       |
    | citation                | list[Citation]                |                                       | reference to a book, paper, or scholarly work |          |       |
    | notes                    | str                           |                                       | additional description of the step            |          |       |

    ## Available Subobjects
    * [Software Configuration](../../subobjects/software_configuration)
    * [Condition](../../subobjects/condition)
    * [Citation](../../subobjects/citation)

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
        software_configuration: List[Any] = field(default_factory=list)
        condition: List[Any] = field(default_factory=list)
        prerequisite_computation: "Computation" = None
        citation: List[Any] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        input_data: List[Any] = None,
        output_data: List[Any] = None,
        software_configuration: List[Any] = None,
        condition: List[Any] = None,
        prerequisite_computation: "Computation" = None,
        citation: List[Any] = None,
        notes: str = "",
        **kwargs
    ) -> None:
        """
        create a computation node

        Parameters
        ----------
        name: str
            name of computation node
        type: str
            type of computation node. Computation type must come from CRIPT controlled vocabulary
        input_data: List[Data] default=None
            input data (data node)
        output_data: List[Data] default=None
            output data (data node)
        software_configuration: List[SoftwareConfiguration] default=None
            software configuration of computation node
        condition: List[Condition] default=None
            condition for the computation node
        prerequisite_computation: Computation default=None
            prerequisite computation
        citation: List[Citation] default=None
            list of citations
        notes: str = ""
            any notes for this computation node
        **kwargs
            for internal use of deserialize JSON from API to node

        Examples
        --------
        ```python
        my_computation = cript.Computation(name="my computation name", type="analysis")
        ```

        Returns
        -------
        None
            instantiate a computation node

        """
        super().__init__(name=name, notes=notes, **kwargs)

        if input_data is None:
            input_data = []

        if output_data is None:
            output_data = []

        if software_configuration is None:
            software_configuration = []

        if condition is None:
            condition = []

        if citation is None:
            citation = []

        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            input_data=input_data,
            output_data=output_data,
            software_configuration=software_configuration,
            condition=condition,
            prerequisite_computation=prerequisite_computation,
            citation=citation,
        )

        self.validate()

    # ------------------ Properties ------------------

    @property
    def type(self) -> str:
        """
        The type of computation

        the computation type must come from CRIPT controlled vocabulary

        Examples
        --------
        ```python
        my_computation.type = "type="analysis"
        ```

        Returns
        -------
        str
            type of computation
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
        List of input data (data nodes) for this node

        Examples
        --------
        ```python
        # create file node
        my_file = cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )

        # create a data node
        my_input_data = cript.Data(name="my data name", type="afm_amp", files=[my_file])

        my_computation.input_data = [my_input_data]
        ```

        Returns
        -------
        List[Data]
            list of input data for this computation
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
        List of output data (data nodes)

        Examples
        --------
        ```python
        # create file node
        my_file = cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )

        # create a data node
        my_output_data = cript.Data(name="my data name", type="afm_amp", files=[my_file])

        my_computation.output_data = [my_output_data]
        ```

        Returns
        -------
        List[Data]
            list of output data for this computation
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
    def software_configuration(self) -> List[Any]:
        """
        List of software_configuration for this computation node

        Examples
        --------
        ```python
        # create software configuration node
        my_software_configuration = cript.SoftwareConfiguration(software=simple_software_node)

        my_computation.software_configuration = my_software_configuration
        ```

        Returns
        -------
        List[SoftwareConfiguration]
            list of software configurations
        """
        return self._json_attrs.software_configuration.copy()

    @software_configuration.setter
    def software_configuration(self, new_software_configuration_list: List[Any]) -> None:
        """
        set the list of software_configuration for this computation node

        Parameters
        ----------
        new_software_configuration_list: List[software_configuration]
            new_software_configuration_list to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, software_configuration=new_software_configuration_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def condition(self) -> List[Any]:
        """
        List of condition for this computation node

        Examples
        --------
        ```python
        # create a condition node
        my_condition = cript.Condition(key="atm", type="min", value=1)

        my_computation.condition = my_condition
        ```

        Returns
        -------
        List[Condition]
            list of condition for the computation node
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition_list: List[Any]) -> None:
        """
        set the list of condition for this node

        Parameters
        ----------
        new_condition_list: List[Condition]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, condition=new_condition_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def prerequisite_computation(self) -> "Computation":
        """
        prerequisite computation

        Examples
        --------
        ```python
        # create computation node for prerequisite_computation
        my_prerequisite_computation = cript.Computation(name="my prerequisite computation name", type="data_fit")

        my_computation.prerequisite_computation = my_prerequisite_computation
        ```

        Returns
        -------
        Computation
            prerequisite computation
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
    def citation(self) -> List[Any]:
        """
        List of citations

         Examples
         --------
         ```python
         # create a reference node for the citation
         my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

         # create a reference
         my_citation = cript.Citation(type="derived_from", reference=my_reference)

         my_computation.citation = [my_citation]
         ```

         Returns
         -------
         List[Citation]
             list of citations for this computation node
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Any]) -> None:
        """
        set the List of citations

        Parameters
        ----------
        new_citation_list: List[Citation]
            list of citations for this computation node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)
