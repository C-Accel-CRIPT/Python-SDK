from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Ingredient, Equipment, Material, Condition, Property, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Process(PrimaryBaseNode):
    """
    ## Definition
    The process node contains a list of ingredients, quantities, and procedure information for an experimental material
    transformation (chemical and physical).

    ## Attributes

    | attribute               | type             | example                                                                         | description                                                         | required | vocab |
    |-------------------------|------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------|----------|-------|
    | type                    | str              | mix                                                                             | type of process                                                     | True     | True  |
    | ingredient             | list[Ingredient] |                                                                                 | ingredients                                                         |          |       |
    | description             | str              | To oven-dried 20 mL glass vial, 5 mL of styrene and 10 ml of toluene was added. | explanation of the process                                          |          |       |
    | equipment               | list[Equipment]  |                                                                                 | equipment used in the process                                       |          |       |
    | product                | list[Material]   |                                                                                 | desired material produced from the process                          |          |       |
    | waste                   | list[Material]   |                                                                                 | material sent to waste                                              |          |       |
    | prerequisite_ processes | list[Process]    |                                                                                 | processes that must be completed prior to the start of this process |          |       |
    | condition              | list[Condition]  |                                                                                 | global process condition                                           |          |       |
    | property              | list[Property]   |                                                                                 | process properties                                                  |          |       |
    | keyword                | list[str]        |                                                                                 | words that classify the process                                     |          | True  |
    | citation               | list[Citation]   |                                                                                 | reference to a book, paper, or scholarly work                       |          |       |

    ## Available Subobjects
    * [Ingredient](../../subobjects/ingredient)
    * [equipment](../../subobjects/equipment)
    * [Property](../../subobjects/property)
    * [Condition](../../subobjects/condition)
    * [Citation](../../subobjects/citation)

    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Process attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        ingredient: List[Any] = field(default_factory=list)
        description: str = ""
        equipment: List[Any] = field(default_factory=list)
        product: List[Any] = field(default_factory=list)
        waste: List[Any] = field(default_factory=list)
        prerequisite_process: List["Process"] = field(default_factory=list)
        condition: List[Any] = field(default_factory=list)
        property: List[Any] = field(default_factory=list)
        keyword: List[str] = None
        citation: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        ingredient: List[Any] = None,
        description: str = "",
        equipment: List[Any] = None,
        product: List[Any] = None,
        waste: List[Any] = None,
        prerequisite_process: List[Any] = None,
        condition: List[Any] = None,
        property: List[Any] = None,
        keyword: List[str] = None,
        citation: List[Any] = None,
        notes: str = "",
        **kwargs
    ) -> None:
        """
        create a process node

        ```python
        my_process = cript.Process(name="my process name", type="affinity_pure")
        ```

        Parameters
        ----------
        ingredient: List[Ingredient]
            [ingredient](../../subobjects/ingredient) used in this process
        type: str = ""
            Process type must come from
            [CRIPT Controlled vocabulary process type](https://criptapp.org/keys/process-type/)
        description: str = ""
            description of this process
        equipment: List[Equipment] = None
            list of [equipment](../../subobjects/equipment) used in this process
        product: List[Material] = None
            product that this process created
        waste: List[Material] = None
            waste that this process created
        condition: List[Condition] = None
            list of [condition](../../subobjects/condition) that this process was created under
        property: List[Property] = None
            list of [properties](../../subobjects/property) for this process
        keyword: List[str] = None
            list of keywords for this process must come from
            [CRIPT process keyword controlled keyword](https://criptapp.org/keys/process-keyword/)
        citation: List[Citation] = None
            list of [citation](../../subobjects/citation)

        Returns
        -------
        None
            instantiate a process node
        """

        if ingredient is None:
            ingredient = []

        if equipment is None:
            equipment = []

        if product is None:
            product = []

        if waste is None:
            waste = []

        if prerequisite_process is None:
            prerequisite_process = []

        if condition is None:
            condition = []

        if property is None:
            property = []

        if keyword is None:
            keyword = []

        if citation is None:
            citation = []

        super().__init__(name=name, notes=notes, **kwargs)

        new_attrs = replace(
            self._json_attrs,
            ingredient=ingredient,
            type=type,
            description=description,
            equipment=equipment,
            product=product,
            waste=waste,
            condition=condition,
            prerequisite_process=prerequisite_process,
            property=property,
            keyword=keyword,
            citation=citation,
        )
        self._update_json_attrs_if_valid(new_attrs)

    # --------------- Properties -------------

    @property
    def type(self) -> str:
        """
        Process type must come from the [CRIPT controlled vocabulary](https://criptapp.org/keys/process-type/)

        Examples
        --------
        ```python
        my_process.type = "affinity_pure"
        ```

        Returns
        -------
        str
            Select a [Process type](https://criptapp.org/keys/process-type/) from CRIPT controlled vocabulary
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_process_type: str) -> None:
        """
        set process type from CRIPT controlled vocabulary

        Parameters
        ----------
        new_process_type: str
            new process type from CRIPT controlled vocabulary

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_process_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def ingredient(self) -> List[Any]:
        """
        List of [ingredient](../../subobjects/ingredients) for this process

        Examples
        ---------
        ```python
        my_ingredients = cript.Ingredient(
            material=simple_material_node,
            quantities=[simple_quantity_node],
        )

        my_process.ingredient = [my_ingredients]
        ```

        Returns
        -------
        List[Ingredient]
            list of ingredients for this process
        """
        return self._json_attrs.ingredient.copy()

    @ingredient.setter
    def ingredient(self, new_ingredient_list: List[Any]) -> None:
        """
        set the list of the ingredients for this process

        Parameters
        ----------
        new_ingredient_list
            list of ingredients to replace the current list

        Returns
        -------
        None
        """
        # TODO need to validate with CRIPT controlled vocabulary
        #   and if invalid then raise an error immediately
        new_attrs = replace(self._json_attrs, ingredient=new_ingredient_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def description(self) -> str:
        """
        description of this process

        Examples
        --------
        ```python
        my_process.description = "To oven-dried 20 mL glass vial, 5 mL of styrene and 10 ml of toluene was added"
        ```

        Returns
        -------
        str
            description of this process
        """
        return self._json_attrs.description

    @description.setter
    def description(self, new_description: str) -> None:
        """
        set the description of this process

        Parameters
        ----------
        new_description: str
            new process description to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, description=new_description)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def equipment(self) -> List[Any]:
        """
        List of [equipment](../../subobjects/equipment) used for this process

        Returns
        -------
        List[Equipment]
            list of equipment used for this process
        """
        return self._json_attrs.equipment.copy()

    @equipment.setter
    def equipment(self, new_equipment_list: List[Any]) -> None:
        """
        set the list of equipment used for this process

        Parameters
        ----------
        new_equipment_list
            new equipment list to replace the current equipment list for this process

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, equipment=new_equipment_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def product(self) -> List[Any]:
        """
        List of product (material nodes) for this process

        Returns
        -------
        List[Material]
            List of process product (Material nodes)
        """
        return self._json_attrs.product.copy()

    @product.setter
    def product(self, new_product_list: List[Any]) -> None:
        """
        set the product list for this process

        Parameters
        ----------
        new_product_list: List[Material]
            replace the current list of process product

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, product=new_product_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def waste(self) -> List[Any]:
        """
        List of waste that resulted from this process

        Examples
        --------
        ```python
        my_process.waste = my_waste_material
        ```

        Returns
        -------
        List[Material]
            list of waste materials that resulted from this product
        """
        return self._json_attrs.waste.copy()

    @waste.setter
    def waste(self, new_waste_list: List[Any]) -> None:
        """
        set the list of waste (Material node) for that resulted from this process

        Parameters
        ----------
        new_waste_list: List[Material]
            replace the list waste that resulted from this process

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, waste=new_waste_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def prerequisite_process(self) -> List["Process"]:
        """
        list of prerequisite process nodes

        Examples
        --------
        ```python

        my_prerequisite_process = [
            cript.Process(name="prerequisite processes 1", type="blow_molding"),
            cript.Process(name="prerequisite processes 2", type="centrifugation"),
        ]

        my_process.prerequisite_process = my_prerequisite_process
        ```

        Returns
        -------
        List[Process]
            list of process that had to happen before this process
        """
        return self._json_attrs.prerequisite_process.copy()

    @prerequisite_process.setter
    def prerequisite_process(self, new_prerequisite_process_list: List["Process"]) -> None:
        """
        set the prerequisite_process for the process node

        Parameters
        ----------
        new_prerequisite_process_list: List["Process"]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, prerequisite_process=new_prerequisite_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def condition(self) -> List[Any]:
        """
        List of condition present for this process

        Examples
        -------
        ```python
        # create condition node
        my_condition = cript.Condition(key="atm", type="min", value=1)

        my_process.condition = [my_condition]
        ```

        Returns
        -------
        List[Condition]
            list of condition for this process node
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition_list: List[Any]) -> None:
        """
        set the list of condition for this process

        Parameters
        ----------
        new_condition_list: List[Condition]
            replace the condition list
        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, condition=new_condition_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keyword(self) -> List[str]:
        """
        List of keyword for this process

        [Process keyword](https://criptapp.org/keys/process-keyword/) must come from CRIPT controlled vocabulary

        Returns
        -------
        List[str]
            list of keywords for this process nod
        """
        return self._json_attrs.keyword.copy()

    @keyword.setter
    def keyword(self, new_keyword_list: List[str]) -> None:
        """
        set the list of keyword for this process from CRIPT controlled vocabulary

        Parameters
        ----------
        new_keyword_list: List[str]
            replace the current list of keyword

        Returns
        -------
        None
        """
        # TODO validate with CRIPT controlled vocabulary
        new_attrs = replace(self._json_attrs, keyword=new_keyword_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Any]:
        """
        List of citation for this process

        Examples
        --------
        ```python
        # crate reference node for this citation
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

        # create citation node
        my_citation = cript.Citation(type="derived_from", reference=my_reference)

        my_process.citation = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            list of citation for this process node
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation_list: List[Any]) -> None:
        """
        set the list of citation for this process

        Parameters
        ----------
        new_citation_list: List[Citation]
            replace the current list of citation

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def property(self) -> List[Any]:
        """
        List of [Property nodes](../../subobjects/property) for this process

        Examples
        --------
        ```python
        # create property node
         my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

         my_process.properties = [my_property]
        ```

        Returns
        -------
        List[Property]
            list of properties for this process
        """
        return self._json_attrs.property.copy()

    @property.setter
    def property(self, new_property_list: List[Any]) -> None:
        """
        set the list of Property nodes for this process

        Parameters
        ----------
        new_property_list: List[Property]
            replace the current list of properties

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, property=new_property_list)
        self._update_json_attrs_if_valid(new_attrs)
