from dataclasses import dataclass, field, replace
from typing import Any, List

# from cript import Ingredient, Equipment, Material, Condition, Property, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Process(PrimaryBaseNode):
    """
    Process Node
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

        the only required argument is ingredient
        the rest of the arguments are optional. They can either be set now or later
        Parameters
        ----------
        ingredients: List[Ingredient]
        type: str = ""
        description: str = ""
        equipments: List[Equipment] = None
        products: List[Material] = None
        waste: List[Material] = None
        conditions: List[Condition] = None
        properties: List[Property] = None
        keywords: List[str] = None
        citations: List[Citation] = None
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

        super().__init__(node="Process", name=name, notes=notes)

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
        Get the type of the process

        Process type comes from CRIPT controlled vocabulary

        Returns
        -------
        str
            type of the process (CRIPT controlled vocabulary)
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
        get a list of ingredients for this process

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
        get the description of this process

        Returns
        -------
        None
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
        get the equipments for this process

        Returns
        -------
        None
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
        get the list of products for this process

        Returns
        -------
        List[Material]
            get a list of process products (Material nodes)
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
        get the list of waste that resulted from this process

        Returns
        -------
        None
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
        get the prerequisite process node

        Returns
        -------
        List[Process]
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
        get a list of conditions present for this process

        Returns
        -------
        None
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
        get the list of Property nodes for this process

        Returns
        -------
        None
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
        get a list of keywords for this process

        Returns
        -------
        List[str]
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
        get the list of citations for this process

        Returns
        -------
        List[Citation]
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
