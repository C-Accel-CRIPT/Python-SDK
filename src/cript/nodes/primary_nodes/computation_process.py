from dataclasses import dataclass, field, replace
from typing import Any, List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.util.json import UIDProxy


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
    | attribute                | type                          | example                               | description                                   | required | vocab |
    |--------------------------|-------------------------------|---------------------------------------|-----------------------------------------------|----------|-------|
    | type                     | str                           | general molecular dynamics simulation | category of computation                       | True     | True  |
    | input_data               | list[Data]                    |                                       | input data nodes                              | True     |       |
    | output_data              | list[Data]                    |                                       | output data nodes                             |          |       |
    | ingredient               | list[Ingredient]              |                                       | ingredients                                   | True     |       |
    | software_ configurations | list[Software  Configuration] |                                       | software and algorithms used                  |          |       |
    | condition                | list[Condition]               |                                       | setup information                             |          |       |
    | property                 | list[Property]                |                                       | computation process properties                |          |       |
    | citation                 | list[Citation]                |                                       | reference to a book, paper, or scholarly work |          |       |
    | notes                    | str                           |                                       | additional description of the step            |          |       |


    ## Available Subobjects
    * [ingredient](../../subobjects/ingredient)
    * [software_configuration](../../subobjects/software_configuration)
    * [property](../../subobjects/property)
    * [condition](../../subobjects/condition)
    * [citation](../../subobjects/citation)

    ## JSON Representation
    ```json
    {
       "name":"my computational process node name",
       "node":["ComputationProcess"],
       "type":"cross_linking",
       "uid":"_:b88ac0a5-b5c0-4197-a63d-b37e1fe8c6c6",
       "uuid":"b88ac0a5-b5c0-4197-a63d-b37e1fe8c6c6"
       "ingredient":[
          {
            "node":["Ingredient"],
            "uid":"_:f68d6fff-9327-48b1-9249-33ce498005e8",
             "uuid":"f68d6fff-9327-48b1-9249-33ce498005e8"
             "keyword":["catalyst"],
             "material":{
                "name":"my material name",
                "node":["Material"],
                "uid":"_:3b12f92c-2121-4520-920e-b4c5622de34a",
                "uuid":"3b12f92c-2121-4520-920e-b4c5622de34a",
                "bigsmiles":"[H]{[>][<]C(C[>])c1ccccc1[]}",
             },

             "quantity":[
                {
                   "key":"mass",
                   "node":["Quantity"],
                   "uid":"_:07c4a6a9-9385-4505-a30a-ca3549cedcd8",
                   "uuid":"07c4a6a9-9385-4505-a30a-ca3549cedcd8",
                   "uncertainty":0.2,
                   "uncertainty_type":"stdev",
                   "unit":"kg",
                   "value":11.2
                }
             ]
          }
       ],
       "input_data":[
          {
            "name":"my data name",
             "node":["Data"],
             "type":"afm_amp",
             "uid":"_:3c16bb05-ded1-4f52-9d02-c88c1a1de915",
             "uuid":"3c16bb05-ded1-4f52-9d02-c88c1a1de915"
             "file":[
                {
                   "name":"my file node name",
                   "node":["File"],
                   "source":"https://criptapp.org",
                   "type":"calibration",
                    "data_dictionary":"my file's data dictionary",
                   "extension":".csv",
                   "uid":"_:ee8153db-4108-49e4-8c5b-ffc26d4e6f71",
                   "uuid":"ee8153db-4108-49e4-8c5b-ffc26d4e6f71"
                }
             ],
          }
       ],
    }
    ```

    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all computational_process nodes attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        input_data: List[Union[Any, UIDProxy]] = field(default_factory=list)
        output_data: List[Union[Any, UIDProxy]] = field(default_factory=list)
        ingredient: List[Union[Any, UIDProxy]] = field(default_factory=list)
        software_configuration: List[Union[Any, UIDProxy]] = field(default_factory=list)
        condition: List[Union[Any, UIDProxy]] = field(default_factory=list)
        property: List[Union[Any, UIDProxy]] = field(default_factory=list)
        citation: List[Union[Any, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        name: str,
        type: str,
        input_data: List[Union[Any, UIDProxy]],
        ingredient: List[Union[Any, UIDProxy]],
        output_data: Optional[List[Union[Any, UIDProxy]]] = None,
        software_configuration: Optional[List[Union[Any, UIDProxy]]] = None,
        condition: Optional[List[Union[Any, UIDProxy]]] = None,
        property: Optional[List[Union[Any, UIDProxy]]] = None,
        citation: Optional[List[Union[Any, UIDProxy]]] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a computational_process node

        Examples
        --------
        >>> import cript
        >>> data_files = cript.File(
        ...     name="my file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary"
        ... )
        >>> input_data = cript.Data(name="my data name", type="afm_amp", file=[data_files])
        >>> my_material = cript.Material(
        ...     name="my material",
        ...     names = ["my material alternative name"]
        ... )
        >>> my_quantity = cript.Quantity(key="mass", value=1.23, unit="kg")
        >>> ingredient = cript.Ingredient(
        ...     material=my_material,
        ...     quantity=[my_quantity],
        ... )
        >>> my_computation_process = cript.ComputationProcess(
        ...     name="my computational process name",
        ...     type="cross_linking",
        ...     input_data=[input_data],
        ...     ingredient=[ingredient],
        ... )


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

        new_json_attrs = replace(
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
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        The [computational process type](https://app.criptapp.org/vocab/computational_process_type)
        must come from CRIPT Controlled vocabulary

        Examples
        --------
        >>> import cript
        >>> my_computation_process.type = "DPD"   # doctest: +SKIP

        Returns
        -------
        str
            computational process type
        """
        return self._json_attrs.type

    @type.setter
    @beartype
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
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def input_data(self) -> List[Any]:
        """
        List of input data for the computational process node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     data_dictionary="my file's data dictionary",
        ...     extension=".csv",
        ... )
        >>> my_input_data = cript.Data(name="my input data name", type="afm_amp", file=[my_file])
        >>> my_computation_process.input_data = [my_input_data]     # doctest: +SKIP

        Returns
        -------
        List[Data]
            list of input data for this computational process node
        """
        return self._json_attrs.input_data.copy()

    @input_data.setter
    @beartype
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
    @beartype
    def output_data(self) -> List[Any]:
        """
        List of the output data for the computational_process

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary"
        ... )
        >>> my_output_data = cript.Data(name="my output data name", type="afm_amp", file=[my_file])
        >>> my_computation_process.output_data = [my_output_data]    # doctest: +SKIP

        Returns
        -------
        List[Data]
            list of output data from this computational process node
        """
        return self._json_attrs.output_data.copy()

    @output_data.setter
    @beartype
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
    @beartype
    def ingredient(self) -> List[Any]:
        """
        List of ingredients for the computational_process

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(name="my material", bigsmiles = "my bigsmiles")
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient = cript.Ingredient(
        ...     material=my_material, quantity=[my_quantity], keyword=["catalyst"]
        ... )
        >>> my_computation_process.ingredient = [my_ingredient]   # doctest: +SKIP

        Returns
        -------
        List[Ingredient]
            list of ingredients for this computational process
        """
        return self._json_attrs.ingredient.copy()

    @ingredient.setter
    @beartype
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
    @beartype
    def software_configuration(self) -> List[Any]:
        """
        List of software_configuration for the computational process

        Examples
        --------
        >>> import cript
        >>> my_software = cript.Software(name="LAMMPS", version="23Jun22", source="lammps.org")
        >>> my_software_configuration = cript.SoftwareConfiguration(software=my_software)
        >>> my_computation_process.software_configuration = [my_software_configuration]   # doctest: +SKIP

        Returns
        -------
        List[SoftwareConfiguration]
            List of software configurations used for this computational process node
        """
        return self._json_attrs.software_configuration.copy()

    @software_configuration.setter
    @beartype
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
    @beartype
    def condition(self) -> List[Any]:
        """
        List of condition for the computational process

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(key="atm", type="min", value=1)
        >>> my_computation_process.condition = [my_condition]     # doctest: +SKIP

        Returns
        -------
        List[Condition]
            list of condition for this computational process node
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    @beartype
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
    @beartype
    def citation(self) -> List[Any]:
        """
        List of citation for the computational process

        Examples
        --------
        >>> import cript
        >>> my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")
        >>> my_citation = cript.Citation(type="derived_from", reference=my_reference)
        >>> my_computation_process.citation = [my_citation]     # doctest: +SKIP

        Returns
        -------
        List[Citation]
            list of citation for this computational process
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    @beartype
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
    @beartype
    def property(self) -> List[Any]:
        """
        List of properties

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.23, unit="J")
        >>> my_computation_process.property = [my_property]     # doctest: +SKIP

        Returns
        -------
        List[Property]
            list of properties for this computational process node
        """
        return self._json_attrs.property.copy()

    @property.setter
    @beartype
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
