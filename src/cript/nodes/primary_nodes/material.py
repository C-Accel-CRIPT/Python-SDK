from dataclasses import dataclass, field, replace
from typing import List, Any

# from cript import Property, Process, ComputationalProcess
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Material(PrimaryBaseNode):
    """
    Material node

    [Material](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=10)
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Material attributes
        """

        node: str = "Material"
        # identifier sub-object for the material
        identifiers: List[dict[str, str]] = field(default_factory=dict)
        # TODO add proper typing in future, using Any for now to avoid circular import error
        components: List["Material"] = field(default_factory=list)
        properties: List[Any] = field(default_factory=list)
        process: List[Any] = field(default_factory=list)
        parent_materials: List["Material"] = field(default_factory=list)
        computation_forcefield: List[Any] = field(default_factory=list)
        keywords: List[str] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        identifiers: List[dict[str, str]],
        components: List["Material"] = None,
        properties: List[Any] = None,
        process: List[Any] = None,
        parent_materials: List["Material"] = None,
        computation_forcefield: List[Any] = None,
        keywords: List[str] = None,
        **kwargs
    ) -> None:
        """
        create a material node

        Parameters
        ----------
        identifiers: List[dict[str, str]]

        components: List["Material"], default=None
        properties: List[Property], default=None
        process: List[Process], default=None
        parent_materials: List["Material"], default=None
        computation_forcefield: List[ComputationalProcess], default=None
        keywords: List[str], default=None

        Returns
        -------
        None
        """

        super().__init__(node="Material")

        # validate keywords if they exist
        if keywords is not None:
            self._validate_keywordss(keywordss=keywords)

        self._json_attrs = replace(
            self._json_attrs,
            identifiers=identifiers,
            components=components,
            properties=properties,
            process=process,
            parent_materials=parent_materials,
            computation_forcefield=computation_forcefield,
            keywords=keywords,
        )

    # ------------ Properties ------------
    @property
    def identifiers(self) -> List[dict[str, str]]:
        """
        get the identifiers for this material

        Returns
        -------
        List[dict[str, str]]
        """
        return self._json_attrs.identifiers.copy()

    @identifiers.setter
    def identifiers(self, new_identifiers_list: List[dict[str, str]]) -> None:
        """
        set the list of identifiers for this material

        the identifier keys must come from the
        material identifiers keywords within the CRIPT controlled vocabulary

        Parameters
        ----------
        new_identifiers_list: List[dict[str, str]]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, identifiers=new_identifiers_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def components(self) -> List["Material"]:
        """
        get the list of components  (material nodes) that make up this material

        Returns
        -------
        None
        """
        return self._json_attrs.components

    @components.setter
    def components(self, new_components_list: List["Material"]) -> None:
        """
        set the list of components (material nodes) that make up this material

        Parameters
        ----------
        new_components_list: List["Material"]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, components=new_components_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def properties(self) -> List[Any]:
        """
        get the list of material properties

        Returns
        -------
        List[Property]
        """
        return self._json_attrs.properties

    @properties.setter
    def properties(self, new_properties_list: List[Any]) -> None:
        """
        set the list of properties for this material

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
    def process(self) -> List[Any]:
        """
        get the list of process for this material

        Returns
        -------
        List[Process]
        """
        return self._json_attrs.process

    @process.setter
    def process(self, new_process_list: List[Any]) -> None:
        """
        set the list of process for this material

        Parameters
        ----------
        new_process_list: List[Process]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, process=new_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def parent_materials(self) -> List["Material"]:
        """
        get the list of parent materials

        Returns
        -------
        List["Material"]
        """
        return self._json_attrs.parent_materials

    @parent_materials.setter
    def parent_materials(self, new_parent_materials_list: List["Material"]) -> None:
        """
        set the parent materials for this material

        Parameters
        ----------
        new_parent_materials_list: List["Material"]

        Returns
        -------
        None
        """

        new_attrs = replace(
            self._json_attrs, parent_materials=new_parent_materials_list
        )
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computation_forcefield(self) -> List[Any]:
        """
        get the computation_forcefield for this material node

        Returns
        -------
        None
        """
        return self._json_attrs.computation_forcefield

    @computation_forcefield.setter
    def computation_forcefield(
        self, new_computation_forcefield_list: List[Any]
    ) -> None:
        """
        sets the list of computation forcefields for this material

        Parameters
        ----------
        new_computation_forcefield_list: List[ComputationalProcess]

        Returns
        -------
        None
        """
        new_attrs = replace(
            self._json_attrs, computation_forcefield=new_computation_forcefield_list
        )
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keywords(self) -> List[str]:
        """
        get the list of keywords for this material

        the material keywords must come from the CRIPT controlled vocabulary

        Returns
        -------
        None
        """
        return self._json_attrs.keywords

    @keywords.setter
    def keywords(self, new_keywords_list: List[str]) -> None:
        """
        set the keywords for this material

        the material keywords must come from the CRIPT controlled vocabulary

        Parameters
        ----------
        new_keywords_list

        Returns
        -------
        None
        """
        # TODO validate keywords before setting them
        self._validate_keywords(keywords=new_keywords_list)

        new_attrs = replace(self._json_attrs, keywords=new_keywords_list)
        self._update_json_attrs_if_valid(new_attrs)

    # ------------ validation ------------
    # TODO this can be a function instead of a method
    def _validate_keywords(self, keywords: List[str]) -> None:
        """
        takes a list of material keywords and loops through validating every single one

        this is a simple loop that calls another method, but I thought it needs to be made into a method
        since both constructor and keywords setter has the same code

        Parameters
        ----------
        keywords: List[str]

        Returns
        -------
        None
        """
        # TODO add this validation in the future
        # for keywords in keywords:
        #     is_vocab_valid(keywords)
        pass

    # TODO this can be a function instead of a method
    def _validate_identifiers(self, identifiers: List[dict[str, str]]) -> None:
        """
        takes a list of material identifiers and loops through validating every single one

        since validation is needed in both constructor and the setter, this is a simple method for it

        Parameters
        ----------
        identifiers: List[dict[str, str]]

        Returns
        -------
        None
        """

        for identifier_dictionary in identifiers:
            for key, value in identifier_dictionary.items():
                # TODO validate keys here
                # is_vocab_valid("material_identifiers", value)
                pass
