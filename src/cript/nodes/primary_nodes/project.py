from dataclasses import dataclass, replace
from typing import List, Union, Any

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes.file import File
from cript.nodes.supporting_nodes.group import Group


class Project(PrimaryBaseNode):
    """
    Project node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Project attributes
        """
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
        Create a Project node with Project name and Group

        Parameters
        ----------
        name: str
            project name
        group: Group
            Group that owns the Project

        Returns
        -------
        None
        """
        super().__init__(node="Project")
        pass

    # ------------------ Properties ------------------

    # Project Name
    @property
    def name(self) -> str:
        """
        name property getter method

        Returns
        -------
        name: str
            project name
        """
        return self._json_attrs.name

    @name.setter
    def name(self, new_name: str):
        """
        Setter for the project name

        Parameters
        ----------
        new_name: str
            new project name

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    # GROUP
    @property
    def group(self) -> Group:
        """
        group property getter method

        Returns
        -------
        group: Group
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

    # TODO consider switching any to BaseNode 
    def _set_node_or_list(self, field_name: str, new_node: Union[Any, List[Any]]):
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
        """
        Collection property getter method

        Returns
        -------
        Collection: List[Collection]
            the list of collections within this project
        """
        return self._json_attrs.collection

    # TODO collection, material, and file (all lists) have the same logic,
    #   make a single function to take care of it
    # Collection
    @collection.setter
    def collection(self, new_collection: Union[Collection, List[Collection]]):
        """
        Setter for the collection.

        User has 2 options
        1. pass a single collection that can be added to the list of collections
        2. the user can pass a list of collections that will replace the current list of collections

        simply calls the _set_node_or_list() method with field name and parameter passed into here

        Parameters
        ----------
        new_collection: Union[Collection, List[Collection]
            Either a single collection to be added to the list of collections
            or a list of collections to replace the current list of collections

        Returns
        -------
        None
        """
        self._set_node_or_list("collection", new_collection)

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
        return self._json_attrs.material

    @material.setter
    def material(self, new_material: Union[Material, List[Material]]):
        """
        Setter for the material.

        User has 2 options
        1. pass a single material that can be added to the list of material
        2. the user can pass a list of material that will replace the current list of material

        simply calls the _set_node_or_list() method with field name and a single node or list of nodes


        Parameters
        ----------
        new_material: Material or List[Material]
            new Material to append to Material list
            or new list of Material to replace the current list

        Returns
        -------
        None
        """
        self._set_node_or_list("material", new_material)

    # File
    @property
    def file(self) -> List[File]:
        """
        file property getter method.

        Returns
        -------
        File: Lis[File]
            list of files that belongs in this project
        """
        return self._json_attrs.file

    @file.setter
    def file(self, new_file: Union[File, List[File]]):
        """
        Setter for the file.

        User has 2 options
        1. pass a single file that can be added to the list of file
        2. the user can pass a list of file that will replace the current list of file

        simply calls the _set_node_or_list() method with field name and a single node or list of nodes


       Parameters
       ----------
       new_file: File or List[File]
           new File to append to File list
           or new list of File to replace the current list

       Returns
       -------
       None
       """
        self._set_node_or_list("file", new_file)
