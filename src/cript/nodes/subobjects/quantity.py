from dataclasses import dataclass, replace
from numbers import Number
from typing import Union

from cript.nodes.core import BaseNode


class Quantity(BaseNode):
    """
    Quantity subobject
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        value: Union[Number, None] = None
        unit: str = ""
        uncertainty: Union[str, None] = None
        uncertainty_type: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, value: Number, unit: str, uncertainty: Union[str, None] = None, uncertainty_type: str = "", **kwargs):
        super().__init__()
        self._json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit, uncertainty=uncertainty, uncertainty_type=uncertainty_type)
        self.validate()

    def set_key_unit(self, new_key: str, new_unit: str):
        new_attrs = replace(self._json_attrs, key=new_key, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @property
    def value(self) -> Union[int, float, str]:
        return self._json_attrs.value

    @value.setter
    def value(self, new_value: Union[int, float, str]):
        new_attrs = replace(self._json_attrs, value=new_value)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def unit(self) -> str:
        return self._json_attrs.unit

    @property
    def uncertainty(self):
        return self._json_attrs.uncertainty

    @property
    def uncertainty_type(self):
        return self._json_attrs.uncertainty_type

    # It only makes sense to set uncertainty and uncertainty type at the same time.
    # So no individual setters, just a combination
    def set_uncertainty(self, uncertainty: str, type: str):
        new_attrs = replace(self._json_attrs, uncertainty=uncertainty, uncertainty_type=type)
        self._update_json_attrs_if_valid(new_attrs)
