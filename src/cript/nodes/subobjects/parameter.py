from dataclasses import dataclass, replace
from typing import Union

from cript.nodes.core import BaseNode
from cript.nodes.exceptions import CRIPTNodeSchemaError


class Parameter(BaseNode):
    """Parameter"""

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Parameter"
        key: str = ""
        value: Union[int, float, str] = ""
        # We explictly allow None for unit here (instead of empty str),
        # this presents number without physical unit, like counting
        # particles or dimensionless numbers.
        unit: Union[str, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    # Note that the key word args are ignored.
    # They are just here, such that we can feed more kwargs in that we get from the back end.
    def __init__(self, key: str, value: Union[int, float], unit: Union[str, None] = None, **kwargs):
        super().__init__(node="Parameter")
        self._json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit)
        self.validate()

    def validate(self):
        super().validate()
        # TODO. Remove this dummy validation of parameter
        if not (isinstance(self._json_attrs.value, float) or isinstance(self._json_attrs.value, int) or isinstance(self._json_attrs.value, str)):
            raise CRIPTNodeSchemaError

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

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

    @unit.setter
    def unit(self, new_unit: str):
        new_attrs = replace(self._json_attrs, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)
