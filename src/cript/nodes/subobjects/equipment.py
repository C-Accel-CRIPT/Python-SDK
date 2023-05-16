from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.condition import Condition
from cript.nodes.supporting_nodes.file import File


class Equipment(BaseNode):
    """
    Equipment node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        description: str = ""
        condition: List[Condition] = field(default_factory=list)
        file: List[File] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, description: str = "", condition: Union[List[Condition], None] = None, file: Union[List[File], None] = None, citation: Union[List[Citation], None] = None, **kwargs):
        if condition is None:
            condition = []
        if file is None:
            file = []
        if citation is None:
            citation = []
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, key=key, description=description, condition=condition, file=file, citation=citation)
        self.validate()

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def description(self) -> str:
        return self._json_attrs.description

    @description.setter
    def description(self, new_description: str):
        new_attrs = replace(self._json_attrs, description=new_description)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def condition(self) -> List[Condition]:
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition):
        new_attrs = replace(self._json_attrs, condition=new_condition)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def file(self) -> List[File]:
        return self._json_attrs.file.copy()

    @file.setter
    def file(self, new_file: List[File]):
        new_attrs = replace(self._json_attrs, file=new_file)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Citation]:
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]):
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
