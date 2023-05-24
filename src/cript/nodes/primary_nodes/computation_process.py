from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Data, Ingredient, SoftwareConfiguration, Condition, Property, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class ComputationProcess(PrimaryBaseNode):
    """
    ## Definition

    A
    [Computational_Process](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=15)
    is a simulation that processes or changes a virtual material. Examples
    include simulations of chemical reactions, chain scission, cross-linking, strong shear, etc. A
    computational process may also encapsulate any computation that dramatically changes the
    materials properties, molecular topology, and physical aspects like molecular orientation, etc. The
    computation_forcefield of a simulation is associated with a material. As a consequence, if the
    forcefield changes or gets refined via a computational procedure (density functional theory,
    iterative Boltzmann inversion for coarse-graining etc.) this forcefield changing step must be
    described as a computational_process and a new material node with a different
    computation_forcefield needs to be created.

    ## Attributes
    | attribute                | type                          | example                               | description                                     | required | vocab |
    |--------------------------|-------------------------------|---------------------------------------|-------------------------------------------------|----------|-------|
    | type                     | str                           | general molecular dynamics simulation | category of computation                         | True     | True  |
    | input_data               | list[Data]                    |                                       | input data nodes                                | True     |       |
    | output_data              | list[Data]                    |                                       | output data nodes                               |          |       |
    | ingredient              | list[Ingredient]              |                                       | ingredients                                     | True     |       |
    | software_ configurations | list[Software  Configuration] |                                       | software and algorithms used                    |          |       |
    | condition                | list[Condition]               |                                       | setup information                               |          |       |
    | property               | list[Property]                |                                       | computation process properties                  |          |       |
    | citation                | list[Citation]                |                                       | reference to a book, paper, or scholarly work   |          |       |
    | notes                    | str                           |                                       | additional description of the step              |          |       |


    ## Available Subobjects
    * [ingredient](../../subobjects/ingredient)
    * [software_configuration](../../subobjects/software_configuration)
    * [property](../../subobjects/property)
    * [condition](../../subobjects/condition)
    * [citation](../../subobjects/citation)

    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all computational_process nodes attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        input_data: List[Any] = field(default_factory=list)
        output_data: List[Any] = field(default_factory=list)
        ingredient: List[Any] = field(default_factory=list)
        software_configuration: List[Any] = field(default_factory=list)
        condition: List[Any] = field(default_factory=list)
        property: List[Any] = field(default_factory=list)
        citation: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        input_data: List[Any],
        ingredient: List[Any],
        output_data: List[Any] = None,
        software_configuration: List[Any] = None,
        condition: List[Any] = None,
        property: List[Any] = None,
        citation: List[Any] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a computational_process node

        Examples
        --------
        ```python

        # create file node for input data node
        data_files = cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )

        # create input data node
        input_data = cript.Data(name="my data name", type="afm_amp", files=[data_files])

        # Material node for Quantity node
        my_material = cript.Material(
            name="my material",
            identifiers=[{"alternative_names": "my material alternative name"}]
            )

        # create quantity node
        my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

        # create ingredient node
        ingredient = cript.Ingredient(
            material=my_material,
            quantities=[my_quantity],
        )

        # create computational process node
        my_computational_process = cript.ComputationalProcess(
            name="my computational process name",
            type="cross_linking",
            input_data=[input_data],
            ingredient=[ingredient],
        )
        ```


        Parameters
        ----------
        name: str
            computational process name
        type: str
            type of computation process from CRIPT controlled vocabulary
        input_data: List[Data]
            list of input data for computational process
        ingredient: List[Ingredient]
            list of ingredients for this computational process node
        output_data: List[Data] default=None
            list of output data for this computational process node
        software_configuration: List[SoftwareConfiguration] default=None
            list of software configurations for this computational process node
        condition: List[Condition] default=None
            list of condition for this computational process node
        property: List[Property] default=None
            list of properties for this computational process node
        citation: List[Citation] default=None
            list of citation for this computational process node
        notes: str default=""
            optional notes for the computational process node

        Returns
        -------
        None
            instantiate computationalProcess node
        """
        super().__init__(name=name, notes=notes, **kwargs)

        # TODO validate type from vocab

        if input_data is None:
            input_data = []

        if ingredient is None:
            ingredient = []

        if output_data is None:
            output_data = []

        if software_configuration is None:
            software_configuration = []

        if condition is None:
            condition = []

        if property is None:
            property = []

        if citation is None:
            citation = []

        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            input_data=input_data,
            ingredient=ingredient,
            output_data=output_data,
            software_configuration=software_configuration,
            condition=condition,
            property=property,
            citation=citation,
        )

        # self.validate()

    # -------------- Properties --------------

    @property
    def type(self) -> str:
        """
        The computational process type must come from CRIPT Controlled vocabulary

        Examples
        --------
        ```python
        my_computational_process.type = "DPD"
        ```

        Returns
        -------
        str
            computational process type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str) -> None:
        """
        set the computational_process type

        computational_process type must come from CRIPT controlled vocabulary

        Parameters
        ----------
        new_type: str
            new computational process type.
            computational process type must come from CRIPT controlled vocabulary

        Returns
        -------
        None
        """
        # TODO check computational_process type with CRIPT controlled vocabulary
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def input_data(self) -> List[Any]:
        """
        List of input data for the computational process node

        Examples
        --------
        ```python
        # create file node for the data node
        my_file = cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )

        # create input data node
        my_input_data = cript.Data(name="my input data name", type="afm_amp", files=[my_file])

        # set computational process data node
        my_computation.input_data = my_input_data
        ```

        Returns
        -------
        List[Data]
            list of input data for this computational process node
        """
        return self._json_attrs.input_data.copy()

    @input_data.setter
    def input_data(self, new_input_data_list: List[Any]) -> None:
        """
        set the input data for this computational process

        Parameters
        ----------
        new_input_data_list: List[Data]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, input_data=new_input_data_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def output_data(self) -> List[Any]:
        """
        List of the output data for the computational_process

        Examples
        --------
        ```python
        # create file node for the data node
        my_file = cript.File(
            source="https://criptapp.org",
            type="calibration",
            extension=".csv",
            data_dictionary="my file's data dictionary"
        )

        # create input data node
        my_output_data = cript.Data(name="my output data name", type="afm_amp", files=[my_file])

        # set computational process data node
        my_computation.output_data = my_input_data
        ```

        Returns
        -------
        List[Data]
            list of output data from this computational process node
        """
        return self._json_attrs.output_data.copy()

    @output_data.setter
    def output_data(self, new_output_data_list: List[Any]) -> None:
        """
        set the output_data list for the computational_process

        Parameters
        ----------
        new_output_data_list: List[Data]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, output_data=new_output_data_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def ingredient(self) -> List[Any]:
        """
        List of ingredients for the computational_process

        Examples
        --------
        ```python
        # create ingredient node
        ingredient = cript.Ingredient(
            material=simple_material_node,
            quantities=[simple_quantity_node],
        )

        my_computational_process.ingredient =
        ```

        Returns
        -------
        List[Ingredient]
            list of ingredients for this computational process
        """
        return self._json_attrs.ingredient.copy()

    @ingredient.setter
    def ingredient(self, new_ingredient_list: List[Any]) -> None:
        """
        set the ingredients list for this computational process

        Parameters
        ----------
        new_ingredient_list: List[Ingredient]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, ingredient=new_ingredient_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def software_configuration(self) -> List[Any]:
        """
        List of software_configuration for the computational process

        Examples
        --------
        ```python
        # create software configuration node
        my_software_configuration = cript.SoftwareConfiguration(software=simple_software_node)

        my_computational_process.software_configuration = my_software_configuration
        ```

        Returns
        -------
        List[SoftwareConfiguration]
            List of software configurations used for this computational process node
        """
        return self._json_attrs.software_configuration.copy()

    @software_configuration.setter
    def software_configuration(self, new_software_configuration_list: List[Any]) -> None:
        """
        set the list of software_configuration for the computational process

        Parameters
        ----------
        new_software_configuration_list: List[SoftwareConfiguration]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, software_configuration=new_software_configuration_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def condition(self) -> List[Any]:
        """
        List of condition for the computational process

        Examples
        --------
        ```python
        # create condition node
         my_condition = cript.Condition(key="atm", type="min", value=1)

         my_computational_process.condition = [my_condition]

        ```

        Returns
        -------
        List[Condition]
            list of condition for this computational process node
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition: List[Any]) -> None:
        """
        set the condition for the computational process

        Parameters
        ----------
        new_condition: List[Condition]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, condition=new_condition)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Any]:
        """
        List of citation for the computational process

        Examples
        --------
        ```python
        # create a reference node for the citation
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

        # create a reference
        my_citation = cript.Citation(type="derived_from", reference=my_reference)

        my_computational_process.citation = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            list of citation for this computational process
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Any]) -> None:
        """
        set the citation list for the computational process node

        Parameters
        ----------
        new_citation_list: List[Citation]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def property(self) -> List[Any]:
        """
        List of properties

        Examples
        --------
        ```python
        # create a property node
        my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

        my_computational_process.property = [my_property]
        ```

        Returns
        -------
        List[Property]
            list of properties for this computational process node
        """
        return self._json_attrs.property.copy()

    @property.setter
    def property(self, new_property_list: List[Any]) -> None:
        """
        set the properties list for the computational process

        Parameters
        ----------
        new_property_list: List[Property]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, property=new_property_list)
        self._update_json_attrs_if_valid(new_attrs)
