from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.parameter import Parameter


class Algorithm(BaseNode):
    """ """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        type: str = ""

        parameter: List[Parameter] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, type: str, parameter: List[Parameter] = None, citation: List[Citation] = None, **kwargs):  # ignored
        if parameter is None:
            parameter = []
        if citation is None:
            citation = []
        super().__init__(node="Algorithm")
        self._json_attrs = replace(self._json_attrs, key=key, type=type, parameter=parameter)
        self.validate()

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def type(self) -> str:
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def parameter(self) -> List[Parameter]:
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter: List[Parameter]):
        new_attrs = replace(self._json_attrs, parameter=new_parameter)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self):
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation):
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
