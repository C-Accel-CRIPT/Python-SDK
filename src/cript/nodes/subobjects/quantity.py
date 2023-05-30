from dataclasses import dataclass, replace
from numbers import Number
from typing import Union

from cript.nodes.core import BaseNode


class Quantity(BaseNode):
    """
    ## Definition
    The [Quantity](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=22)
    sub-objects are the amount of material involved in a process

    ---

    ## Can Be Added To:
    * [Ingredient](../ingredient)

    ## Available sub-objects
    * None

    ----

    ## Attributes

    | attribute        | type    | example | description          | required | vocab |
    |------------------|---------|---------|----------------------|----------|-------|
    | key              | str     | mass    | type of quantity     | True     | True  |
    | value            | Any     | 1.23    | amount of material   | True     |       |
    | unit             | str     | gram    | unit for quantity    | True     |       |
    | uncertainty      | Number  | 0.1     | uncertainty of value |          |       |
    | uncertainty_type | str     | std     | type of uncertainty  |          | True  |




    ## JSON Representation
    ```json
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        value: Union[Number, None] = None
        unit: str = ""
        uncertainty: Union[Number, None] = None
        uncertainty_type: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, value: Number, unit: str, uncertainty: Union[Number, None] = None, uncertainty_type: str = "", **kwargs):
        """
        create Quantity sub-object

        Parameters
        ----------
        key : str
            type of quantity. Quantity key must come from [CRIPT Controlled Vocabulary]()
        value : Number
            amount of material
        unit : str
            unit for quantity
        uncertainty : Union[Number, None], optional
            uncertainty of value, by default None
        uncertainty_type : str, optional
            type of uncertainty. Quantity uncertainty type must come from [CRIPT Controlled Vocabulary](), by default ""

        Examples
        --------
        ```python
        import cript

        my_quantity = cript.Quantity(
            key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        )
        ```

        Returns
        -------
        None
            create Quantity sub-object
        """
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit, uncertainty=uncertainty, uncertainty_type=uncertainty_type)
        self.validate()

    def set_key_unit(self, new_key: str, new_unit: str) -> None:
        """
        set the Quantity key and unit attributes

        Quantity key must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_quantity.set_key_unit(new_key="mass", new_unit="gram")
        ```

        Parameters
        ----------
        new_key : str
            new Quantity key. Quantity key must come from [CRIPT Controlled Vocabulary]()
        new_unit : str
            new unit

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def key(self) -> str:
        """
        get the Quantity sub-object key attribute

        Returns
        -------
        str
            this Quantity key attribute
        """
        return self._json_attrs.key

    @property
    def value(self) -> Union[int, float, str]:
        """
        amount of Material

        Examples
        --------
        ```python
        my_quantity.value = 1
        ```

        Returns
        -------
        Union[int, float, str]
            amount of Material
        """
        return self._json_attrs.value

    @value.setter
    def value(self, new_value: Union[int, float, str]) -> None:
        """
        set the amount of Material

        Parameters
        ----------
        new_value : Union[int, float, str]
            amount of Material

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, value=new_value)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def unit(self) -> str:
        """
        get the Quantity unit attribute

        Returns
        -------
        str
            unit for the Quantity value attribute
        """
        return self._json_attrs.unit

    @property
    def uncertainty(self) -> Number:
        """
        get the uncertainty value

        Returns
        -------
        Number
            uncertainty value
        """
        return self._json_attrs.uncertainty

    @property
    def uncertainty_type(self) -> str:
        """
        get the uncertainty type attribute for the Quantity sub-object

        `uncertainty_type` must come from [CRIPT Controlled Vocabulary]()

        Returns
        -------
        str
            uncertainty type
        """
        return self._json_attrs.uncertainty_type

    def set_uncertainty(self, uncertainty: Number, type: str) -> None:
        """
        set the `uncertainty value` and `uncertainty_type`

        Uncertainty and uncertainty type are set at the same time to keep the value and type in sync

        `uncertainty_type` must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_property.set_uncertainty(uncertainty=1, type="stderr")
        ```

        Parameters
        ----------
        uncertainty : Number
            uncertainty value
        type : str
            type of uncertainty, uncertainty_type must come from [CRIPT Controlled Vocabulary]()

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, uncertainty=uncertainty, uncertainty_type=type)
        self._update_json_attrs_if_valid(new_attrs)
