from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes import User


class Project(PrimaryBaseNode):
    """
    ## Definition
    A [Project](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=7)
    is the highest level node that is Not nested inside any other node.
    A Project can be thought of as a folder that can contain [Collections](../collection) and
    [Materials](../materials).


    | attribute   | type             | description                            |
    |-------------|------------------|----------------------------------------|
    | collection | List[Collection] | collections that relate to the project |
    | materials   | List[Materials]  | materials owned by the project         |

    <!-- TODO consider adding JSON section -->
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Project attributes
        """

        member: List[User] = field(default_factory=list)
        admin: User = None
        collection: List[Collection] = field(default_factory=list)
        material: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, collection: List[Collection] = None, material: List[Material] = None, notes: str = "", **kwargs):
        """
        Create a Project node with Project name and Group

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

        self._json_attrs = replace(self._json_attrs, name=name, collection=collection, material=material)
        self.validate()

    def validate(self):
        from cript.nodes.exceptions import (
            CRIPTOrphanedMaterialError,
            get_orphaned_experiment_exception,
        )

        # First validate like other nodes
        super().validate()

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
                raise CRIPTOrphanedMaterialError(material)

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

            # Concatination of all experiment attributes (process, computation, etc.)
            # Every node of the graph must be present somewhere in this concatinated list.
            experiment_nodes = []
            for experiment in project_experiments:
                for ex_node in getattr(experiment, node_type_attr):
                    experiment_nodes.append(ex_node)
            for node in project_graph_nodes:
                if node not in experiment_nodes:
                    raise get_orphaned_experiment_exception(node)

    # ------------------ Properties ------------------

    @property
    def member(self) -> List[User]:
        return self._json_attrs.member.copy()

    @property
    def admin(self) -> User:
        return self._json_attrs.admin

    # Collection
    @property
    def collection(self) -> List[Collection]:
        """
        Collection is a Project node's property that can be set during creation in the constructor
        or later by setting the project's property

        Examples
        --------
        ```python
        my_new_collection = cript.Collection(
            name="my collection name", experiments=[my_experiment_node]
        )

        my_project.collection = my_new_collection
        ```

        Returns
        -------
        Collection: List[Collection]
            the list of collections within this project
        """
        return self._json_attrs.collection

    # Collection
    @collection.setter
    def collection(self, new_collection: List[Collection]) -> None:
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

    # Material
    @property
    def material(self) -> List[Material]:
        """
        List of Materials that belong to this Project.

        Examples
        --------
        ```python
        identifiers = [{"alternative_names": "my material alternative name"}]
        my_material = cript.Material(name="my material", identifiers=identifiers)

        my_project.material = [my_material]
        ```

        Returns
        -------
        Material: List[Material]
            List of materials that belongs to this project
        """
        return self._json_attrs.material

    @material.setter
    def material(self, new_materials: List[Material]) -> None:
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
