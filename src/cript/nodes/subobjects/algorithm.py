from typing import List
from dataclasses import dataclass, replace, field
from ..core import BaseNode
from .parameter import Parameter

class Algorithm(BaseNode):
    """
    Algorithm subobject
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node:str = "Algorithm"
        key: str = ""
        type: str = ""

        parameter: List[Parameter] = field(default_factory=list)
        # citation

    _json_attrs: JsonAttributes = JsonAttributes()
    def __init__(self, key:str, type:str, parameter:List[Parameter]):
        super().__init__(node="Algorithm")
        self._json_attrs = replace(self._json_attrs, key=key, type=type, parameter=parameter)


    @property
    def key(self) -> str:
        return self._json_attrs.key
    @key.setter
    def key(self, new_key:str):
        self._json_attrs = replace(self._json_attrs, key=new_key)

    @property
    def type(self) -> str:
        return self._json_attrs.type
    @type.setter
    def type(self, new_type:str):
        self._json_attrs = replace(self._json_attrs, type=new_type)

    @property
    def parameter(self) -> List[Parameter]:
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter:List[Parameter]):
        self._json_attrs(self._json_attrs, parameter=new_parameter)
