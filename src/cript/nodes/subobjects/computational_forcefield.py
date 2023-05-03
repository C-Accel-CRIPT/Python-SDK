from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.data import Data
from cript.nodes.subobjects.citation import Citation


class ComputationalForcefield(BaseNode):
    """
    ComputationForcefield
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        building_block: str = ""
        coarse_grained_mapping: str = ""
        implicit_solvent: str = ""
        source: str = ""
        description: str = ""
        data: List[Data] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, building_block: str, coarse_grained_mapping: str = "", implicit_solvent: str = "", source: str = "", description: str = "", data: List[Data] = None, citation: Union[List[Citation], None] = None, **kwargs):
        if citation is None:
            citation = []
        super().__init__()

        if data is None:
            data = []

        self._json_attrs = replace(
            self._json_attrs,
            key=key,
            building_block=building_block,
            coarse_grained_mapping=coarse_grained_mapping,
            implicit_solvent=implicit_solvent,
            source=source,
            description=description,
            data=data,
            citation=citation,
        )
        self.validate()

    @property
    def key(self) -> str:
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def building_block(self) -> str:
        return self._json_attrs.building_block

    @building_block.setter
    def building_block(self, new_building_block: str):
        new_attrs = replace(self._json_attrs, building_block=new_building_block)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def coarse_grained_mapping(self) -> str:
        return self._json_attrs.coarse_grained_mapping

    @coarse_grained_mapping.setter
    def coarse_grained_mapping(self, new_coarse_grained_mapping: str):
        new_attrs = replace(self._json_attrs, coarse_grained_mapping=new_coarse_grained_mapping)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def implicit_solvent(self) -> str:
        return self._json_attrs.implicit_solvent

    @implicit_solvent.setter
    def implicit_solvent(self, new_implicit_solvent: str):
        new_attrs = replace(self._json_attrs, implicit_solvent=new_implicit_solvent)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def source(self) -> str:
        return self._json_attrs.source

    @source.setter
    def source(self, new_source: str):
        new_attrs = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def description(self) -> str:
        return self._json_attrs.description

    @description.setter
    def description(self, new_description: str):
        new_attrs = replace(self._json_attrs, description=new_description)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> List[Data]:
        return self._json_attrs.data.copy()

    @data.setter
    def data(self, new_data: List[Data]):
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Citation]:
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]):
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
