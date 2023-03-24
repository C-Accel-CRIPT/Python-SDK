from dataclasses import dataclass, replace
from typing import List

from cript import Data, Ingredient, SoftwareConfiguration, Condition, Property, Citation
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class ComputationalProcess(PrimaryBaseNode):
    """
    Computational_Process node

    [Computational_Process](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=15)
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all computational_process nodes attributes
        """

        node: str = "Computational_Process"
        type_: str = ""
        input_data: List[Data] = None
        output_data: List[Data] = None
        ingredients: List[Ingredient] = None
        software_configurations: List[SoftwareConfiguration] = None
        conditions: List[Condition] = None
        properties: List[Property] = None
        citations: List[Citation] = None

    def __init__(
        self,
        type_: str,
        input_data: List[Data],
        ingredients: List[Ingredient],
        output_data: List[Data] = None,
        software_configurations: List[SoftwareConfiguration] = None,
        conditions: List[Condition] = None,
        properties: List[Property] = None,
        citations: List[Citation] = None,
        **kwargs
    ) -> None:
        """
        create a computational_process node

        type_, input_data, and ingredients are required and the rest are optional

        Parameters
        ----------
        type_: str
            type of computation process from CRIPT controlled vocabulary

        input_data: List[Data]
            list of input data for computational process

        ingredients: List[Ingredient]
            list of ingredients for this computational process node

        output_data: List[Data] default=None
            list of output data for this computational process node

        software_configurations: List[SoftwareConfiguration] default=None
            list of software configurations for this computational process node

        conditions: List[Condition] default=None
            list of conditions for this computational process node

        properties: List[Property] default=None
            list of properties for this computational process node

        citations: List[Citation] default=None
            list of citations for this computational process node

        Returns
        -------
        None
        """
        super().__init__(node="Computational_Process")
        # TODO validate type_ from vocab

        self._json_attrs = replace(
            self._json_attrs,
            type_=type_,
            input_data=input_data,
            ingredients=ingredients,
            output_data=output_data,
            software_configurations=software_configurations,
            conditions=conditions,
            properties=properties,
            citations=citations,
        )

        self.validate()

    # -------------- Properties --------------

    @property
    def type_(self) -> str:
        """
        get the computational process type

        must come from CRIPT controlled vocabulary

        Returns
        -------
        None
        """
        return self._json_attrs.type_

    @type_.setter
    def type_(self, new_type: str) -> None:
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
        new_attrs = replace(self._json_attrs, type_=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def input_data(self) -> List[Data]:
        """
        get the input data for the computational process node

        Returns
        -------
        List[Data]
        """
        return self._json_attrs.input_data.copy()

    @input_data.setter
    def input_data(self, new_input_data_list: List[Data]) -> None:
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
    def output_data(self) -> List[Data]:
        """
        get the output data for the computational_process

        Returns
        -------
        List[Data]
        """
        return self._json_attrs.out_put.copy()

    @output_data.setter
    def output_data(self, new_output_data_list: List[Data]) -> None:
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
    def ingredients(self) -> List[Ingredient]:
        """
        get the ingredients list for the computational_process

        Returns
        -------
        List[Ingredient]
        """
        return self._json_attrs.ingredients.copy()

    @ingredients.setter
    def ingredients(self, new_ingredients_list: List[Ingredient]) -> None:
        """
        set the ingredients list for this computational process

        Parameters
        ----------
        new_ingredients_list: List[Ingredient]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, ingredients=new_ingredients_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def software_configurations(self) -> List[SoftwareConfiguration]:
        """
        get a list of software_configurations for the computational process

        Returns
        -------
        List[SoftwareConfiguration]
        """
        return self._json_attrs.software_configurations.copy()

    @software_configurations.setter
    def software_configurations(
        self, new_software_configuration_list: List[SoftwareConfiguration]
    ) -> None:
        """
        set the list of software_configuration for the computational process

        Parameters
        ----------
        new_software_configuration_list: List[SoftwareConfiguration]

        Returns
        -------
        None
        """
        new_attrs = replace(
            self._json_attrs, software_configuration=new_software_configuration_list
        )
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def conditions(self) -> List[Condition]:
        """
        get the list of conditions for the computational process

        Returns
        -------
        List[Condition]
        """
        return self._json_attrs.conditions.copy()

    @conditions.setter
    def conditions(self, new_conditions: List[Condition]) -> None:
        """
        set the conditions for the computational process

        Parameters
        ----------
        new_conditions: List[Condition]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, conditions=new_conditions)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def properties(self) -> List[Property]:
        """
        get a list of properties

        Returns
        -------
        List[Property]
        """
        return self._json_attrs.properties.copy()

    @properties.setter
    def properties(self, new_properties_list: List[Property]) -> None:
        """
        set the properties list for the computational process

        Parameters
        ----------
        new_properties_list: List[Property]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, properties=new_properties_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Citation]:
        """
        get a list of citations for the computational process

        Returns
        -------
        List[Citation]
        """
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations_list: List[Citation]) -> None:
        """
        set the citations list for the computational process node

        Parameters
        ----------
        new_citations_list: List[Citation]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citations=new_citations_list)
        self._update_json_attrs_if_valid(new_attrs)
