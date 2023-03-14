from typing import Union
from dataclasses import dataclass, replace
from ..core import BaseNode


class Parameter(BaseNode):
    """Parameter    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Parameter"
        key: str = ""
        value: Union[int, float, str] = ""
        unit: Union[str, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self, key: str, value: Union[int, float], unit: Union[str, None] = None
    ):
        super().__init__(node="Parameter")
        self._json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit)

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        self._json_attrs = replace(self._json_attrs, key=new_key)

    @property
    def value(self) -> Union[int, float, str]:
        return self._json_attrs.value

    @value.setter
    def value(self, new_value: Union[int, float, str]):
        self._json_attrs = replace(self._json_attrs, value=new_value)

    @property
    def unit(self) -> str:
        return self._json_attrs.unit

    @unit.setter
    def unit(self, new_unit: str):
        self._json_attrs = replace(self._json_attrs, unit=new_unit)
