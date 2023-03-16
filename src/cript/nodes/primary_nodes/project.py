from dataclasses import dataclass, replace
from typing import List, Union, Any

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.supporting_nodes.file import File
from cript.nodes.supporting_nodes.group import Group


class Project(PrimaryBaseNode):
    """
    Project node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Project"
        # project name
        name: str = ""
        group: Group = None
        collection: List[Collection] = None
        material: List[Material] = None
        file: List[File] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, group: Group):
        """

        Parameters
        ----------
        name
        group
        """
        super().__init__(node="Project")
        pass

    # ------------------ Properties ------------------

    # Project Name
    @property
    def name(self) -> str:
        return self._json_attrs.name

    @name.setter
    def name(self, new_name: str):
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    # GROUP
    @property
    def group(self) -> Group:
        return self._json_attrs.group

    @group.setter
    def group(self, new_group: Group):
        new_attrs = replace(self._json_attrs, group=new_group)
        self._update_json_attrs_if_valid(new_attrs)

    def _set_node_or_list(self, field_name: str, new_node: Union[BaseNode, List[BaseNode]]):
        """
        This method sets a field that is a list of node or a single node for this project.
        The user can pass in either a node (such as collection, material, or file )
        to be appended to the list of collections
        or the user can pass in a list of collections to replace the old list of collections.
        This method works by checking if the argument is a list or a single node and
        then behaves accordingly.

        Parameters
        ----------
        field_name: str
            field name within the dataclass JsonAttributes

        new_node: Union[BaseNode, List[BaseNode]
            new node to append to node list
            or new list of nodes to replace the current list

        Returns
        -------
        None
        """
        if isinstance(new_node, list):
            # replace the old list with the new list
            # TODO see if you can write **{field_name: new_node} in a better way
            new_attrs = replace(self._json_attrs, **{field_name: new_node})
            # TODO this needs a more DRY way of handling this
            self._update_json_attrs_if_valid(new_attrs)

        # if appending a single node to the list
        # get the old list, append the node, and replace the field
        else:
            # TODO see if you can write this better
            new_list: List[BaseNode] = getattr(self._json_attrs, field_name)
            new_list.append(new_node)
            new_attrs = replace(self._json_attrs, **{field_name: new_list})
            self._update_json_attrs_if_valid(new_attrs)

    # Collection
    @property
    def collection(self) -> List[Collection]:
        return self._json_attrs.collection

    # TODO collection, material, and file (all lists) have the same logic,
    #   make a single function to take care of it
    @collection.setter
    def collection(self, new_collection: Union[Collection, List[Collection]]):
        """
        This method sets the collection for this project.
        The user can pass in either a collection to be appended to the list of collection
        or the user can pass in a list of collections to replace the old list of collections.
        This method works by checking if the argument is a list or collection object and
        behaves accordingly.

        Parameters
        ----------
        new_collection: Collection or List[Collection]
            new collection to append to collection list
            or new list of collections to replace the current list
        """

        if isinstance(new_collection, list):
            new_attrs = replace(self._json_attrs, collection=new_collection)
            self._update_json_attrs_if_valid(new_attrs)

        # if appending a single collection to the list
        # get the old list, append the collection, and replace the field
        else:
            new_list: List[Collection] = self._json_attrs.collection
            new_list.append(new_collection)
            new_attrs = replace(self._json_attrs, collection=new_list)
            self._update_json_attrs_if_valid(new_attrs)

    # Material
    @property
    def material(self) -> List[Material]:
        return self._json_attrs.material

    @material.setter
    def material(self, new_material: Union[Material, List[Material]]):
        """
        This method sets the Material for this project.
        The user can pass in either a Material to be appended to the list of Material
        or the user can pass in a list of Material to replace the old list of Material.
        This method works by checking if the argument is a list or Material object and
        behaves accordingly.

        Parameters
        ----------
        new_material: Material or List[Material]
            new Material to append to Material list
            or new list of Material to replace the current list
        """
        if isinstance(new_material, list):
            new_attrs = replace(self._json_attrs, collection=new_material)
            self._update_json_attrs_if_valid(new_attrs)

        # if appending a single material to the list
        # get the old list, append the material, and replace the field
        else:
            new_list: List[Collection] = self._json_attrs.collection
            new_list.append(new_material)
            new_attrs = replace(self._json_attrs, collection=new_list)
            self._update_json_attrs_if_valid(new_attrs)

    # File
    @property
    def file(self) -> List[File]:
        return self._json_attrs.file

    @file.setter
    def file(self, new_file: Union[File, List[File]]):
        if isinstance(new_file, list):
            new_attrs = replace(self._json_attrs, file=new_file)
            self._update_json_attrs_if_valid(new_attrs)

            # if appending a single material to the list
            # get the old list, append the material, and replace the field
        else:
            new_list: List[File] = self._json_attrs.file
            new_list.append(new_file)
            new_attrs = replace(self._json_attrs, file=new_list)
            self._update_json_attrs_if_valid(new_attrs)
