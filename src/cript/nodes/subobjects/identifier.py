from typing import Union,  List
from numbers import Number
from dataclasses import dataclass, replace
from cript.nodes.core import BaseNode

class Identifier(BaseNode):
    """
    Identifier subobject
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Identifier"
        key: str = ""
        value: Union[str, Number, List[str], List[Number]] = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key:str, value: Union[str, Number, List[str], List[Number]], **kwargs):
        super().__init__(node="Identifier")
        self._json_attrs = replace(self._json_attrs, key=key, value=value)
        self.validate()

    @property
    def key(self):
        return self._json_attrs.key

    @key.setter
    def key(self, new_key):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def value(self):
        try: # Handle list values
            return self._json_attrs.value.copy()
        except AttributeError: # Non lists
            return self._json_attrs.value

    @value.setter
    def value(self, new_value):
        new_attrs = replace(self._json_attrs, value=new_value)
        self._update_json_attrs_if_valid(new_attrs)
