from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Inventory(PrimaryBaseNode):
    """
    ## Definition
    An
    [Inventory Node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=9)
    is a list of material nodes.
    An example of an inventory can be a grouping of materials that were extracted from literature
    and curated into a group for machine learning, or it can be a subset of chemicals that are used for a
    certain type of synthesis.

    ## Attributes

    | Attribute  | Type                            | Example             | Description                               |
    |------------|---------------------------------|---------------------|-------------------------------------------|
    | materials  | list[[Material](./material.md)] |                     | materials that you like to group together |



    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Inventory attributes
        """
        materials: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, materials_list: List[Material], notes: str = "", **kwargs) -> None:
        """
        Instantiate an inventory node

        Examples
        --------
        ```python
        material_1 = cript.Material(
            name="material 1",
            identifiers=[{"alternative_names": "material 1 alternative name"}],
        )

        material_2 = cript.Material(
            name="material 2",
            identifiers=[{"alternative_names": "material 2 alternative name"}],
        )

        # instantiate inventory node
        my_inventory = cript.Inventory(
            name="my inventory name", materials_list=[material_1, material_2]
        )
        ```

        Parameters
        ----------
        materials_list: List[Material]
            list of materials in this inventory

        Returns
        -------
        None
            instantiate an inventory node
        """

        if materials_list is None:
            materials_list = []

        super().__init__(name=name, notes=notes)

        self._json_attrs = replace(self._json_attrs, materials=materials_list)

    # ------------------ Properties ------------------
    @property
    def materials(self) -> List[Material]:
        """
        List of [materials](../material) in this inventory

        Examples
        --------
        ```python
        material_3 = cript.Material(
            name="new material 3",
            identifiers=[{"alternative_names": "new material 3 alternative name"}],
        )

        my_inventory.materials = [my_material_3]
        ```

        Returns
        -------
        List[Material]
            list of materials representing the inventory within the collection
        """
        return self._json_attrs.materials.copy()

    @materials.setter
    def materials(self, new_material_list: List[Material]):
        """
        set the list of materials for this inventory node

        Parameters
        ----------
        new_material_list: List[Material]
            new list of materials to replace the current list of material nodes for this inventory node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, materials=new_material_list)
        self._update_json_attrs_if_valid(new_attrs)
