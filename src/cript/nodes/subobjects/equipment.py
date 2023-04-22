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
        node: str = "Equipment"
        key: str = ""
        description: str = ""
        conditions: List[Condition] = field(default_factory=list)
        files: List[File] = field(default_factory=list)
        citations: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, description: str = "", conditions: Union[List[Condition], None] = None, files: Union[List[File], None] = None, citations: Union[List[Citation], None] = None, **kwargs):
        if conditions is None:
            conditions = []
        if files is None:
            files = []
        if citations is None:
            citations = []
        super().__init__("Equipment")
        self._json_attrs = replace(self._json_attrs, key=key, description=description, conditions=conditions, files=files, citations=citations)
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
    def conditions(self) -> List[Condition]:
        return self._json_attrs.conditions.copy()

    @conditions.setter
    def conditions(self, new_conditions):
        new_attrs = replace(self._json_attrs, conditions=new_conditions)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def files(self) -> List[File]:
        return self._json_attrs.files.copy()

    @files.setter
    def files(self, new_files: List[File]):
        new_attrs = replace(self._json_attrs, files=new_files)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Citation]:
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations: List[Citation]):
        new_attrs = replace(self._json_attrs, citations=new_citations)
        self._update_json_attrs_if_valid(new_attrs)
