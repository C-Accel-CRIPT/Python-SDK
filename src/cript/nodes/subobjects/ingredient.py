from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.material import Material
from cript.nodes.subobjects.quantity import Quantity


class Ingredient(BaseNode):
    """
    Ingredient subobject
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        material: Union[Material, None] = None
        quantity: List[Quantity] = field(default_factory=list)
        keyword: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, material: Material, quantity: List[Quantity], keyword: str = "", **kwargs):
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, material=material, quantity=quantity, keyword=keyword)
        self.validate()

    @property
    def material(self) -> Material:
        return self._json_attrs.material

    @property
    def quantity(self) -> List[Quantity]:
        return self._json_attrs.quantity.copy()

    def set_material(self, new_material: Material, new_quantity: List[Quantity]):
        new_attrs = replace(self._json_attrs, material=new_material, quantity=new_quantity)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def keyword(self) -> str:
        return self._json_attrs.keyword

    @keyword.setter
    def keyword(self, new_keyword: str):
        new_attrs = replace(self._json_attrs, keyword=new_keyword)
        self._update_json_attrs_if_valid(new_attrs)
