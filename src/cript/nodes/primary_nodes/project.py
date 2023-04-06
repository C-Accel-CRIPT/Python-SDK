from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes.group import Group


class Project(PrimaryBaseNode):
    """
    Project node
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Project attributes
        """

        # TODO is group needed?
        group: Group = None
        collections: List[Collection] = field(default_factory=list)
        materials: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        group: Group,
        collections: List[Collection] = None,
        materials: List[Material] = None,
        notes: str = "",
        **kwargs
    ):
        """
        Create a Project node with Project name and Group

        Parameters
        ----------
        name: str
            project name

        Collections: List[Collection]
            list of Collections that belongs to this Project

        Returns
        -------
        None
        """
        super().__init__(node="Project", name=name, notes=notes)

        if collections is None:
            collections = []

        if materials is None:
            materials = []

        self._json_attrs = replace(self._json_attrs, name=name, collections=collections, materials=materials)
        self.validate()

    # ------------------ Properties ------------------

    # GROUP
    @property
    def group(self) -> Group:
        """
        group property getter method

        Returns
        -------
        group: cript.Group
            Group that owns the project
        """
        return self._json_attrs.group

    @group.setter
    def group(self, new_group: Group):
        """
        Sets the group the project belongs to

        Parameters
        ----------
        new_group: Group
            new Group object

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, group=new_group)
        self._update_json_attrs_if_valid(new_attrs)

    # Collection
    @property
    def collections(self) -> List[Collection]:
        """
        Collection property getter method

        Returns
        -------
        Collection: List[Collection]
            the list of collections within this project
        """
        return self._json_attrs.collections

    # Collection
    @collections.setter
    def collections(self, new_collection: List[Collection]) -> None:
        """
        set list of collections for the project node

        Parameters
        ----------
        new_collection: List[Collection]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, collections=new_collection)
        self._update_json_attrs_if_valid(new_attrs)

    # Material
    @property
    def material(self) -> List[Material]:
        """
        Material property getter method. Gets the list of materials within the project

        Returns
        -------
        Material: List[Material]
            List of materials that belongs to this project
        """
        return self._json_attrs.materials

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
        new_attrs = replace(self._json_attrs, materials=new_materials)
        self._update_json_attrs_if_valid(new_attrs)
