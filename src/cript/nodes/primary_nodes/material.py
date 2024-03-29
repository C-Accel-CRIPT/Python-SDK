from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional

from beartype import beartype

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.process import Process


class Material(PrimaryBaseNode):
    """
    ## Definition
    A [Material node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=10)
    is a collection of the identifiers and properties of a chemical, mixture, or substance.

    ## Attributes
    | attribute                 | type                                                                 | example                                           | description                                         | required    | vocab |
    |---------------------------|----------------------------------------------------------------------|---------------------------------------------------|-----------------------------------------------------|-------------|-------|
    | identifier                | list[Identifier]                                                     |                                                   | material identifiers                                | True        |       |
    | component                 | list[[Material](./)]                                                 |                                                   | list of component that make up the mixture          |             |       |
    | property                  | list[[Property](../../subobjects/property)]                          |                                                   | material properties                                 |             |       |
    | process                   | [Process](../process)                                                |                                                   | process node that made this material                |             |       |
    | parent_material           | [Material](./)                                                       |                                                   | material node that this node was copied from        |             |       |
    | computational_forcefield  | [Computation  Forcefield](../../subobjects/computational_forcefield) |                                                   | computation forcefield                              | Conditional |       |
    | keyword                   | list[str]                                                            | [thermoplastic, homopolymer, linear, polyolefins] | words that classify the material                    |             | True  |
    | notes                     | str                                                                  | "my awesome notes"                                | miscellaneous information, or custom data structure |             | True  |

    ## Navigating to Material
    Materials can be easily found on the [CRIPT](https://app.criptapp.org) home screen in the
    under the navigation within the [Materials link](https://app.criptapp.org/material/)

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
         "node":["Material"],
         "name":"my unique material name",
         "uid":"_:9679ff12-f9b4-41f4-be95-080b78fa71fd",
         "uuid":"9679ff12-f9b4-41f4-be95-080b78fa71fd"
         "bigsmiles":"[H]{[>][<]C(C[>])c1ccccc1[]}",
      }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Material attributes
        """

        # identifier sub-object for the material
        identifier: List[Dict[str, str]] = field(default_factory=dict)  # type: ignore
        # TODO add proper typing in future, using Any for now to avoid circular import error
        component: List["Material"] = field(default_factory=list)
        process: Optional[Process] = None
        property: List[Any] = field(default_factory=list)
        parent_material: Optional["Material"] = None
        computational_forcefield: Optional[Any] = None
        keyword: List[str] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        name: str,
        identifier: List[Dict[str, str]],
        component: Optional[List["Material"]] = None,
        process: Optional[Process] = None,
        property: Optional[List[Any]] = None,
        parent_material: Optional["Material"] = None,
        computational_forcefield: Optional[Any] = None,
        keyword: Optional[List[str]] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a material node

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(
        ...     name="my component material 1",
        ...     identifier=[{"amino_acid": "component 1 alternative name"}],
        ... )

        Parameters
        ----------
        name: str
        identifier: List[Dict[str, str]]
        component: List["Material"], default=None
        property: Optional[Process], default=None
        process: List[Process], default=None
        parent_material: "Material", default=None
        computational_forcefield: ComputationalForcefield, default=None
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

        if keyword is None:
            keyword = []

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            identifier=identifier,
            component=component,
            process=process,
            property=property,
            parent_material=parent_material,
            computational_forcefield=computational_forcefield,
            keyword=keyword,
        )

    @property
    @beartype
    def identifier(self) -> List[Dict[str, str]]:
        """
        get the identifiers for this material

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(
        ...     name="my component material 1",
        ...     identifier=[{"smiles": "component 1 smiles"}],
        ... )
        >>> my_material.identifier = [{"smiles": "my material alternative name"}]

        [material identifier key](https://app.criptapp.org/vocab/material_identifier_key)
        must come from CRIPT controlled vocabulary

        Returns
        -------
        List[Dict[str, str]]
            list of dictionary that has identifiers for this material
        """
        return self._json_attrs.identifier.copy()

    @identifier.setter
    @beartype
    def identifier(self, new_identifier_list: List[Dict[str, str]]) -> None:
        """
        set the list of identifiers for this material

        the identifier keys must come from the
        material identifiers keyword within the CRIPT controlled vocabulary

        Parameters
        ----------
        new_identifier_list: List[Dict[str, str]]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, identifier=new_identifier_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def component(self) -> List["Material"]:
        """
        list of components ([material nodes](./)) that make up this material

        Examples
        ---------
        >>> import cript
        >>> my_components = [
        ...     cript.Material(
        ...         name="my component material 1",
        ...         identifier=[{"smiles": "my material smiles"}],
        ...     ),
        ...     cript.Material(
        ...         name="my component material 2",
        ...         identifier=[{"vendor": "my material vendor"}],
        ...     ),
        ... ]
        >>> my_mixed_material = cript.Material(
        ...     name="my material",
        ...     component=my_components,
        ...     identifier=[{"bigsmiles": "123456"}]
        ... )

        Returns
        -------
        List[Material]
            list of component that make up this material
        """
        return self._json_attrs.component

    @component.setter
    @beartype
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
    @beartype
    def parent_material(self) -> Optional["Material"]:
        """
        List of parent materials

        Returns
        -------
        List["Material"]
            list of parent materials
        """
        return self._json_attrs.parent_material

    @parent_material.setter
    @beartype
    def parent_material(self, new_parent_material: Optional["Material"]) -> None:
        """
        set the [parent materials](./) for this material

        Parameters
        ----------
        new_parent_material: "Material"

        Returns
        -------
        None
        """

        new_attrs = replace(self._json_attrs, parent_material=new_parent_material)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def computational_forcefield(self) -> Any:
        """
        list of [computational_forcefield](../../subobjects/computational_forcefield) for this material node

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(
        ...     name="my component material 1", identifier=[{"smiles": "my smiles"}]
        ... )
        >>> my_computational_forcefield = cript.ComputationalForcefield(
        ...     key="opls_aa",
        ...     building_block="atom",
        ... )
        >>> my_material.computational_forcefield = my_computational_forcefield

        Returns
        -------
        List[ComputationForcefield]
            list of computational_forcefield that created this material
        """
        return self._json_attrs.computational_forcefield

    @computational_forcefield.setter
    @beartype
    def computational_forcefield(self, new_computational_forcefield_list: Any) -> None:
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
    @beartype
    def keyword(self) -> List[str]:
        """
        List of keyword for this material

        the material keyword must come from the
        [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/material_keyword)

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(
        ... name="my material", identifier=[{"inchi": "my material inchi"}]
        ... )
        >>> my_material.keyword = ["acetylene", "acrylate", "alternating"]

        Returns
        -------
        List[str]
            list of material keyword
        """
        return self._json_attrs.keyword

    @keyword.setter
    @beartype
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
        new_attrs = replace(self._json_attrs, keyword=new_keyword_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def process(self) -> Optional[Process]:
        return self._json_attrs.process  # type: ignore

    @process.setter
    def process(self, new_process: Process) -> None:
        new_attrs = replace(self._json_attrs, process=new_process)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def property(self) -> List[Any]:
        """
        list of material [property](../../subobjects/property)

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(
        ...     name="my component material 1",
        ...     identifier=[{"smiles": "component 1 smiles"}],
        ... )
        >>> my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")
        >>> my_material.property = [my_property]

        Returns
        -------
        List[Property]
            list of property that define this material
        """
        return self._json_attrs.property.copy()

    @property.setter
    @beartype
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
    @beartype
    def _from_json(cls, json_dict: Dict):
        """
        Create a new instance of a node from a JSON representation.

        Parameters
        ----------
        json_dict : Dict
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
        * `identifier`: A list of material identifiers.
            * If the `identifier` property is not present in the JSON dictionary,
            it will be set to an empty list.
        """
        from cript.nodes.util.material_deserialization import (
            _deserialize_flattened_material_identifiers,
        )

        json_dict = _deserialize_flattened_material_identifiers(json_dict)

        return super()._from_json(json_dict)
