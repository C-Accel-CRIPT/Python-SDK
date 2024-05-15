import warnings
from dataclasses import dataclass, field, replace
from typing import Any, List, Optional, Union

from beartype import beartype

from cript.nodes.exceptions import CRIPTMaterialIdentifierWarning
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.process import Process
from cript.nodes.util.json import UIDProxy


class Material(PrimaryBaseNode):
    """
    ## Definition
    A [Material node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=10)
    is a collection of the properties of a chemical, mixture, or substance.

    ## Attributes
    | attribute                 | type                                                                 | example                                           | description                                         | required    | vocab |
    |---------------------------|----------------------------------------------------------------------|---------------------------------------------------|-----------------------------------------------------|-------------|-------|
    | component                 | list[[Material](./)]                                                 |                                                   | list of component that make up the mixture          |             |       |
    | property                  | list[[Property](../../subobjects/property)]                          |                                                   | material properties                                 |             |       |
    | process                   | [Process](../process)                                                |                                                   | process node that made this material                |             |       |
    | parent_material           | [Material](./)                                                       |                                                   | material node that this node was copied from        |             |       |
    | computational_forcefield  | [Computation  Forcefield](../../subobjects/computational_forcefield) |                                                   | computation forcefield                              | Conditional |       |
    | keyword                   | list[str]                                                            | [thermoplastic, homopolymer, linear, polyolefins] | words that classify the material                    |             | True  |
    | notes                     | str                                                                  | "my awesome notes"                                | miscellaneous information, or custom data structure |             | True  |
    | amino_acid                | str                                                                  | "LeuProHis"                                       | if the material is an amino acid sequence, list it. | Conditional |       |
    | bigsmiles                 | str                                                                  | "CC{[$][$]CC[$][]}"                               | BigSMILES string for polymer                        | Conditional |       |
    | chem_formula              | str                                                                  | "C22H33NO10"                                      | Chemical formula of the material or monomer        | Conditional |       |
    | chem_repeat               | str                                                                  | "C=Cc1ccccc1"                                     | Chemical formula of the repeat unit                | Conditional |       |
    | chemical_id               | str                                                                  | "126094"                                          | Unique chemical ID                                  | Conditional |       |
    | inchi                     | str                                                                  | "InChI=1S/H2O/h1H2"                               | InChI string of the chemical                        | Conditional |       |
    | inchi_key                 | str                                                                  | "XLYOFNOQVPJJNP-UHFFFAOYSA-N"                     | InChI key of the chemical                           | Conditional |       |
    | lot_number                | str                                                                  | "123"                                             | Lot number of the chemical                          | Conditional |       |
    | names                     | list[str]                                                            | ["water", "Hydrogen oxide"]                       | Alternative names that are being used               | Conditional |       |
    | pubchem_cid               | int                                                                  | 962                                               | PubChemID of the chemical                           | Conditional |       |
    | smiles                    | str                                                                  | "O"                                               | Smiles string of the chemical                       | Conditional |       |
    | vendor                    | str                                                                  | "fisher scientific"                               | Vendor the chemical was purchased from              | Conditional |       |


    ## Navigating to Material
    Materials can be easily found on the [CRIPT](https://app.criptapp.org) home screen in the
    under the navigation within the [Materials link](https://app.criptapp.org/material/)

    ## Available Sub-Objects for Material
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

        # TODO add proper typing in future, using Any for now to avoid circular import error
        component: List[Union["Material", UIDProxy]] = field(default_factory=list)
        process: Optional[Union[Process, UIDProxy]] = None
        property: List[Union[Any, UIDProxy]] = field(default_factory=list)
        parent_material: Optional[Union["Material", UIDProxy]] = None
        computational_forcefield: Optional[Union[Any, UIDProxy]] = None
        keyword: List[str] = field(default_factory=list)
        amino_acid: Optional[str] = None
        bigsmiles: Optional[str] = None
        chem_formula: Optional[str] = None
        chem_repeat: List[str] = field(default_factory=list)
        chemical_id: Optional[str] = None
        inchi: Optional[str] = None
        inchi_key: Optional[str] = None
        lot_number: Optional[str] = None
        names: List[str] = field(default_factory=list)
        pubchem_cid: Optional[int] = None
        smiles: Optional[str] = None
        vendor: Optional[str] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        name: str,
        component: Optional[List[Union["Material", UIDProxy]]] = None,
        process: Optional[Union[Process, UIDProxy]] = None,
        property: Optional[List[Union[Any, UIDProxy]]] = None,
        parent_material: Optional[Union["Material", UIDProxy]] = None,
        computational_forcefield: Optional[Union[Any, UIDProxy]] = None,
        keyword: Optional[List[str]] = None,
        amino_acid: Optional[str] = None,
        bigsmiles: Optional[str] = None,
        chem_formula: Optional[str] = None,
        chem_repeat: Optional[List[str]] = None,
        chemical_id: Optional[str] = None,
        inchi: Optional[str] = None,
        inchi_key: Optional[str] = None,
        lot_number: Optional[str] = None,
        names: Optional[List[str]] = None,
        pubchem_cid: Optional[int] = None,
        smiles: Optional[str] = None,
        vendor: Optional[str] = None,
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
        ...     amino_acid = "component 1 alternative name",
        ... )

        Parameters
        ----------
        name: str
        component: List["Material"], default=None
        property: Optional[Process], default=None
        process: List[Process], default=None
        parent_material: "Material", default=None
        computational_forcefield: ComputationalForcefield, default=None
        keyword: List[str], default=None
        amino_acid: Optional[str] = None,
        bigsmiles: Optional[str] = None,
        chem_formula: Optional[str] = None,
        chem_repeat: Optional[List[str]] = None,
        chemical_id: Optional[str] = None,
        inchi: Optional[str] = None,
        inchi_key: Optional[str] = None,
        lot_number: Optional[str] = None,
        names: Optional[List[str]] = None,
        pubchem_cid: Optional[int] = None,
        smiles: Optional[str] = None,
        vendor: Optional[str] = None,

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

        if chem_repeat is None:
            chem_repeat = []

        if names is None:
            names = []

        new_json_attrs = replace(
            self._json_attrs,
            name=name,
            component=component,
            process=process,
            property=property,
            parent_material=parent_material,
            computational_forcefield=computational_forcefield,
            keyword=keyword,
            amino_acid=amino_acid,
            bigsmiles=bigsmiles,
            chem_formula=chem_formula,
            chem_repeat=chem_repeat,
            chemical_id=chemical_id,
            inchi=inchi,
            inchi_key=inchi_key,
            lot_number=lot_number,
            names=names,
            pubchem_cid=pubchem_cid,
            smiles=smiles,
            vendor=vendor,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    def validate(self, api=None, is_patch: bool = False, force_validation: bool = False) -> None:
        super().validate(api=api, is_patch=is_patch, force_validation=force_validation)

        if (
            self.amino_acid is None
            and self.bigsmiles is None
            and self.chem_formula is None
            and len(self.chem_repeat) == 0
            and self.chemical_id is None
            and self.inchi_key is None
            and self.inchi is None
            and self.lot_number is None
            and len(self.names) == 0
            and self.pubchem_cid is None
            and self.smiles is None
            and self.vendor is None
        ):
            warnings.warn(CRIPTMaterialIdentifierWarning(self))

    @property
    @beartype
    def amino_acid(self) -> Union[str, None]:
        return self._json_attrs.amino_acid

    @amino_acid.setter
    @beartype
    def amino_acid(self, new_amino_acid: str) -> None:
        new_attrs = replace(self._json_attrs, amino_acid=new_amino_acid)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def bigsmiles(self) -> Union[str, None]:
        return self._json_attrs.bigsmiles

    @bigsmiles.setter
    @beartype
    def bigsmiles(self, new_bigsmiles: str) -> None:
        new_attrs = replace(self._json_attrs, bigsmiles=new_bigsmiles)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def chem_formula(self) -> Union[str, None]:
        return self._json_attrs.chem_formula

    @chem_formula.setter
    @beartype
    def chem_formula(self, new_chem_formula: str) -> None:
        new_attrs = replace(self._json_attrs, chem_formula=new_chem_formula)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def chemical_id(self) -> Union[str, None]:
        return self._json_attrs.chemical_id

    @chemical_id.setter
    @beartype
    def chemical_id(self, new_chemical_id: str) -> None:
        new_attrs = replace(self._json_attrs, chemical_id=new_chemical_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def inchi(self) -> Union[str, None]:
        return self._json_attrs.inchi

    @inchi.setter
    @beartype
    def inchi(self, new_inchi: str) -> None:
        new_attrs = replace(self._json_attrs, inchi=new_inchi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def inchi_key(self) -> Union[str, None]:
        return self._json_attrs.inchi_key

    @inchi_key.setter
    @beartype
    def inchi_key(self, new_inchi_key: str) -> None:
        new_attrs = replace(self._json_attrs, inchi_key=new_inchi_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def lot_number(self) -> Union[str, None]:
        return self._json_attrs.lot_number

    @lot_number.setter
    @beartype
    def lot_number(self, new_lot_number: str) -> None:
        new_attrs = replace(self._json_attrs, lot_number=new_lot_number)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def smiles(self) -> Union[str, None]:
        return self._json_attrs.smiles

    @smiles.setter
    @beartype
    def smiles(self, new_smiles: str) -> None:
        new_attrs = replace(self._json_attrs, smiles=new_smiles)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def vendor(self) -> Union[str, None]:
        return self._json_attrs.vendor

    @vendor.setter
    @beartype
    def vendor(self, new_vendor: str) -> None:
        new_attrs = replace(self._json_attrs, vendor=new_vendor)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def chem_repeat(self) -> List[str]:
        return self._json_attrs.chem_repeat.copy()

    @chem_repeat.setter
    @beartype
    def chem_repeat(self, new_chem_repeat: List[str]) -> None:
        new_attrs = replace(self._json_attrs, chem_repeat=new_chem_repeat)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def names(self) -> List[str]:
        return self._json_attrs.names.copy()

    @names.setter
    @beartype
    def names(self, new_names: List[str]) -> None:
        new_attrs = replace(self._json_attrs, names=new_names)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def pubchem_cid(self) -> Union[int, None]:
        return self._json_attrs.pubchem_cid

    @pubchem_cid.setter
    @beartype
    def pubchem_cid(self, new_pubchem_cid: int) -> None:
        new_attrs = replace(self._json_attrs, pubchem_cid=new_pubchem_cid)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def component(self) -> List[Union["Material", UIDProxy]]:
        """
        list of components ([material nodes](./)) that make up this material

        Examples
        ---------
        >>> import cript
        >>> my_components = [
        ...     cript.Material(
        ...         name="my component material 1",
        ...         smiles="my material smiles",
        ...     ),
        ...     cript.Material(
        ...         name="my component material 2",
        ...         vendor= "my material vendor",
        ...     ),
        ... ]
        >>> my_mixed_material = cript.Material(
        ...     name="my material",
        ...     component=my_components,
        ...     bigsmiles = "123456",
        ... )

        Returns
        -------
        List[Material]
            list of component that make up this material
        """
        return self._json_attrs.component

    @component.setter
    @beartype
    def component(self, new_component_list: List[Union["Material", UIDProxy]]) -> None:
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
    def parent_material(self) -> Optional[Union["Material", UIDProxy]]:
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
    def parent_material(self, new_parent_material: Optional[Union["Material", UIDProxy]]) -> None:
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
        ...     name="my component material 1", smiles= "my smiles"
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
    def computational_forcefield(self, new_computational_forcefield: Any) -> None:
        """
        sets the list of computational forcefields for this material

        Parameters
        ----------
        new_computation_forcefield: ComputationalForcefield

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computational_forcefield=new_computational_forcefield)
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
        ... name="my material", inchi = "my material inchi"
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
    def process(self) -> Optional[Union[Process, UIDProxy]]:
        return self._json_attrs.process  # type: ignore

    @process.setter
    def process(self, new_process: Union[Process, UIDProxy]) -> None:
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
        ...     smiles = "component 1 smiles",
        ... )
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.23, unit="J")
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
