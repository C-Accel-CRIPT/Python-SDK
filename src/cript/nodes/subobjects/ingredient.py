from dataclasses import dataclass, field, replace
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.material import Material
from cript.nodes.subobjects.quantity import Quantity
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Ingredient(UUIDBaseNode):
    """
    ## Definition
    An [Ingredient](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=22)
    sub-objects are links to material nodes with the associated quantities.

    ---

    ## Can Be Added To:
    * [process](../../primary_nodes/process)
    * [computation_process](../../primary_nodes/computation_process)

    ## Available sub-objects:
    * [Quantity](../quantity)

    ---

    ## Attributes

    | attribute  | type           | example  | description            | required | vocab |
    |------------|----------------|----------|------------------------|----------|-------|
    | material   | Material       |          | material               | True     |       |
    | quantity   | list[Quantity] |          | quantities             | True     |       |
    | keyword    | list(str)      | catalyst | keyword for ingredient |          | True  |

    ## JSON Representation
    ```json
    {
        "node":["Ingredient"],
        "keyword":["catalyst"],
        "uid":"_:32f173ab-a98a-449b-a528-1b656f652dd3",
        "uuid":"32f173ab-a98a-449b-a528-1b656f652dd3"
       "material":{
          "name":"my material 1",
          "node":["Material"],
          "bigsmiles":"[H]{[>][<]C(C[>])c1ccccc1[]}",
          "uid":"_:029367a8-aee7-493a-bc08-991e0f6939ae",
          "uuid":"029367a8-aee7-493a-bc08-991e0f6939ae"
       },
       "quantity":[
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
       ]
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        material: Optional[Union[Material, UIDProxy]] = None
        quantity: List[Union[Quantity, UIDProxy]] = field(default_factory=list)
        keyword: List[str] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, material: Union[Material, UIDProxy], quantity: List[Union[Quantity, UIDProxy]], keyword: Optional[List[str]] = None, **kwargs):
        """
        create an ingredient sub-object

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(name="my material", bigsmiles="my bigsmiles")
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient = cript.Ingredient(
        ...     material=my_material, quantity=[my_quantity], keyword=["catalyst"]
        ... )

        Parameters
        ----------
        material : Material
            material node
        quantity : List[Quantity]
            list of quantity sub-objects
        keyword : List[str], optional
            ingredient keyword must come from
            [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/ingredient_keyword), by default ""

        Returns
        -------
        None
            Create new Ingredient sub-object
        """
        super().__init__(**kwargs)
        if keyword is None:
            keyword = []
        new_json_attrs = replace(self._json_attrs, material=material, quantity=quantity, keyword=keyword)
        self._update_json_attrs_if_valid(new_json_attrs)

    @classmethod
    def _from_json(cls, json_dict: dict):
        # TODO: remove this temporary fix, once back end is working correctly
        if isinstance(json_dict["material"], list):
            json_dict["material"] = json_dict["material"][0]
        return super(Ingredient, cls)._from_json(json_dict)

    @property
    @beartype
    def material(self) -> Union[Material, None, UIDProxy]:
        """
        current material in this ingredient sub-object

        Returns
        -------
        Material
            Material node within the ingredient sub-object
        """
        return self._json_attrs.material

    @property
    @beartype
    def quantity(self) -> List[Union[Quantity, UIDProxy]]:
        """
        quantity for the ingredient sub-object

        Returns
        -------
        List[Quantity]
            list of quantities for the ingredient sub-object
        """
        return self._json_attrs.quantity.copy()

    @beartype
    def set_material(self, new_material: Union[Material, UIDProxy], new_quantity: List[Union[Quantity, UIDProxy]]) -> None:
        """
        update ingredient sub-object with new material and new list of quantities

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(name="my material", bigsmiles = "123456")
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient = cript.Ingredient(
        ...     material=my_material, quantity=[my_quantity], keyword=["catalyst"]
        ... )
        >>> my_new_material = cript.Material(
        ...     name="my material", bigsmiles = "78910"
        ... )
        >>> my_new_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient.set_material(new_material=my_new_material, new_quantity=[my_new_quantity])

        Parameters
        ----------
        new_material : Material
            new material node to replace the current
        new_quantity : List[Quantity]
            new list of quantity sub-objects to replace the current quantity subobject on this node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, material=new_material, quantity=new_quantity)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def keyword(self) -> List[str]:
        """
        ingredient keyword must come from the
        [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/ingredient_keyword)

        Examples
        --------
        >>> import cript
        >>> my_material = cript.Material(name="my material", bigsmiles = "123456")
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient = cript.Ingredient(
        ...     material=my_material, quantity=[my_quantity], keyword=["catalyst"]
        ... )
        >>> my_ingredient.keyword = ["computation"]

        Returns
        -------
        str
            get the current ingredient keyword
        """
        return self._json_attrs.keyword.copy()

    @keyword.setter
    @beartype
    def keyword(self, new_keyword: List[str]) -> None:
        """
        set new ingredient keyword to replace the current

        Parameters
        ----------
        new_keyword : str
            new ingredient keyword

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, keyword=new_keyword)
        self._update_json_attrs_if_valid(new_attrs)
