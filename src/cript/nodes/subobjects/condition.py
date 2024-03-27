from dataclasses import dataclass, field, replace
from numbers import Number
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.data import Data
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Condition(UUIDBaseNode):
    """
    ## Definition

    A [Condition](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=21) sub-object
    is the conditions under which the experiment was conducted.
    Some examples include temperature, mixing_rate, stirring, time_duration.

    ----

    ## Can Be Added To:
    ### Primary Nodes
    * [Process](../../primary_nodes/process)
    * [Computation_Process](../../primary_nodes/computation_process)

    ### Subobjects
    * [Property](../property)
    * [Equipment](../equipment)

    ---

    ## Attributes

    | attribute        | type   | example                 | description                                                                            | required | vocab |
    |------------------|--------|-------------------------|----------------------------------------------------------------------------------------|----------|-------|
    | key              | str    | temp                    | type of condition                                                                      | True     | True  |
    | type             | str    | min                     | type of value stored, 'value' is just the number, 'min', 'max', 'avg', etc. for series | True     | True  |
    | descriptor       | str    | upper temperature probe | freeform description for condition                                                     |          |       |
    | value            | Number | 1.23                    | value or quantity                                                                      | True     |       |
    | unit             | str    | gram                    | unit for value                                                                         |          |       |
    | uncertainty      | Number | 0.1                     | uncertainty of value                                                                   |          |       |
    | uncertainty_type | str    | std                     | type of uncertainty                                                                    |          | True  |
    | set_id           | int    | 0                       | ID of set (used to link measurements in as series)                                     |          |       |
    | measurement _id  | int    | 0                       | ID for a single measurement (used to link multiple condition at a single instance)     |          |       |
    | data             | List[Data] |                         | detailed data associated with the condition                                            |          |       |

    ## JSON Representation
    ```json
    {
        "node": ["Condition"],
        "key": "temperature",
        "type": "value",
        "descriptor": "room temperature of lab",
        "value": 22,
        "unit": "C",
        "uncertainty": 5,
        "uncertainty_type": "stdev",
        "set_id": 0,
        "measurement_id": 2,
        "data": [{
            "node":["Data"],
            "name":"my data name",
            "type":"afm_amp",
            "file":[
                {
                    "node":["File"],
                    "type":"calibration",
                    "source":"https://criptapp.org",
                    "extension":".csv",
                    "data_dictionary":"my file's data dictionary"
                }
            ]
        }],
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        type: str = ""
        descriptor: str = ""
        value: Optional[Union[Number, str]] = None
        unit: str = ""
        uncertainty: Optional[Union[Number, str]] = None
        uncertainty_type: str = ""
        set_id: Optional[int] = None
        measurement_id: Optional[int] = None
        data: List[Union[Data, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        key: str,
        type: str,
        value: Union[Number, str],
        unit: str = "",
        descriptor: str = "",
        uncertainty: Optional[Union[Number, str]] = None,
        uncertainty_type: str = "",
        set_id: Optional[int] = None,
        measurement_id: Optional[int] = None,
        data: Optional[List[Union[Data, UIDProxy]]] = None,
        **kwargs
    ):
        """
        create Condition sub-object

        Parameters
        ----------
        key : str
            type of condition
        type : str
            type of value stored
        value : Number
            value or quantity
        unit : str, optional
            unit for value, by default ""
        descriptor : str, optional
            freeform description for condition, by default ""
        uncertainty : Union[Number, None], optional
           uncertainty of value, by default None
        uncertainty_type : str, optional
            type of uncertainty, by default ""
        set_id : Union[int, None], optional
            ID of set (used to link measurements in as series), by default None
        measurement_id : Union[int, None], optional
            ID for a single measurement (used to link multiple condition at a single instance), by default None
        data : List[Data], optional
            detailed data associated with the condition, by default None


        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )

        Returns
        -------
        None
        """
        super().__init__(**kwargs)

        if data is None:
            data = []

        new_json_attrs = replace(
            self._json_attrs,
            key=key,
            type=type,
            value=value,
            descriptor=descriptor,
            unit=unit,
            uncertainty=uncertainty,
            uncertainty_type=uncertainty_type,
            set_id=set_id,
            measurement_id=measurement_id,
            data=data,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def key(self) -> str:
        """
        type of condition

        > Condition key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/condition_key)

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.key = "energy_threshold"

        Returns
        -------
        condition key: str
            type of condition
        """
        return self._json_attrs.key

    @key.setter
    @beartype
    def key(self, new_key: str) -> None:
        """
        set this Condition sub-object key

        Parameters
        ----------
        new_key : str
            type of condition

        Returns
        --------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        description for the value stored for this Condition node

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.type = "min"

        Returns
        -------
        condition type: str
            description for the value
        """
        return self._json_attrs.type

    @type.setter
    @beartype
    def type(self, new_type: str) -> None:
        """
        set the type attribute for this Condition node

        Parameters
        ----------
        new_type : str
            new description of the Condition value

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def descriptor(self) -> str:
        """
        freeform description for Condition

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.descriptor = "my condition description"

        Returns
        -------
        description: str
            description of this Condition sub-object
        """
        return self._json_attrs.descriptor

    @descriptor.setter
    @beartype
    def descriptor(self, new_descriptor: str) -> None:
        """
        set the description of this Condition sub-object

        Parameters
        ----------
        new_descriptor : str
            new description describing the Condition subobject

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, descriptor=new_descriptor)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def value(self) -> Optional[Union[Number, str]]:
        """
        value or quantity

        Returns
        -------
        Union[Number, None]
            new value or quantity
        """
        return self._json_attrs.value

    def set_value(self, new_value: Union[Number, str], new_unit: str) -> None:
        """
        set the value for this Condition subobject

        Parameters
        ----------
        new_value : Number
            new value
        new_unit : str
            units for the new value

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.set_value(new_value=1, new_unit="gram")

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, value=new_value, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def unit(self) -> str:
        """
        set units for this Condition subobject

        Returns
        -------
        unit: str
            units
        """
        return self._json_attrs.unit

    @property
    @beartype
    def uncertainty(self) -> Optional[Union[Number, str]]:
        """
        set uncertainty value for this Condition subobject

        Returns
        -------
        uncertainty: Union[Number, None]
            uncertainty
        """
        return self._json_attrs.uncertainty

    @beartype
    def set_uncertainty(self, new_uncertainty: Union[Number, str, None], new_uncertainty_type: str) -> None:
        """
        set uncertainty and uncertainty type

        Parameters
        ----------
        new_uncertainty : Number
            new uncertainty value
        new_uncertainty_type : str
            new uncertainty type

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.set_uncertainty(new_uncertainty=0.2, new_uncertainty_type="stdev")

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, uncertainty=new_uncertainty, uncertainty_type=new_uncertainty_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def uncertainty_type(self) -> str:
        """
        Uncertainty type for the uncertainty value

        [Uncertainty type](https://app.criptapp.org/vocab/uncertainty_type) must come from CRIPT controlled vocabulary

        Returns
        -------
        uncertainty_type: str
            uncertainty type
        """
        return self._json_attrs.uncertainty_type

    @property
    @beartype
    def set_id(self) -> Union[int, None]:
        """
        ID of set (used to link measurements in as series)

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.set_id = 0

        Returns
        -------
        set_id: Union[int, None]
            ID of set
        """
        return self._json_attrs.set_id

    @set_id.setter
    @beartype
    def set_id(self, new_set_id: Union[int, None]) -> None:
        """
         set this Condition subobjects set_id

        Parameters
        ----------
        new_set_id : Union[int, None]
            ID of set

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, set_id=new_set_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def measurement_id(self) -> Union[int, None]:
        """
        ID for a single measurement (used to link multiple condition at a single instance)

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.measurement_id = 0

        Returns
        -------
        measurement_id: Union[int, None]
            ID for a single measurement
        """
        return self._json_attrs.measurement_id

    @measurement_id.setter
    @beartype
    def measurement_id(self, new_measurement_id: Union[int, None]) -> None:
        """
        set the set_id for this Condition subobject

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_condition.measurement_id = 1

        Parameters
        ----------
        new_measurement_id : Union[int, None]
            ID for a single measurement

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, measurement_id=new_measurement_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def data(self) -> List[Union[Data, UIDProxy]]:
        """
        detailed data associated with the condition

        Examples
        --------
        >>> import cript
        >>> my_condition = cript.Condition(
        ...     key="temperature",
        ...     type="value",
        ...     value=22,
        ...     unit="C",
        ... )
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
        ...     type="calibration",
        ...     extension=".pdf",
        ... )
        >>> my_data = cript.Data(
        ...     name="my data node name",
        ...     type="afm_amp",
        ...     file=[my_file],
        ... )
        >>> my_condition.data = [my_data]

        Returns
        -------
        Condition: Union[Data, None]
            detailed data associated with the condition
        """
        return self._json_attrs.data.copy()

    @data.setter
    @beartype
    def data(self, new_data: List[Union[Data, UIDProxy]]) -> None:
        """
        set the data node for this Condition Subobject

        Parameters
        ----------
        new_data : List[Data]
            new Data node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)
