from dataclasses import dataclass, field, replace
from typing import Any, List, Union

# from cript import Property, Process, ComputationalProcess
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
    | component              | list[[Material](./)]                                |                                                   | list of components that make up the mixture  |             |       |
    | properties              | list[[Property](../subobjects/property)]            |                                                   | material properties                          |             |       |
    | process                 | [Process](../process)                               |                                                   | process node that made this material         |             |       |
    | parent_material         | [Material](./)                                      |                                                   | material node that this node was copied from |             |       |
    | computation_ forcefield | [Computation  Forcefield](../computational_process) |                                                   | computation forcefield                       | Conditional |       |
    | keyword                | list[str]                                           | [thermoplastic, homopolymer, linear, polyolefins] | words that classify the material             |             | True  |

    ## Navigating to Material
    Materials can be easily found on the [CRIPT](https://criptapp.org) home screen in the
    under the navigation within the [Materials link](https://criptapp.org/material/)

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
        "name": "my unique material",
        "component_count": 0,
        "computational_forcefield_count": 0,
        "created_at": "2023-03-14T00:45:02.196297Z",
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
        properties: List[Any] = field(default_factory=list)
        process: List[Any] = field(default_factory=list)
        parent_material: List["Material"] = field(default_factory=list)
        computation_forcefield: List[Any] = field(default_factory=list)
        keyword: List[str] = field(default_factory=list)
        bigsmiles: str = ""
        cas: str = ""
        chem_formula: str = ""
        inchi: str = ""
        inchi_key: str = ""
        mol_form: str = ""
        pubchem_cid: Union[int, None] = None
        smiles: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        component: List["Material"] = None,
        properties: List[Any] = None,
        process: List[Any] = None,
        parent_material: List["Material"] = None,
        computation_forcefield: List[Any] = None,
        keyword: List[str] = None,
        notes: str = "",
        bigsmiles: str = "",
        cas: str = "",
        chem_formula: str = "",
        inchi: str = "",
        inchi_key: str = "",
        mol_form: str = "",
        # TODO assign default
        pubchem_cid: Union[int, None] = None,
        smiles: str = "",
        **kwargs
    ):
        """
        create a material node

        Parameters
        ----------
        name: str
        component: List["Material"], default=None
        properties: List[Property], default=None
        process: List[Process], default=None
        parent_material: List["Material"], default=None
        computation_forcefield: List[ComputationalProcess], default=None
        keyword: List[str], default=None
        bigsmiles: str = "",
        cas: str = "",
        chem_formula: str = "",
        inchi: str="",
        inchi_key: str = "",
        mol_form: str = "",
        pubchem_cid: Union[int, None] = None,
        smiles: str = "",

        Returns
        -------
        None
            Instantiate a material node
        """

        super().__init__(name=name, notes=notes, **kwargs)

        if component is None:
            component = []

        if properties is None:
            properties = []

        if process is None:
            process = []

        if parent_material is None:
            parent_material = []

        if computation_forcefield is None:
            computation_forcefield = []

        if keyword is None:
            keyword = []

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            component=component,
            properties=properties,
            process=process,
            parent_material=parent_material,
            computation_forcefield=computation_forcefield,
            keyword=keyword,
            bigsmiles=bigsmiles,
            cas=cas,
            chem_formula=chem_formula,
            inchi=inchi,
            inchi_key=inchi_key,
            mol_form=mol_form,
            pubchem_cid=pubchem_cid,
            smiles=smiles,
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
    def bigsmiles(self) -> str:
        return self._json_attrs.bigsmiles

    @bigsmiles.setter
    def bigsmiles(self, new_bigsmiles: str):
        new_attrs = replace(self._json_attrs, bigsmiles=new_bigsmiles)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def cas(self) -> str:
        return self._json_attrs.cas

    @cas.setter
    def cas(self, new_cas: str):
        new_attrs = replace(self._json_attrs, cas=new_cas)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def chem_formula(self) -> str:
        return self._json_attrs.chem_formula

    @chem_formula.setter
    def chem_formula(self, new_chem_formula: str):
        new_attrs = replace(self._json_attrs, chem_formula=new_chem_formula)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def inchi(self) -> str:
        return self._json_attrs.inchi

    @inchi.setter
    def inchi(self, new_inchi: str):
        new_attrs = replace(self._json_attrs, inchi=new_inchi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def inchi_key(self) -> str:
        return self._json_attrs.inchi_key

    @inchi_key.setter
    def inchi_key(self, new_inchi_key: str):
        new_attrs = replace(self._json_attrs, inchi_key=new_inchi_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def mol_form(self) -> str:
        return self._json_attrs.mol_form

    @mol_form.setter
    def mol_form(self, new_mol_form: str):
        new_attrs = replace(self._json_attrs, mol_form=new_mol_form)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def pubchem_cid(self) -> Union[int, None]:
        return self._json_attrs.pubchem_cid

    @pubchem_cid.setter
    def pubchem_cid(self, new_pubchem_cid: str):
        new_attrs = replace(self._json_attrs, pubchem_cid=new_pubchem_cid)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def smiles(self) -> str:
        return self._json_attrs.smiles

    @smiles.setter
    def smiles(self, new_smiles: str):
        new_attrs = replace(self._json_attrs, smiles=new_smiles)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def component(self) -> List["Material"]:
        """
        list of components ([material nodes](./)) that make up this material

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
            list of components that make up this material
        """
        return self._json_attrs.component.copy()

    @component.setter
    def component(self, new_component_list: List["Material"]) -> None:
        """
        set the list of components (material nodes) that make up this material

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
    def properties(self) -> List[Any]:
        """
        list of material [properties](../../subobjects/property)

        ```python
        # property subobject
        my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

        my_material.properties = my_property
        ```

        Returns
        -------
        List[Property]
            list of properties that define this material
        """
        return self._json_attrs.properties.copy()

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
        List of [process](../process) for this material

        ```python
        # process node
        my_process = cript.Process(name="my process name", type="affinity_pure")

        my_material.process = my_process
        ```

        Returns
        -------
        List[Process]
            list of [Processes](../process) that created this material
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
    def computation_forcefield(self) -> List[Any]:
        """
        list of [computational_forcefield](../../subobjects/computational_forcefield) for this material node

        Returns
        -------
        List[ComputationForcefield]
            list of computational_forcefield that created this material
        """
        return self._json_attrs.computation_forcefield

    @computation_forcefield.setter
    def computation_forcefield(self, new_computation_forcefield_list: List[Any]) -> None:
        """
        sets the list of computation forcefields for this material

        Parameters
        ----------
        new_computation_forcefield_list: List[ComputationalProcess]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation_forcefield=new_computation_forcefield_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keyword(self) -> List[str]:
        """
        List of keywords for this material

        the material keywords must come from the
        [CRIPT controlled vocabulary](https://criptapp.org/keys/material-keyword/)

        ```python
        identifiers = [{"alternative_names": "my material alternative name"}]

        # keywords
        material_keywords = ["acetylene", "acrylate", "alternating"]

        my_material = cript.Material(
            name="my material", keyword=material_keywords, identifiers=identifiers
        )
        ```

        Returns
        -------
        List[str]
            list of material keywords
        """
        return self._json_attrs.keyword.copy()

    @keyword.setter
    def keyword(self, new_keyword_list: List[str]) -> None:
        """
        set the keywords for this material

        the material keywords must come from the CRIPT controlled vocabulary

        Parameters
        ----------
        new_keyword_list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, keyword=new_keyword_list)
        self._update_json_attrs_if_valid(new_attrs)
