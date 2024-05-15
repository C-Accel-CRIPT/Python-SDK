from dataclasses import dataclass, field, replace
from numbers import Number
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.computation import Computation
from cript.nodes.primary_nodes.data import Data
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.process import Process
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.condition import Condition
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Property(UUIDBaseNode):
    """
    ## Definition
    [Property](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=18)
    sub-objects are qualities/traits of a [material](../../primary_nodes/material) or
    [Process](../../primary_nodes/process)

    ---

    ## Can Be Added To:
    * [Material](../../primary_nodes/material)
    * [Process](../../primary_nodes/process)
    * [Computation_Process](../../primary_nodes/computation_process)

    ## Available sub-objects:
    * [Condition](../condition)
    * [Citation](../citation)

    ---

    ## Attributes

    | attribute          | type              | example                                 | description                                                                  | required | vocab |
    |--------------------|-------------------|-----------------------------------------|------------------------------------------------------------------------------|----------|-------|
    | key                | str               | enthalpy                                | type of property                                                             | True     | True  |
    | type               | str               | min                                     | type of value stored                                                         | True     | True  |
    | value              | Any               | 1.23                                    | value or quantity                                                            | True     |       |
    | unit               | str               | gram                                    | unit for value                                                               | True     |       |
    | uncertainty        | Number            | 0.1                                     | uncertainty of value                                                         |          |       |
    | uncertainty_type   | str               | standard_deviation                      | type of uncertainty                                                          |          | True  |
    | component          | list[Material]    |                                         | material that the property relates to**                                      |          |       |
    | structure          | str               | {\\[\\]\\[$\\]\\[C:1\\]\\[C:1\\]\\[$\\] | specific chemical structure associate with the property with atom mappings** |          |       |
    | method             | str               | sec                                     | approach or source of property data                                          |          | True  |
    | sample_preparation | Process           |                                         | sample preparation                                                           |          |       |
    | condition          | list[Condition]   |                                         | conditions under which the property was measured                             |          |       |
    | data               | Data              |                                         | data node                                                                    |          |       |
    | computation        | list[Computation] |                                         | computation method that produced property                                    |          |       |
    | citation           | list[Citation]    |                                         | reference to a book, paper, or scholarly work                                |          |       |
    | notes              | str               |                                         | miscellaneous information, or custom data structure (e.g.; JSON)             |          |       |


    ## JSON Representation
    ```json
    {
       "key":"enthalpy",
       "node":["Property"],
       "type":"value",
       "unit":"J",
       "value":5.0
       "uid":"_:bc3abb68-25b5-4144-aa1b-85d82b7c77e1",
       "uuid":"bc3abb68-25b5-4144-aa1b-85d82b7c77e1",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        type: str = ""
        value: Union[Number, str, None] = None
        unit: Optional[str] = ""
        uncertainty: Optional[Number] = None
        uncertainty_type: str = ""
        component: List[Union[Material, UIDProxy]] = field(default_factory=list)
        structure: str = ""
        method: str = ""
        sample_preparation: Optional[Union[Process, UIDProxy]] = None
        condition: List[Union[Condition, UIDProxy]] = field(default_factory=list)
        data: List[Union[Data, UIDProxy]] = field(default_factory=list)
        computation: List[Union[Computation, UIDProxy]] = field(default_factory=list)
        citation: List[Union[Citation, UIDProxy]] = field(default_factory=list)
        notes: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        key: str,
        type: str,
        value: Union[Number, str, None],
        unit: Union[str, None],
        uncertainty: Optional[Number] = None,
        uncertainty_type: str = "",
        component: Optional[List[Union[Material, UIDProxy]]] = None,
        structure: str = "",
        method: str = "",
        sample_preparation: Optional[Union[Process, UIDProxy]] = None,
        condition: Optional[List[Union[Condition, UIDProxy]]] = None,
        data: Optional[List[Union[Data, UIDProxy]]] = None,
        computation: Optional[List[Union[Computation, UIDProxy]]] = None,
        citation: Optional[List[Union[Citation, UIDProxy]]] = None,
        notes: str = "",
        **kwargs
    ):
        """
        create a property sub-object

        Parameters
        ----------
        key : str
            type of property, Property key must come from the CRIPT Controlled Vocabulary
        type : str
            type of value stored, Property type must come from the CRIPT Controlled Vocabulary
        value : Union[Number, None]
            value or quantity
        unit : str
            unit for value
        uncertainty : Union[Number, None], optional
            uncertainty value of the value, by default None
        uncertainty_type : str, optional
            type of uncertainty, by default ""
        component : Union[List[Material], None], optional
            List of Material nodes, by default None
        structure : str, optional
            specific chemical structure associate with the property with atom mappings**, by default ""
        method : str, optional
            approach or source of property data, by default ""
        sample_preparation : Union[Process, None], optional
            sample preparation, by default None
        condition : Union[List[Condition], None], optional
            conditions under which the property was measured, by default None
        data : Union[List[Data], None], optional
            Data node, by default None
        computation : Union[List[Computation], None], optional
            computation method that produced property, by default None
        citation : Union[List[Citation], None], optional
            reference scholarly work, by default None
        notes : str, optional
            miscellaneous information, or custom data structure (e.g.; JSON), by default ""


        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")

        Returns
        -------
        None
            create a Property sub-object
        """
        if component is None:
            component = []
        if condition is None:
            condition = []
        if computation is None:
            computation = []
        if data is None:
            data = []
        if citation is None:
            citation = []

        super().__init__(**kwargs)
        new_json_attrs = replace(
            self._json_attrs,
            key=key,
            type=type,
            value=value,
            unit=unit,
            uncertainty=uncertainty,
            uncertainty_type=uncertainty_type,
            component=component,
            structure=structure,
            method=method,
            sample_preparation=sample_preparation,
            condition=condition,
            data=data,
            computation=computation,
            citation=citation,
            notes=notes,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def key(self) -> str:
        """
        Property key must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/)

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.key = "angle_rdist"

        Returns
        -------
        str
            Property Key
        """
        return self._json_attrs.key

    @key.setter
    @beartype
    def key(self, new_key: str) -> None:
        """
        set the key for this Property sub-object

        Parameters
        ----------
        new_key : str
            new Property key

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        type of value for this Property sub-object

        [property type](https://app.criptapp.org/vocab/) must come from CRIPT controlled vocabulary

        Examples
        ---------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.type = "max"

        Returns
        -------
        str
            type of value for this Property sub-object
        """
        return self._json_attrs.type

    @type.setter
    @beartype
    def type(self, new_type: str) -> None:
        """
        set the Property type for this subobject

        Parameters
        ----------
        new_type : str
            new Property type

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def value(self) -> Union[Number, str, None]:
        """
        get the Property value

        Returns
        -------
        Union[Number, None]
            Property value
        """
        return self._json_attrs.value

    @beartype
    def set_value(self, new_value: Union[Number, str, None], new_unit: str) -> None:
        """
        set the value attribute of the Property subobject

        Examples
        ---------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.set_value(new_value=1, new_unit="gram")

        Parameters
        ----------
        new_value : Number
            new value
        new_unit : str
            new unit for the value

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, value=new_value, unit=new_unit)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def unit(self) -> Optional[str]:
        """
        get the Property unit for the value

        Returns
        -------
        str
            unit
        """
        return self._json_attrs.unit

    @property
    @beartype
    def uncertainty(self) -> Union[Number, None]:
        """
        get the uncertainty value of the Property node

        Returns
        -------
        Union[Number, None]
            uncertainty value
        """
        return self._json_attrs.uncertainty

    @beartype
    def set_uncertainty(self, new_uncertainty: Optional[Number], new_uncertainty_type: str) -> None:
        """
        set the uncertainty value and type

        Uncertainty type must come from [CRIPT Controlled Vocabulary]

        Parameters
        ----------
        new_uncertainty : Number
            new uncertainty value
        new_uncertainty_type : str
            new uncertainty type

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.set_uncertainty(new_uncertainty=2, new_uncertainty_type="fwhm")

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
        get the uncertainty_type for this Property subobject

        [Uncertainty type](https://app.criptapp.org/vocab/uncertainty_type)
        must come from CRIPT Controlled Vocabulary

        Returns
        -------
        str
            Uncertainty type
        """
        return self._json_attrs.uncertainty_type

    @property
    @beartype
    def component(self) -> List[Union[Material, UIDProxy]]:
        """
        list of Materials that the Property relates to

        Examples
        ---------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_material = cript.Material(name="my material", bigsmiles = "123456")
        >>> my_property.component = [my_material]

        Returns
        -------
        List[Material]
            list of Materials that the Property relates to
        """
        return self._json_attrs.component.copy()

    @component.setter
    @beartype
    def component(self, new_component: List[Union[Material, UIDProxy]]) -> None:
        """
        set the list of Materials as components for the Property subobject

        Parameters
        ----------
        new_component : List[Material]
            new list of Materials to for the Property subobject

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, component=new_component)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def structure(self) -> str:
        """
        specific chemical structure associate with the property with atom mappings

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.structure = "{[][$][C:1][C:1][$],[$][C:2][C:2]([C:2])[$][]}"

        Returns
        -------
        str
            Property structure string
        """
        return self._json_attrs.structure

    @structure.setter
    @beartype
    def structure(self, new_structure: str) -> None:
        """
        set the this Property's structure

        Parameters
        ----------
        new_structure : str
            new structure

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, structure=new_structure)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def method(self) -> str:
        """
        approach or source of property data True sample_preparation Process sample preparation

        [Property method](https://app.criptapp.org/vocab/property_method) must come from CRIPT Controlled Vocabulary

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.method = "ASTM_D3574_Test_A"

        Returns
        -------
        str
            Property method
        """
        return self._json_attrs.method

    @method.setter
    @beartype
    def method(self, new_method: str) -> None:
        """
        set the Property method

        Parameters
        ----------
        new_method : str
            new Property method

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, method=new_method)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def sample_preparation(self) -> Union[Process, None, UIDProxy]:
        """
        sample_preparation

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_process = cript.Process(name="my process name", type="affinity_pure")
        >>> my_property.sample_preparation = my_process

        Returns
        -------
        Union[Process, None]
            Property linking back to the Process that has it as subobject
        """
        return self._json_attrs.sample_preparation

    @sample_preparation.setter
    @beartype
    def sample_preparation(self, new_sample_preparation: Union[Process, None, UIDProxy]) -> None:
        """
        set the sample_preparation for the Property subobject

        Parameters
        ----------
        new_sample_preparation : Union[Process, None]
            back link to the Process that has this Property as its subobject

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, sample_preparation=new_sample_preparation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def condition(self) -> List[Union[Condition, UIDProxy]]:
        """
        list of Conditions under which the property was measured

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_condition = cript.Condition(key="atm", type="max", value=1)
        >>> my_property.condition = [my_condition]

        Returns
        -------
        List[Condition]
            list of Conditions
        """
        return self._json_attrs.condition.copy()

    @condition.setter
    @beartype
    def condition(self, new_condition: List[Union[Condition, UIDProxy]]) -> None:
        """
        set the list of Conditions for this property subobject

        Parameters
        ----------
        new_condition : List[Condition]
            new list of Condition Subobjects

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, condition=new_condition)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def data(self) -> List[Union[Data, UIDProxy]]:
        """
        List of Data nodes for this Property subobjects

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary",
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_property.data = [my_data]

        Returns
        -------
        List[Data]
            list of Data nodes
        """
        return self._json_attrs.data.copy()

    @data.setter
    @beartype
    def data(self, new_data: List[Union[Data, UIDProxy]]) -> None:
        """
        set the Data node for the Property subobject

        Parameters
        ----------
        new_data : List[Data]
            new list of Data nodes

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data=new_data)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def computation(self) -> List[Union[Computation, UIDProxy]]:
        """
        list of Computation nodes that produced this property

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_computation = cript.Computation(name="my computation name", type="analysis")
        >>> my_property.computation = [my_computation]

        Returns
        -------
        List[Computation]
            list of Computation nodes
        """
        return self._json_attrs.computation.copy()

    @computation.setter
    @beartype
    def computation(self, new_computation: List[Union[Computation, UIDProxy]]) -> None:
        """
        set the list of Computation nodes that produced this property

        Parameters
        ----------
        new_computation : List[Computation]
            new list of Computation nodes

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation=new_computation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def citation(self) -> List[Union[Citation, UIDProxy]]:
        """
        list of Citation subobjects for this Property subobject

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     type="journal_article",
        ...     title=title,
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="reference", reference=my_reference)
        >>> my_property.citation = [my_citation]

        Returns
        -------
        List[Citation]
            list of Citation subobjects for this Property subobject
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    @beartype
    def citation(self, new_citation: List[Union[Citation, UIDProxy]]) -> None:
        """
        set the list of Citation subobjects for the Property subobject

        Parameters
        ----------
        new_citation : List[Citation]
            new list of Citation subobjects

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def notes(self) -> str:
        """
        notes for this Property subobject

        Examples
        --------
        >>> import cript
        >>> my_property = cript.Property(key="enthalpy", type="min", value=1.00, unit="J")
        >>> my_property.notes = "these are my notes"

        Returns
        -------
        str
            notes for this property subobject
        """
        return self._json_attrs.notes

    @notes.setter
    @beartype
    def notes(self, new_notes: str) -> None:
        """
        set the notes for this Property sub-object

        Parameters
        ----------
        new_notes : str
            new notes

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, notes=new_notes)
        self._update_json_attrs_if_valid(new_attrs)
