from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Inventory(PrimaryBaseNode):
    """
    Inventory Node
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Inventory attributes
        """

        node: str = "Inventory"
        materials: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, materials_list: List[Material], **kwargs) -> None:
        """
        create an inventory node

        Parameters
        ----------
        materials_list: List[Material]
            list of materials in this inventory

        Returns
        -------
        None
        """

        if materials_list is None:
            materials_list = []

        super().__init__(node="Inventory")
        self._json_attrs = replace(self._json_attrs, materials=materials_list)

    # ------------------ Properties ------------------
    @property
    def materials(self) -> List[Material]:
        """
        get the list of materials in this inventory

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
