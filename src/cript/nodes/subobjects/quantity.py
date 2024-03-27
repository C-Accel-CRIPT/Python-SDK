from dataclasses import dataclass, replace
from numbers import Number
from typing import Optional, Union

from beartype import beartype

from cript.nodes.uuid_base import UUIDBaseNode


class Quantity(UUIDBaseNode):
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
    {
     "node":["Quantity"],
     "key":"mass",
     "value":11.2
     "uncertainty":0.2,
     "uncertainty_type":"stdev",
     "unit":"kg",
     "uid":"_:c95ee781-923b-4699-ba3b-923ce186ac5d",
     "uuid":"c95ee781-923b-4699-ba3b-923ce186ac5d",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        value: Union[Number, str, None] = None
        unit: str = ""
        uncertainty: Optional[Number] = None
        uncertainty_type: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, key: str, value: Number, unit: str, uncertainty: Optional[Number] = None, uncertainty_type: str = "", **kwargs):
        """
        create Quantity sub-object

        Parameters
        ----------
        key : str
            type of quantity. Quantity key must come from
            [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/quantity_key)
        value : Number
            amount of material
        unit : str
            unit for quantity
        uncertainty : Union[Number, None], optional
            uncertainty of value, by default None
        uncertainty_type : str, optional
            type of uncertainty. Quantity uncertainty type must come from
            [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/uncertainty_type), by default ""

        Examples
        --------
        >>> import cript
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )

        Returns
        -------
        None
            create Quantity sub-object
        """
        super().__init__(**kwargs)
        new_json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit, uncertainty=uncertainty, uncertainty_type=uncertainty_type)
        self._update_json_attrs_if_valid(new_json_attrs)

    @classmethod
    def _from_json(cls, json_dict: dict):
        # TODO: remove this temporary fix, once back end is working correctly
        for key in ["value", "uncertainty"]:
            try:
                json_dict[key] = float(json_dict[key])
            except KeyError:
                pass
        return super(Quantity, cls)._from_json(json_dict)

    @beartype
    def set_key_unit(self, new_key: str, new_unit: str) -> None:
        """
        set the Quantity key and unit attributes

        Quantity key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/quantity_key)

        Examples
        --------
        >>> import cript
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_quantity.set_key_unit(new_key="mass", new_unit="kg")

        Parameters
        ----------
        new_key : str
            new Quantity key. Quantity key must come from
            [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/quantity_key)
        new_unit : str
            new unit

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def key(self) -> str:
        """
        get the Quantity sub-object key attribute

        [Quantity type](https://app.criptapp.org/vocab/quantity_key) must come from CRIPT controlled vocabulary

        Returns
        -------
        str
            this Quantity key attribute
        """
        return self._json_attrs.key

    @property
    @beartype
    def value(self) -> Union[int, float, str]:
        """
        amount of Material

        Examples
        --------
        >>> import cript
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_quantity.value = 1

        Returns
        -------
        Union[int, float, str]
            amount of Material
        """
        return self._json_attrs.value  # type: ignore

    @value.setter
    @beartype
    def value(self, new_value: Union[Number, str, None]) -> None:
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
    @beartype
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
    @beartype
    def uncertainty(self) -> Optional[Number]:
        """
        get the uncertainty value

        Returns
        -------
        Number
            uncertainty value
        """
        return self._json_attrs.uncertainty  # type: ignore

    @property
    @beartype
    def uncertainty_type(self) -> str:
        """
        get the uncertainty type attribute for the Quantity sub-object

        [Uncertainty type](https://app.criptapp.org/vocab/uncertainty_type) must come from CRIPT controlled vocabulary

        Returns
        -------
        str
            uncertainty type
        """
        return self._json_attrs.uncertainty_type

    @beartype
    def set_uncertainty(self, uncertainty: Optional[Number], type: str) -> None:
        """
        set the `uncertainty value` and `uncertainty_type`

        Uncertainty and uncertainty type are set at the same time to keep the value and type in sync

        `uncertainty_type` must come from
        [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/uncertainty_type)

        Examples
        --------
        >>> import cript
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )

        Parameters
        ----------
        uncertainty : Number
            uncertainty value
        type : str
            type of uncertainty, uncertainty_type must come from
            [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/uncertainty_type)

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, uncertainty=uncertainty, uncertainty_type=type)
        self._update_json_attrs_if_valid(new_attrs)
