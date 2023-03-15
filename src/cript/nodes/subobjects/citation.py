from copy import copy
from typing import Union
from dataclasses import dataclass, replace
from cript.nodes.core import BaseNode
from cript.nodes.subobjects.reference import Reference

class Citation(BaseNode):
    """
    Citation subobject
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Citation"
        type: str = ""
        reference: Union[Reference, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, type:str, reference:Reference, **kwargs):
        super().__init__(node="Citation")
        self._json_attrs = replace(self._json_attrs, type=type, reference=reference)
        self.validate()

    @property
    def type(self):
        return self._json_attrs.type

    @type.setter
    def type(self, new_type):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def reference(self):
        return self._json_attrs.reference

    @reference.setter
    def reference(self, new_reference):
        new_attrs = replace(self._json_attrs, reference=new_reference)
        self._update_json_attrs_if_valid(new_attrs)
