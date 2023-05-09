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
        component: List[Material] = field(default_factory=list)
        component_relative: List[Material] = field(default_factory=list)
        structure: str = ""
        method: str = ""
        sample_preparation: Union[Process, None] = None
        condition: List[Condition] = field(default_factory=list)
        data: Union[Data, None] = None
        computation: List[Computation] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)
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
        component: Union[List[Material], None] = None,
        component_relative: Union[List[Material], None] = None,
        structure: str = "",
        method: str = "",
        sample_preparation: Union[Process, None] = None,
        condition: Union[List[Condition], None] = None,
        data: Union[Data, None] = None,
        computation: Union[List[Computation], None] = None,
        citation: Union[List[Citation], None] = None,
        notes: str = "",
        **kwargs
    ):
        if component is None:
            component = []
        if component_relative is None:
            component_relative = []
        if condition is None:
            condition = []
        if computation is None:
            computation = []
        if citation is None:
            citation = []

        super().__init__(**kwargs)
        self._json_attrs = replace(
            self._json_attrs,
            key=key,
            type=type,
            value=value,
            unit=unit,
            uncertainty=uncertainty,
            uncertainty_type=uncertainty_type,
            component=component,
            component_relative=component_relative,
            structure=structure,
            method=method,
            sample_preparation=sample_preparation,
            condition=condition,
            data=data,
            computation=computation,
            citation=citation,
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
    def component(self) -> List[Material]:
        return self._json_attrs.component.copy()

    @component.setter
    def component(self, new_component: List[Material]):
        new_attrs = replace(self._json_attrs, component=new_component)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def component_relative(self) -> List[Material]:
        return self._json_attrs.component_relative.copy()

    @component_relative.setter
    def component_relative(self, new_component_relative: List[Material]):
        new_attrs = replace(self._json_attrs, component_relative=new_component_relative)
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
    def condition(self) -> List[Condition]:
        return self._json_attrs.condition.copy()

    @condition.setter
    def condition(self, new_condition: List[Condition]):
        new_attrs = replace(self._json_attrs, condition=new_condition)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> Union[Data, None]:
        return self._json_attrs.data

    @data.setter
    def data(self, new_data: Union[Data, None]):
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def computation(self) -> List[Computation]:
        return self._json_attrs.computation.copy()

    @computation.setter
    def computation(self, new_computation: List[Computation]):
        new_attrs = replace(self._json_attrs, computation=new_computation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> List[Citation]:
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: List[Citation]):
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def notes(self) -> str:
        return self._json_attrs.notes

    @notes.setter
    def notes(self, new_notes: str):
        new_attrs = replace(self._json_attrs, notes=new_notes)
        self._update_json_attrs_if_valid(new_attrs)
