from dataclasses import dataclass, field, replace
from numbers import Number
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.computation import Computation
from cript.nodes.primary_nodes.data import Data
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.process import Process
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.condition import Condition


class Property(BaseNode):
    """
    Property Node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        type: str = ""
        value: Union[Number, None] = None
        unit: str = ""
        uncertainty: Union[Number, None] = None
        uncertainty_type: str = ""
        components: List[Material] = field(default_factory=list)
        components_relative: List[Material] = field(default_factory=list)
        structure: str = ""
        method: str = ""
        sample_preparation: Union[Process, None] = None
        conditions: List[Condition] = field(default_factory=list)
        data: Union[Data, None] = None
        computations: List[Computation] = field(default_factory=list)
        citations: List[Citation] = field(default_factory=list)
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        key: str,
        type: str,
        value: Union[Number, None],
        unit: str,
        uncertainty: Union[Number, None] = None,
        uncertainty_type: str = "",
        components: Union[List[Material], None] = None,
        components_relative: Union[List[Material], None] = None,
        structure: str = "",
        method: str = "",
        sample_preparation: Union[Process, None] = None,
        conditions: Union[List[Condition], None] = None,
        data: Union[Data, None] = None,
        computations: Union[List[Computation], None] = None,
        citations: Union[List[Citation], None] = None,
        notes: str = "",
        **kwargs
    ):
        if components is None:
            components = []
        if components_relative is None:
            components_relative = []
        if conditions is None:
            conditions = []
        if computations is None:
            computations = []
        if citations is None:
            citations = []

        super().__init__()
        self._json_attrs = replace(
            self._json_attrs,
            key=key,
            type=type,
            value=value,
            unit=unit,
            uncertainty=uncertainty,
            uncertainty_type=uncertainty_type,
            components=components,
            components_relative=components_relative,
            structure=structure,
            method=method,
            sample_preparation=sample_preparation,
            conditions=conditions,
            data=data,
            computations=computations,
            citations=citations,
            notes=notes,
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
    def type(self) -> str:
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def value(self) -> Union[Number, None]:
        return self._json_attrs.value

    def set_value(self, new_value: Number, new_unit: str):
        new_attrs = replace(self._json_attrs, value=new_value, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def unit(self) -> str:
        return self._json_attrs.unit

    @property
    def uncertainty(self) -> Union[Number, None]:
        return self._json_attrs.uncertainty

    def set_uncertainty(self, new_uncertainty: Number, new_uncertainty_type: str):
        new_attrs = replace(self._json_attrs, uncertainty=new_uncertainty, uncertainty_type=new_uncertainty_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def uncertainty_type(self) -> str:
        return self._json_attrs.uncertainty_type

    @property
    def components(self) -> List[Material]:
        return self._json_attrs.components.copy()

    @components.setter
    def components(self, new_components: List[Material]):
        new_attrs = replace(self._json_attrs, components=new_components)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def components_relative(self) -> List[Material]:
        return self._json_attrs.components_relative.copy()

    @components_relative.setter
    def components_relative(self, new_components_relative: List[Material]):
        new_attrs = replace(self._json_attrs, components_relative=new_components_relative)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def structure(self) -> str:
        return self._json_attrs.structure

    @structure.setter
    def structure(self, new_structure: str):
        new_attrs = replace(self._json_attrs, structure=new_structure)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def method(self) -> str:
        return self._json_attrs.method

    @method.setter
    def method(self, new_method: str):
        new_attrs = replace(self._json_attrs, method=new_method)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def sample_preparation(self) -> Union[Process, None]:
        return self._json_attrs.sample_preparation

    @sample_preparation.setter
    def sample_preparation(self, new_sample_preparation: Union[Process, None]):
        new_attrs = replace(self._json_attrs, sample_preparation=new_sample_preparation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def conditions(self) -> List[Condition]:
        return self._json_attrs.conditions.copy()

    @conditions.setter
    def conditions(self, new_conditions: List[Condition]):
        new_attrs = replace(self._json_attrs, conditions=new_conditions)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> Union[Data, None]:
        return self._json_attrs.data

    @data.setter
    def data(self, new_data: Union[Data, None]):
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computations(self) -> List[Computation]:
        return self._json_attrs.computations.copy()

    @computations.setter
    def computations(self, new_computations: List[Computation]):
        new_attrs = replace(self._json_attrs, computations=new_computations)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Citation]:
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations: List[Citation]):
        new_attrs = replace(self._json_attrs, citations=new_citations)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def notes(self) -> str:
        return self._json_attrs.notes

    @notes.setter
    def notes(self, new_notes: str):
        new_attrs = replace(self._json_attrs, notes=new_notes)
        self._update_json_attrs_if_valid(new_attrs)
