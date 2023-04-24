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
    | ingredients             | list[Ingredient] |                                                                                 | ingredients                                                         |          |       |
    | description             | str              | To oven-dried 20 mL glass vial, 5 mL of styrene and 10 ml of toluene was added. | explanation of the process                                          |          |       |
    | equipment               | list[Equipment]  |                                                                                 | equipment used in the process                                       |          |       |
    | products                | list[Material]   |                                                                                 | desired material produced from the process                          |          |       |
    | waste                   | list[Material]   |                                                                                 | material sent to waste                                              |          |       |
    | prerequisite_ processes | list[Process]    |                                                                                 | processes that must be completed prior to the start of this process |          |       |
    | conditions              | list[Condition]  |                                                                                 | global process conditions                                           |          |       |
    | properties              | list[Property]   |                                                                                 | process properties                                                  |          |       |
    | keywords                | list[str]        |                                                                                 | words that classify the process                                     |          | True  |
    | citations               | list[Citation]   |                                                                                 | reference to a book, paper, or scholarly work                       |          |       |

    ## Available Subobjects
    * [Ingredient](../../subobjects/ingredient)
    * [Equipments](../../subobjects/equipment)
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
        ingredients: List[Any] = field(default_factory=list)
        description: str = ""
        equipments: List[Any] = field(default_factory=list)
        products: List[Any] = field(default_factory=list)
        waste: List[Any] = field(default_factory=list)
        prerequisite_processes: List["Process"] = field(default_factory=list)
        conditions: List[Any] = field(default_factory=list)
        properties: List[Any] = field(default_factory=list)
        keywords: List[str] = None
        citations: List[Any] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        type: str,
        ingredients: List[Any] = None,
        description: str = "",
        equipments: List[Any] = None,
        products: List[Any] = None,
        waste: List[Any] = None,
        prerequisite_processes: List[Any] = None,
        conditions: List[Any] = None,
        properties: List[Any] = None,
        keywords: List[str] = None,
        citations: List[Any] = None,
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
        ingredients: List[Ingredient]
            [ingredients](../../subobjects/ingredient) used in this process
        type: str = ""
            Process type must come from
            [CRIPT Controlled vocabulary process type](https://criptapp.org/keys/process-type/)
        description: str = ""
            description of this process
        equipments: List[Equipment] = None
            list of [equipments](../../subobjects/equipment) used in this process
        products: List[Material] = None
            products that this process created
        waste: List[Material] = None
            waste that this process created
        conditions: List[Condition] = None
            list of [conditions](../../subobjects/condition) that this process was created under
        properties: List[Property] = None
            list of [properties](../../subobjects/property) for this process
        keywords: List[str] = None
            list of keywords for this process must come from
            [CRIPT process keywords controlled keywords](https://criptapp.org/keys/process-keyword/)
        citations: List[Citation] = None
            list of [citations](../../subobjects/citation)

        Returns
        -------
        None
            instantiate a process node
        """

        if ingredients is None:
            ingredients = []

        if equipments is None:
            equipments = []

        if products is None:
            products = []

        if waste is None:
            waste = []

        if prerequisite_processes is None:
            prerequisite_processes = []

        if conditions is None:
            conditions = []

        if properties is None:
            properties = []

        if keywords is None:
            keywords = []

        if citations is None:
            citations = []

        super().__init__(name=name, notes=notes)

        new_attrs = replace(
            self._json_attrs,
            ingredients=ingredients,
            type=type,
            description=description,
            equipments=equipments,
            products=products,
            waste=waste,
            conditions=conditions,
            prerequisite_processes=prerequisite_processes,
            properties=properties,
            keywords=keywords,
            citations=citations,
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
    def ingredients(self) -> List[Any]:
        """
        List of [ingredients](../../subobjects/ingredients) for this process

        Examples
        ---------
        ```python
        my_ingredients = cript.Ingredient(
            material=simple_material_node,
            quantities=[simple_quantity_node],
        )

        my_process.ingredients = [my_ingredients]
        ```

        Returns
        -------
        List[Ingredient]
            list of ingredients for this process
        """
        return self._json_attrs.ingredients.copy()

    @ingredients.setter
    def ingredients(self, new_ingredients_list: List[Any]) -> None:
        """
        set the list of the ingredients for this process

        Parameters
        ----------
        new_ingredients_list
            list of ingredients to replace the current list

        Returns
        -------
        None
        """
        # TODO need to validate with CRIPT controlled vocabulary
        #   and if invalid then raise an error immediately
        new_attrs = replace(self._json_attrs, ingredients=new_ingredients_list)
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
    def equipments(self) -> List[Any]:
        """
        List of [equipments](../../subobjects/equipments) used for this process

        Returns
        -------
        List[Equipment]
            list of equipments used for this process
        """
        return self._json_attrs.equipments.copy()

    @equipments.setter
    def equipments(self, new_equipment_list: List[Any]) -> None:
        """
        set the list of equipments used for this process

        Parameters
        ----------
        new_equipment_list
            new equipment list to replace the current equipment list for this process

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, equipments=new_equipment_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def products(self) -> List[Any]:
        """
        List of products (material nodes) for this process

        Returns
        -------
        List[Material]
            List of process products (Material nodes)
        """
        return self._json_attrs.products.copy()

    @products.setter
    def products(self, new_products_list: List[Any]) -> None:
        """
        set the products list for this process

        Parameters
        ----------
        new_products_list: List[Material]
            replace the current list of process products

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, products=new_products_list)
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
    def prerequisite_processes(self) -> List["Process"]:
        """
        list of prerequisite process nodes

        Examples
        --------
        ```python

        my_prerequisite_processes = [
            cript.Process(name="prerequisite processes 1", type="blow_molding"),
            cript.Process(name="prerequisite processes 2", type="centrifugation"),
        ]

        my_process.prerequisite_processes = my_prerequisite_processes
        ```

        Returns
        -------
        List[Process]
            list of process that had to happen before this process
        """
        return self._json_attrs.prerequisite_processes

    @prerequisite_processes.setter
    def prerequisite_processes(self, new_prerequisite_processes_list: List["Process"]) -> None:
        """
        set the prerequisite_processes for the process node

        Parameters
        ----------
        new_prerequisite_processes_list: List["Process"]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, prerequisite_processes=new_prerequisite_processes_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def conditions(self) -> List[Any]:
        """
        List of conditions present for this process

        Examples
        -------
        ```python
        # create condition node
        my_condition = cript.Condition(key="atm", type="min", value=1)

        my_process.conditions = [my_condition]
        ```

        Returns
        -------
        List[Condition]
            list of conditions for this process node
        """
        return self._json_attrs.conditions.copy()

    @conditions.setter
    def conditions(self, new_condition_list: List[Any]) -> None:
        """
        set the list of conditions for this process

        Parameters
        ----------
        new_condition_list: List[Condition]
            replace the conditions list
        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, conditions=new_condition_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def properties(self) -> List[Any]:
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
        return self._json_attrs.properties.copy()

    @properties.setter
    def properties(self, new_property_list: List[Any]) -> None:
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
        new_attrs = replace(self._json_attrs, properties=new_property_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keywords(self) -> List[str]:
        """
        List of keywords for this process

        [Process keywords](https://criptapp.org/keys/process-keyword/) must come from CRIPT controlled vocabulary

        Returns
        -------
        List[str]
            list of keywords for this process nod
        """
        return self._json_attrs.keywords.copy()

    @keywords.setter
    def keywords(self, new_keywords_list: List[str]) -> None:
        """
        set the list of keywords for this process from CRIPT controlled vocabulary

        Parameters
        ----------
        new_keywords_list: List[str]
            replace the current list of keywords

        Returns
        -------
        None
        """
        # TODO validate with CRIPT controlled vocabulary
        new_attrs = replace(self._json_attrs, keywords=new_keywords_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Any]:
        """
        List of citations for this process

        Examples
        --------
        ```python
        # crate reference node for this citation
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

        # create citation node
        my_citation = cript.Citation(type="derived_from", reference=my_reference)

        my_process.citations = [my_citation]
        ```

        Returns
        -------
        List[Citation]
            list of citations for this process node
        """
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations_list: List[Any]) -> None:
        """
        set the list of citations for this process

        Parameters
        ----------
        new_citations_list: List[Citation]
            replace the current list of citations

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citations=new_citations_list)
        self._update_json_attrs_if_valid(new_attrs)
