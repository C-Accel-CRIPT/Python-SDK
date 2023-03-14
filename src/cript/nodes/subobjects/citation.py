from copy import copy
from typing import Union
from dataclasses import dataclass, replace
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.reference import Reference

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

    def __init__(self, type:str, reference:Reference):
        super().__init__(node="Citation")
        self._json_attrs = replace(self._json_attrs, type=type, reference=reference)
        self.validate()

    @property
    def type(self):
        return self._json_attrs.type

    @type.setter
    def type(self, new_type):
        tmp = copy(self)
        tmp._json_attrs.type = replace(tmp._json_attrs, type=new_type)
        tmp.validate()
        self._json_attrs.type = replace(tmp._json_attrs, type=new_type)
        self.validate()

    @property
    def reference(self):
        return self._json_attrs.reference

    @reference.setter
    def reference(self, new_reference):
        tmp = copy(self)
        tmp._json_attrs.reference = replace(self._json_attrs, reference=new_reference)
        tmp.validate()
        self._json_attrs.reference = replace(self._json_attrs, reference=new_reference)
        self.validate()
