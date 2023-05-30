from dataclasses import dataclass, field, replace
from typing import List, Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.material import Material
from cript.nodes.subobjects.quantity import Quantity


class Ingredient(BaseNode):
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
    | keyword    | str            | catalyst | keyword for ingredient |          | True  |

    ## JSON Representation
    ```json

    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        material: Union[Material, None] = None
        quantity: List[Quantity] = field(default_factory=list)
        keyword: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, material: Material, quantity: List[Quantity], keyword: str = "", **kwargs):
        """
        create an ingredient sub-object

        Examples
        --------
        ```python
        import cript

        # create material and identifier for the ingredient sub-object
        my_identifiers = [{"bigsmiles": "123456"}]
        my_material = cript.Material(name="my material", identifier=my_identifiers)

        # create quantity sub-object
        my_quantity = cript.Quantity(key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev")

        # create ingredient sub-object and add all appropriate nodes/sub-objects
        my_ingredient = cript.Ingredient(material=my_material, quantity=my_quantity, keyword="catalyst")
        ```

        Parameters
        ----------
        material : Material
            material node
        quantity : List[Quantity]
            list of quantity sub-objects
        keyword : str, optional
            ingredient keyword must come from [CRIPT Controlled Vocabulary](), by default ""

        Returns
        -------
        None
            Create new Ingredient sub-object
        """
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, material=material, quantity=quantity, keyword=keyword)
        self.validate()

    @property
    def material(self) -> Material:
        """
        current material in this ingredient sub-object

        Returns
        -------
        Material
            Material node within the ingredient sub-object
        """
        return self._json_attrs.material

    @property
    def quantity(self) -> List[Quantity]:
        """
        quantity for the ingredient sub-object

        Returns
        -------
        List[Quantity]
            list of quantities for the ingredient sub-object
        """
        return self._json_attrs.quantity.copy()

    def set_material(self, new_material: Material, new_quantity: List[Quantity]) -> None:
        """
        update ingredient sub-object with new material and new list of quantities

        Examples
        --------
        ```python
        my_identifiers = [{"bigsmiles": "123456"}]
        my_new_material = cript.Material(name="my material", identifier=my_identifiers)

        my_new_quantity = cript.Quantity(
            key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        )

        # set new material and list of quantities
        my_ingredient.set_material(new_material=my_new_material, new_quantity=[my_new_quantity])

        ```

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
    def keyword(self) -> str:
        """
        ingredient keyword must come from the [CRIPT controlled vocabulary]()

        Examples
        --------
        ```python
        # set new ingredient keyword
        my_ingredient.keyword = "computation"
        ```

        Returns
        -------
        str
            get the current ingredient keyword
        """
        return self._json_attrs.keyword

    @keyword.setter
    def keyword(self, new_keyword: str) -> None:
        """
        set new ingredient keyword to replace the current

        ingredient keyword must come from the [CRIPT controlled vocabulary]()

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
