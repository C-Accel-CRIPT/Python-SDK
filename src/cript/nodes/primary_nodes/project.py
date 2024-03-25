import warnings
from dataclasses import dataclass, field, replace
from typing import List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes import User
from cript.nodes.util.json import UIDProxy


class Project(PrimaryBaseNode):
    """
    ## Definition
    A [Project](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=7)
    is the highest level node that is Not nested inside any other node.
    A Project can be thought of as a folder that can contain [Collections](../collection) and
    [Materials](../material).


    | attribute  | type             | description                                         |
    |------------|------------------|-----------------------------------------------------|
    | collection | List[Collection] | collections that relate to the project              |
    | materials  | List[Materials]  | materials owned by the project                      |
    | notes      | str              | miscellaneous information, or custom data structure |

    ## JSON Representation
    ```json
    {
       "name":"my project name",
       "node":["Project"],
       "uid":"_:270168b7-fc29-4c37-aa93-334212e1d962",
       "uuid":"270168b7-fc29-4c37-aa93-334212e1d962",
       "collection":[
          {
            "name":"my collection name",
             "node":["Collection"],
             "uid":"_:c60955a5-4de0-4da5-b2c8-77952b1d9bfa",
             "uuid":"c60955a5-4de0-4da5-b2c8-77952b1d9bfa",
             "experiment":[
                {
                   "name":"my experiment name",
                   "node":["Experiment"],
                   "uid":"_:a8cbc083-506e-45ce-bb8f-5e50917ab361",
                   "uuid":"a8cbc083-506e-45ce-bb8f-5e50917ab361"
                }
             ],
             "inventory":[],
             "citation":[]
          }
       ]
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Project attributes
        """

        member: List[Union[User, UIDProxy]] = field(default_factory=list)
        admin: List[Union[User, UIDProxy]] = field(default_factory=list)
        collection: List[Union[Collection, UIDProxy]] = field(default_factory=list)
        material: List[Union[Material, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, name: str, collection: Optional[List[Union[Collection, UIDProxy]]] = None, material: Optional[List[Union[Material, UIDProxy]]] = None, notes: str = "", **kwargs):
        """
        Create a Project node with Project name

        Examples
        --------
        >>> import cript
        >>> my_project = cript.Project(name="my Project name")


        Parameters
        ----------
        name: str
            project name
        collection: List[Collection]
            list of Collections that belongs to this Project
         material: List[Material]
            list of materials that belongs to this project
        notes: str
            notes for this project

        Returns
        -------
        None
            instantiate a Project node
        """
        super().__init__(name=name, notes=notes, **kwargs)

        if collection is None:
            collection = []

        if material is None:
            material = []

        new_json_attrs = replace(self._json_attrs, name=name, collection=collection, material=material)
        self._update_json_attrs_if_valid(new_json_attrs)

    def validate(self, api=None, is_patch=False, force_validation: bool = False):
        from cript.nodes.exceptions import CRIPTOrphanedMaterialWarning
        from cript.nodes.util.core import get_orphaned_experiment_exception

        # First validate like other nodes
        super().validate(api=api, is_patch=is_patch, force_validation=force_validation)

        # Check graph for orphaned nodes, that should be listed in project
        # Project.materials should contain all material nodes
        project_graph_materials = self.find_children({"node": ["Material"]})
        # Combine all materials listed in the project inventories
        project_inventory_materials = []
        for inventory in self.find_children({"node": ["Inventory"]}):
            for material in inventory.material:
                project_inventory_materials.append(material)
        for material in project_graph_materials:
            if material not in self.material and material not in project_inventory_materials:
                warnings.warn(CRIPTOrphanedMaterialWarning(material))

        # Check graph for orphaned nodes, that should be listed in the experiments
        project_experiments = self.find_children({"node": ["Experiment"]})
        # There are 4 different types of nodes Experiments are collecting.
        node_types = ("Process", "Computation", "ComputationProcess", "Data")
        # We loop over them with the same logic
        for node_type in node_types:
            # All in the graph has to be in at least one experiment
            project_graph_nodes = self.find_children({"node": [node_type]})
            node_type_attr = node_type.lower()
            # Non-consistent naming makes this necessary for Computation Process
            if node_type == "ComputationProcess":
                node_type_attr = "computation_process"

            # Concatenation of all experiment attributes (process, computation, etc.)
            # Every node of the graph must be present somewhere in this concatenated list.
            experiment_nodes = []
            for experiment in project_experiments:
                for ex_node in getattr(experiment, node_type_attr):
                    experiment_nodes.append(ex_node)
            for node in project_graph_nodes:
                if node not in experiment_nodes:
                    warnings.warn(get_orphaned_experiment_exception(node))

    @property
    @beartype
    def member(self) -> List[Union[User, UIDProxy]]:
        return self._json_attrs.member.copy()

    @property
    @beartype
    def admin(self) -> List[Union[User, UIDProxy]]:
        return self._json_attrs.admin

    @property
    @beartype
    def collection(self) -> List[Union[Collection, UIDProxy]]:
        """
        Collection is a Project node's property that can be set during creation in the constructor
        or later by setting the project's property

        Examples
        --------
        >>> import cript
        >>> my_project = cript.Project(name="my Project name")
        >>> my_new_collection = cript.Collection(name="my collection name")
        >>> my_project.collection = [my_new_collection]

        Returns
        -------
        Collection: List[Collection]
            the list of collections within this project
        """
        return self._json_attrs.collection

    @collection.setter
    @beartype
    def collection(self, new_collection: List[Union[Collection, UIDProxy]]) -> None:
        """
        set list of collections for the project node

        Parameters
        ----------
        new_collection: List[Collection]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, collection=new_collection)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def material(self) -> List[Union[Material, UIDProxy]]:
        """
        List of Materials that belong to this Project.

        Examples
        --------
        >>> import cript
        >>> my_project = cript.Project(name="my Project name")
        >>> my_material = cript.Material(name="my material", bigsmiles="my bigsmiles")
        >>> my_project.material = [my_material]

        Returns
        -------
        Material: List[Material]
            List of materials that belongs to this project
        """
        return self._json_attrs.material

    @material.setter
    @beartype
    def material(self, new_materials: List[Union[Material, UIDProxy]]) -> None:
        """
        set the list of materials for this project

        Parameters
        ----------
        new_materials: List[Material]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, material=new_materials)
        self._update_json_attrs_if_valid(new_attrs)
