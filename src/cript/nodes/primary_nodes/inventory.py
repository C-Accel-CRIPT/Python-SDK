from dataclasses import dataclass, field, replace
from typing import List

from beartype import beartype

from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Inventory(PrimaryBaseNode):
    """
    ## Definition
    An
    [Inventory Node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=9)
    is a list of material nodes.
    An example of an inventory can be a grouping of materials that were extracted from literature
    and curated into a group for machine learning, or it can be a subset of chemicals that are used for a
    certain type of synthesis.

    ## Attributes
    | Attribute | Type                            | Example            | Description                                         |
    |-----------|---------------------------------|--------------------|-----------------------------------------------------|
    | material  | list[[Material](./material.md)] |                    | material that you like to group together            |
    | notes     | str                             | "my awesome notes" | miscellaneous information, or custom data structure |


    ## JSON Representation
    ```json
    {
       "name":"my inventory name",
       "node":["Inventory"],
       "uid":"_:90f45778-b7c9-4b77-8b83-a6ea9671a937",
       "uuid":"90f45778-b7c9-4b77-8b83-a6ea9671a937",
       "material":[
          {
             "node":["Material"],
             "name":"my material 1",
             "uid":"_:9679ff12-f9b4-41f4-be95-080b78fa71fd",
             "uuid":"9679ff12-f9b4-41f4-be95-080b78fa71fd"
             "bigsmiles":"[H]{[>][<]C(C[>])c1ccccc1[]}",
          },
          {
             "node":["Material"],
             "name":"my material 2",
             "uid":"_:1ee41708-3531-43eb-8049-4bb91ad73df6",
             "uuid":"1ee41708-3531-43eb-8049-4bb91ad73df6"
             "bigsmiles":"654321",
          }
       ]
    }
    ```


    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Inventory attributes
        """

        material: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, name: str, material: List[Material], notes: str = "", **kwargs) -> None:
        """
        Instantiate an inventory node

        Examples
        --------
        ```python
        material_1 = cript.Material(
            name="material 1",
            identifiers=[{"alternative_names": "material 1 alternative name"}],
        )

        material_2 = cript.Material(
            name="material 2",
            identifiers=[{"alternative_names": "material 2 alternative name"}],
        )

        # instantiate inventory node
        my_inventory = cript.Inventory(
            name="my inventory name", material=[material_1, material_2]
        )
        ```

        Parameters
        ----------
        material: List[Material]
            list of materials in this inventory

        Returns
        -------
        None
            instantiate an inventory node
        """

        if material is None:
            material = []

        super().__init__(name=name, notes=notes, **kwargs)

        self._json_attrs = replace(self._json_attrs, material=material)

    @property
    @beartype
    def material(self) -> List[Material]:
        """
        List of [material](../material) in this inventory

        Examples
        --------
        ```python
        material_3 = cript.Material(
            name="new material 3",
            identifiers=[{"alternative_names": "new material 3 alternative name"}],
        )

        my_inventory.material = [my_material_3]
        ```

        Returns
        -------
        List[Material]
            list of material representing the inventory within the collection
        """
        return self._json_attrs.material.copy()

    @material.setter
    @beartype
    def material(self, new_material_list: List[Material]):
        """
        set the list of material for this inventory node

        Parameters
        ----------
        new_material_list: List[Material]
            new list of material to replace the current list of material nodes for this inventory node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, material=new_material_list)
        self._update_json_attrs_if_valid(new_attrs)
