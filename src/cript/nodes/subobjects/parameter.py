from dataclasses import dataclass, replace
from numbers import Number
from typing import Optional, Union

from beartype import beartype

from cript.nodes.uuid_base import UUIDBaseNode


class Parameter(UUIDBaseNode):
    """
    ## Definition

    A [parameter](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=25)
    is an input value to an algorithm.

    ??? note "Difference between `Parameter` and `Condition`"
        For typical computations, the difference between
        parameter and condition lies in whether it changes the thermodynamic state of the simulated
        system: Variables that are part of defining a thermodynamic state should be defined as a condition
        in a parent node.

        Therefore, `number` and `volume` need to be listed as conditions while
        `boundaries` and `origin` are parameters of ensemble size

    ---
    ## Can Be Added To:
    * [Algorithm sub-object](../algorithm)

    ## Available sub-objects:
    * None

    ---

    ## Attributes

    | attribute | type | example | description        | required | vocab |
    |-----------|------|---------|--------------------|----------|-------|
    | key       | str  |         | key for identifier | True     | True  |
    | value     | Any  |         | value              | True     |       |
    | unit      | str  |         | unit for parameter |          |       |


    ## JSON Representation
    ```json
    {
       "key":"update_frequency",
       "node":["Parameter"],
       "unit":"1/second",
       "value":1000.0
       "uid":"_:6af3b3aa-1dbc-4ce7-be8b-1896b375001c",
       "uuid":"6af3b3aa-1dbc-4ce7-be8b-1896b375001c",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        value: Optional[Number] = None
        # We explicitly allow None for unit here (instead of empty str),
        # this presents number without physical unit, like counting
        # particles or dimensionless numbers.
        unit: Union[str, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    # Note that the key word args are ignored.
    # They are just here, such that we can feed more kwargs in that we get from the back end.
    @beartype
    def __init__(self, key: str, value: Number, unit: Optional[str] = None, **kwargs):
        """
        create new Parameter sub-object

        Parameters
        ----------
        key : str
            Parameter key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/parameter_key)
        value : Union[int, float]
            Parameter value
        unit : Union[str, None], optional
            Parameter unit, by default None

        Examples
        --------
        >>> import cript
        >>> my_parameter = cript.Parameter("update_frequency", 1000.0, "1/second")

        Returns
        -------
        None
            create Parameter sub-object
        """
        super().__init__(**kwargs)
        new_json_attrs = replace(self._json_attrs, key=key, value=value, unit=unit)
        self._update_json_attrs_if_valid(new_json_attrs)

    @classmethod
    def _from_json(cls, json_dict: dict):
        # TODO: remove this temporary fix, once back end is working correctly
        try:
            json_dict["value"] = float(json_dict["value"])
        except KeyError:
            pass
        return super(Parameter, cls)._from_json(json_dict)

    @property
    @beartype
    def key(self) -> str:
        """
        Parameter key must come from the [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/parameter_key)

        Examples
        --------
        >>> import cript
        >>> my_parameter = cript.Parameter("update_frequency", 1000.0, "1/second")
        >>> my_parameter.key = "damping_time"

        Returns
        -------
        str
            parameter key
        """
        return self._json_attrs.key

    @key.setter
    @beartype
    def key(self, new_key: str) -> None:
        """
        set new key for the Parameter sub-object

        Parameters
        ----------
        new_key : str
            new Parameter key

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def value(self) -> Optional[Number]:
        """
        Parameter value

        Examples
        --------
        >>> import cript
        >>> my_parameter = cript.Parameter("update_frequency", 1000.0, "1/second")
        >>> my_parameter.value = 1

        Returns
        -------
        Union[int, float, str]
            parameter value
        """
        return self._json_attrs.value

    @value.setter
    @beartype
    def value(self, new_value: Number) -> None:
        """
        set the Parameter value

        Parameters
        ----------
        new_value : Union[int, float, str]
            new parameter value

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, value=new_value)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def unit(self) -> Union[str, None]:
        """
        Parameter unit

        Examples
        --------
        >>> import cript
        >>> my_parameter = cript.Parameter("update_frequency", 1000.0, "1/second")
        >>> my_parameter.unit = "gram"

        Returns
        -------
        str
            parameter unit
        """
        return self._json_attrs.unit

    @unit.setter
    @beartype
    def unit(self, new_unit: str) -> None:
        """
        set the unit attribute for the Parameter sub-object

        Parameters
        ----------
        new_unit : str
            new Parameter unit

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)
