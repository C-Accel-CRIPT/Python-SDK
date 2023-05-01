from dataclasses import dataclass, field, replace
from numbers import Number
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.data import Data
from cript.nodes.primary_nodes.material import Material


class Condition(BaseNode):
    """
    Condition subobject
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        type: str = ""
        descriptor: str = ""
        value: Union[Number, None] = None
        unit: str = ""
        uncertainty: Union[Number, None] = None
        uncertainty_type: str = ""
        material: List[Material] = field(default_factory=list)
        set_id: Union[int, None] = None
        measurement_id: Union[int, None] = None
        data: Union[Data, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        key: str,
        type: str,
        value: Number,
        unit: str = "",
        descriptor: str = "",
        uncertainty: Union[Number, None] = None,
        uncertainty_type: str = "",
        material: Union[List[Material], None] = None,
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: Union[Data, None] = None,
        **kwargs
    ):
        if material is None:
            material = []
        super().__init__()

        self._json_attrs = replace(
            self._json_attrs,
            key=key,
            type=type,
            value=value,
            descriptor=descriptor,
            unit=unit,
            uncertainty=uncertainty,
            uncertainty_type=uncertainty_type,
            material=material,
            set_id=set_id,
            measurement_id=measurement_id,
            data=data,
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
    def descriptor(self) -> str:
        return self._json_attrs.descriptor

    @descriptor.setter
    def descriptor(self, new_descriptor: str):
        new_attrs = replace(self._json_attrs, descriptor=new_descriptor)
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
    def material(self) -> List[Material]:
        return self._json_attrs.material.copy()

    @material.setter
    def material(self, new_material: List[Material]):
        new_attrs = replace(self._json_attrs, material=new_material)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def set_id(self) -> Union[int, None]:
        return self._json_attrs.set_id

    @set_id.setter
    def set_id(self, new_set_id: Union[int, None]):
        new_attrs = replace(self._json_attrs, set_id=new_set_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def measurement_id(self) -> Union[int, None]:
        return self._json_attrs.measurement_id

    @measurement_id.setter
    def measurement_id(self, new_measurement_id: Union[int, None]):
        new_attrs = replace(self._json_attrs, measurement_id=new_measurement_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data(self) -> Union[Data, None]:
        return self._json_attrs.data

    @data.setter
    def data(self, new_data: Data):
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)
