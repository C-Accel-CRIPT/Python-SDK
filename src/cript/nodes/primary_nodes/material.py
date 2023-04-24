from dataclasses import dataclass, field, replace
from typing import Any, List

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
    | identifiers             | list[Identifier]                                    |                                                   | material identifiers                         | True        |       |
    | components              | list[[Material](./)]                                |                                                   | list of components that make up the mixture  |             |       |
    | properties              | list[[Property](../subobjects/property)]            |                                                   | material properties                          |             |       |
    | process                 | [Process](../process)                               |                                                   | process node that made this material         |             |       |
    | parent_material         | [Material](./)                                      |                                                   | material node that this node was copied from |             |       |
    | computation_ forcefield | [Computation  Forcefield](../computational_process) |                                                   | computation forcefield                       | Conditional |       |
    | keywords                | list[str]                                           | [thermoplastic, homopolymer, linear, polyolefins] | words that classify the material             |             | True  |

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
        components: List["Material"] = field(default_factory=list)
        properties: List[Any] = field(default_factory=list)
        process: List[Any] = field(default_factory=list)
        parent_materials: List["Material"] = field(default_factory=list)
        computation_forcefield: List[Any] = field(default_factory=list)
        keywords: List[str] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        identifiers: List[dict[str, str]],
        components: List["Material"] = None,
        properties: List[Any] = None,
        process: List[Any] = None,
        parent_materials: List["Material"] = None,
        computation_forcefield: List[Any] = None,
        keywords: List[str] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a material node

        Parameters
        ----------
        name: str
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
            Instantiate a material node
        """

        super().__init__(name=name, notes=notes)

        if components is None:
            components = []

        if properties is None:
            properties = []

        if process is None:
            process = []

        if parent_materials is None:
            parent_materials = []

        if computation_forcefield is None:
            computation_forcefield = []

        if keywords is None:
            keywords = []

        # validate keywords if they exist
        if keywords is not None:
            self._validate_keywords(keywords=keywords)

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
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
        list of components ([material nodes](./)) that make up this material

        Examples
        --------
        ```python
        # material component
        my_components = [
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
        my_material = cript.Material(name="my material", components=my_components, identifiers=identifiers)
        ```

        Returns
        -------
        List[Material]
            list of components that make up this material
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
    def parent_materials(self) -> List["Material"]:
        """
        List of parent materials

        Returns
        -------
        List["Material"]
            list of parent materials
        """
        return self._json_attrs.parent_materials

    @parent_materials.setter
    def parent_materials(self, new_parent_materials_list: List["Material"]) -> None:
        """
        set the [parent materials](./) for this material

        Parameters
        ----------
        new_parent_materials_list: List["Material"]

        Returns
        -------
        None
        """

        new_attrs = replace(self._json_attrs, parent_materials=new_parent_materials_list)
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
    def keywords(self) -> List[str]:
        """
        List of keywords for this material

        the material keywords must come from the
        [CRIPT controlled vocabulary](https://criptapp.org/keys/material-keyword/)

        ```python
        identifiers = [{"alternative_names": "my material alternative name"}]

        # keywords
        material_keywords = ["acetylene", "acrylate", "alternating"]

        my_material = cript.Material(
            name="my material", keywords=material_keywords, identifiers=identifiers
        )
        ```

        Returns
        -------
        List[str]
            list of material keywords
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
