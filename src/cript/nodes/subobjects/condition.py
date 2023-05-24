from dataclasses import dataclass, replace
from numbers import Number
from typing import Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.data import Data


class Condition(BaseNode):
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

    ### Subojects
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
    | data             | Data   |                         | detailed data associated with the condition                                            |          |       |

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
        "data": {
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
        },
    }
    ```
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
        set_id: Union[int, None] = None,
        measurement_id: Union[int, None] = None,
        data: Union[Data, None] = None,
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
        data : Union[Data, None], optional
            detailed data associated with the condition, by default None


        Examples
        --------
        ```python
        # instantiate a Condition sub-object
        my_condition = cript.Condition(
            key="temperature",
            type="value",
            value=22,
            unit="C",
        )
        ```

        Returns
        -------
        None
        """
        super().__init__(**kwargs)

        self._json_attrs = replace(
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
        self.validate()

    @property
    def key(self) -> str:
        """
        type of condition

        > Condition key must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_condition.key = "energy_threshold"
        ```

        Returns
        -------
        condition key: str
            type of condition
        """
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str) -> None:
        """
        set this Condition sub-object key

        > Condition key must come from [CRIPT Controlled Vocabulary]()

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
    def type(self) -> str:
        """
        description for the value stored for this Condition node

        Examples
        --------
        ```python
        my_condition.type = "min"
        ```

        Returns
        -------
        condition type: str
            description for the value
        """
        return self._json_attrs.type

    @type.setter
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
    def descriptor(self) -> str:
        """
        freeform description for Condition

        Examples
        --------
        ```python
        my_condition.description = "my condition description"
        ```

        Returns
        -------
        description: str
            description of this Condition sub-object
        """
        return self._json_attrs.descriptor

    @descriptor.setter
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
    def value(self) -> Union[Number, None]:
        """
        value or quantity

        Examples
        -------
        ```python
        my_condition.value = 10
        ```

        Returns
        -------
        Union[Number, None]
            new value or quantity
        """
        return self._json_attrs.value

    def set_value(self, new_value: Number, new_unit: str) -> None:
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
        ```python
        my_condition.set_value(new_value=1, new_unit="gram")
        ```

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, value=new_value, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def unit(self) -> str:
        """
        set units for this Condition subobject

        Examples
        --------
        ```python
        my_condition.unit = "gram"
        ```

        Returns
        -------
        unit: str
            units
        """
        return self._json_attrs.unit

    @property
    def uncertainty(self) -> Union[Number, None]:
        """
        set uncertainty value for this Condition subobject

        Examples
        --------
        ```python
        my_condition.uncertainty = "0.1"
        ```

        Returns
        -------
        uncertainty: Union[Number, None]
            uncertainty
        """
        return self._json_attrs.uncertainty

    def set_uncertainty(self, new_uncertainty: Number, new_uncertainty_type: str) -> None:
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
        ```python
        my_condition.set_uncertainty(new_uncertainty="0.2", new_uncertainty_type="std")
        ```

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, uncertainty=new_uncertainty, uncertainty_type=new_uncertainty_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def uncertainty_type(self) -> str:
        """
        Uncertainty type for the uncertainty value

        Examples
        --------
        ```python
        my_condition.uncertainty_type = "std"
        ```

        Returns
        -------
        uncertainty_type: str
            uncertainty type
        """
        return self._json_attrs.uncertainty_type

    @property
    def set_id(self) -> Union[int, None]:
        """
        ID of set (used to link measurements in as series)

        Examples
        --------
        ```python
        my_condition.set_id = 0
        ```

        Returns
        -------
        set_id: Union[int, None]
            ID of set
        """
        return self._json_attrs.set_id

    @set_id.setter
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
    def measurement_id(self) -> Union[int, None]:
        """
        ID for a single measurement (used to link multiple condition at a single instance)

        Examples
        --------
        ```python
        my_condition.measurement_id = 0
        ```

        Returns
        -------
        measurement_id: Union[int, None]
            ID for a single measurement
        """
        return self._json_attrs.measurement_id

    @measurement_id.setter
    def measurement_id(self, new_measurement_id: Union[int, None]) -> None:
        """
        set the set_id for this Condition subobject

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
    def data(self) -> Union[Data, None]:
        """
        detailed data associated with the condition

        Examples
        --------
        ```python
        # create file nodes for the data node
        my_file = cript.File(
            source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
            type="calibration",
            extension=".pdf",
        )

        # create data node and add the file node to it
        my_data = cript.Data(
            name="my data node name",
            type="afm_amp",
            file=my_file,
        )

        # add data node to Condition subobject
        my_condition.data = my_data
        ```

        Returns
        -------
        Condition: Union[Data, None]
            detailed data associated with the condition
        """
        return self._json_attrs.data

    @data.setter
    def data(self, new_data: Data) -> None:
        """
        set the data node for this Condition Subobject

        Parameters
        ----------
        new_data : Data
            new Data node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)
