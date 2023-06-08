from dataclasses import dataclass, field, replace
from typing import Any, List

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Material(PrimaryBaseNode):
    """
    ## Definition
    A [Material node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=10)
    is nested inside a [Project](../project).
    A [Material node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=10)
    is just the materials used within an project/experiment.

    ## Attributes
    | attribute               | type                                                | example                                           | description                                  | required    | vocab |
    |-------------------------|-----------------------------------------------------|---------------------------------------------------|----------------------------------------------|-------------|-------|
    | identifiers             | list[Identifier]                                    |                                                   | material identifiers                         | True        |       |
    | component              | list[[Material](./)]                                |                                                   | list of component that make up the mixture  |             |       |
    | property              | list[[Property](../subobjects/property)]            |                                                   | material properties                          |             |       |
    | process                 | [Process](../process)                               |                                                   | process node that made this material         |             |       |
    | parent_material         | [Material](./)                                      |                                                   | material node that this node was copied from |             |       |
    | computational_ forcefield | [Computation  Forcefield](../computational_forcefield) |                                                   | computation forcefield                       | Conditional |       |
    | keyword                | list[str]                                           | [thermoplastic, homopolymer, linear, polyolefins] | words that classify the material             |             | True  |

    ## Navigating to Material
    Materials can be easily found on the [CRIPT](https://criptapp.org) home screen in the
    under the navigation within the [Materials link](https://criptapp.org/material/)

    ## Available Sub-Objects for Material
    * [Identifier](../../subobjects/identifier)
    * [Property](../../subobjects/property)
    * [Computational_forcefield](../../subobjects/computational_forcefield)

    Example
    -------
     water, brine (water + NaCl), polystyrene, polyethylene glycol hydrogels, vulcanized polyisoprene, mcherry (protein), and mica


    Warnings
    -------
    !!! warning "Material names"
        Material names Must be unique within a [Project](../project)

    ```json
    {
        "name": "my unique material",
        "component_count": 0,
        "computational_forcefield_count": 0,
        "created_at": "2023-03-14T00:45:02.196297Z",
        "identifier_count": 0,
        "identifiers": [],
        "model_version": "1.0.0",
        "node": "Material",
        "notes": "",
        "property_count": 0,
        "uid": "0x24a08",
        "updated_at": "2023-03-14T00:45:02.196276Z",
        "uuid": "403fa02c-9a84-4f9e-903c-35e535151b08",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Material attributes
        """

        # identifier sub-object for the material
        identifiers: List[dict[str, str]] = field(default_factory=dict)
        # TODO add proper typing in future, using Any for now to avoid circular import error
        component: List["Material"] = field(default_factory=list)
        property: List[Any] = field(default_factory=list)
        parent_material: List["Material"] = field(default_factory=list)
        computational_forcefield: List[Any] = field(default_factory=list)
        keyword: List[str] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        identifiers: List[dict[str, str]],
        component: List["Material"] = None,
        property: List[Any] = None,
        parent_material: List["Material"] = None,
        computational_forcefield: List[Any] = None,
        keyword: List[str] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a material node

        Parameters
        ----------
        name: str
        identifiers: List[dict[str, str]]
        component: List["Material"], default=None
        property: List[Property], default=None
        process: List[Process], default=None
        parent_material: List["Material"], default=None
        computational_forcefield: List[ComputationalProcess], default=None
        keyword: List[str], default=None

        Returns
        -------
        None
            Instantiate a material node
        """

        super().__init__(name=name, notes=notes, **kwargs)

        if component is None:
            component = []

        if property is None:
            property = []

        if parent_material is None:
            parent_material = []

        if computational_forcefield is None:
            computational_forcefield = []

        if keyword is None:
            keyword = []

        # validate keyword if they exist
        if keyword is not None:
            self._validate_keyword(keyword=keyword)

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            identifiers=identifiers,
            component=component,
            property=property,
            parent_material=parent_material,
            computational_forcefield=computational_forcefield,
            keyword=keyword,
        )

    # ------------ Properties ------------
    @property
    def name(self) -> str:
        """
        material name

        Examples
        ```python
        my_material.name = "my new material"
        ```

        Returns
        -------
        str
            material name
        """
        return self._json_attrs.name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        set the name of the material

        Parameters
        ----------
        new_name: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def identifiers(self) -> List[dict[str, str]]:
        """
        get the identifiers for this material

        ```python
        my_material.identifier = {"alternative_names": "my material alternative name"}
        ```

        Returns
        -------
        List[dict[str, str]]
            list of dictionary that has identifiers for this material
        """
        return self._json_attrs.identifiers.copy()

    @identifiers.setter
    def identifiers(self, new_identifiers_list: List[dict[str, str]]) -> None:
        """
        set the list of identifiers for this material

        the identifier keys must come from the
        material identifiers keyword within the CRIPT controlled vocabulary

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
    def component(self) -> List["Material"]:
        """
        list of component ([material nodes](./)) that make up this material

        Examples
        --------
        ```python
        # material component
        my_component = [
            cript.Material(
                name="my component material 1",
                identifiers=[{"alternative_names": "component 1 alternative name"}],
            ),
            cript.Material(
                name="my component material 2",
                identifiers=[{"alternative_names": "component 2 alternative name"}],
            ),
        ]


        identifiers = [{"alternative_names": "my material alternative name"}]
        my_material = cript.Material(name="my material", component=my_component, identifiers=identifiers)
        ```

        Returns
        -------
        List[Material]
            list of component that make up this material
        """
        return self._json_attrs.component

    @component.setter
    def component(self, new_component_list: List["Material"]) -> None:
        """
        set the list of component (material nodes) that make up this material

        Parameters
        ----------
        new_component_list: List["Material"]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, component=new_component_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def parent_material(self) -> List["Material"]:
        """
        List of parent materials

        Returns
        -------
        List["Material"]
            list of parent materials
        """
        return self._json_attrs.parent_material

    @parent_material.setter
    def parent_material(self, new_parent_material_list: List["Material"]) -> None:
        """
        set the [parent materials](./) for this material

        Parameters
        ----------
        new_parent_material_list: List["Material"]

        Returns
        -------
        None
        """

        new_attrs = replace(self._json_attrs, parent_material=new_parent_material_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computational_forcefield(self) -> List[Any]:
        """
        list of [computational_forcefield](../../subobjects/computational_forcefield) for this material node

        Returns
        -------
        List[ComputationForcefield]
            list of computational_forcefield that created this material
        """
        return self._json_attrs.computational_forcefield

    @computational_forcefield.setter
    def computational_forcefield(self, new_computational_forcefield_list: List[Any]) -> None:
        """
        sets the list of computational forcefields for this material

        Parameters
        ----------
        new_computation_forcefield_list: List[ComputationalForcefield]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computational_forcefield=new_computational_forcefield_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keyword(self) -> List[str]:
        """
        List of keyword for this material

        the material keyword must come from the
        [CRIPT controlled vocabulary](https://criptapp.org/keys/material-keyword/)

        ```python
        identifiers = [{"alternative_names": "my material alternative name"}]

        # keyword
        material_keyword = ["acetylene", "acrylate", "alternating"]

        my_material = cript.Material(
            name="my material", keyword=material_keyword, identifiers=identifiers
        )
        ```

        Returns
        -------
        List[str]
            list of material keyword
        """
        return self._json_attrs.keyword

    @keyword.setter
    def keyword(self, new_keyword_list: List[str]) -> None:
        """
        set the keyword for this material

        the material keyword must come from the CRIPT controlled vocabulary

        Parameters
        ----------
        new_keyword_list

        Returns
        -------
        None
        """
        # TODO validate keyword before setting them
        self._validate_keyword(keyword=new_keyword_list)

        new_attrs = replace(self._json_attrs, keyword=new_keyword_list)
        self._update_json_attrs_if_valid(new_attrs)

    # ------------ validation ------------
    # TODO this can be a function instead of a method
    def _validate_keyword(self, keyword: List[str]) -> None:
        """
        takes a list of material keyword and loops through validating every single one

        this is a simple loop that calls another method, but I thought it needs to be made into a method
        since both constructor and keyword setter has the same code

        Parameters
        ----------
        keyword: List[str]

        Returns
        -------
        None
        """
        # TODO add this validation in the future
        # for keyword in keyword:
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

    @property
    def property(self) -> List[Any]:
        """
        list of material [property](../../subobjects/property)

        ```python
        # property subobject
        my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

        my_material.property = my_property
        ```

        Returns
        -------
        List[Property]
            list of property that define this material
        """
        return self._json_attrs.property.copy()

    @property.setter
    def property(self, new_property_list: List[Any]) -> None:
        """
        set the list of properties for this material

        Parameters
        ----------
        new_property_list: List[Property]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, property=new_property_list)
        self._update_json_attrs_if_valid(new_attrs)

    @classmethod
    def _from_json(cls, json_dict: dict):
        """
        Create a new instance of a node from a JSON representation.

        Parameters
        ----------
        json_dict : dict
            A JSON dictionary representing a node

        Returns
        -------
        node
            A new instance of a node.

        Notes
        -----
        required fields in JSON:
        * `name`: The name of the node

        optional fields in JSON:
        * `identifiers`: A list of material identifiers.
            * If the `identifiers` property is not present in the JSON dictionary,
            it will be set to an empty list.
        """
        from cript.nodes.util.material_deserialization import (
            _deserialize_flattened_material_identifiers,
        )

        json_dict = _deserialize_flattened_material_identifiers(json_dict)

        return super()._from_json(json_dict)
