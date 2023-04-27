from dataclasses import dataclass, field, replace
from typing import List

import requests

from cript.api.exceptions import CRIPTAPISaveError
from cript.nodes.primary_nodes.collection import Collection
from cript.nodes.primary_nodes.material import Material
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes.group import Group


class Project(PrimaryBaseNode):
    """
    ## Definition
    A [Project](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=7)
    is the highest level node that is Not nested inside any other node.
    A Project can be thought of as a folder that can contain [Collections](../collection) and
    [Materials](../materials).


    | attribute   | type             | description                            |
    |-------------|------------------|----------------------------------------|
    | collections | List[Collection] | collections that relate to the project |
    | materials   | List[Materials]  | materials owned by the project         |

    <!-- TODO consider adding JSON section -->
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Project attributes
        """

        # TODO is group needed?
        group: Group = None
        collections: List[Collection] = field(default_factory=list)
        material: List[Material] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        # group: Group,
        collections: List[Collection] = None,
        material: List[Material] = None,
        notes: str = "",
        **kwargs,
    ):
        """
        Create a Project node with Project name and Group

        Parameters
        ----------
        name: str
            project name
        collections: List[Collection]
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
        super().__init__(name=name, notes=notes)

        if collections is None:
            collections = []

        if material is None:
            material = []

        self._json_attrs = replace(self._json_attrs, name=name, collections=collections, material=material)
        self.validate()

    def save(self, api=None) -> None:
        """
        This method takes a project node, serializes the class into JSON
        and then sends the JSON to be saved to the API.
        It takes Project node because everything is connected to the Project node,
        and it can be used to send either a POST or PATCH request to API

        Parameters
        ----------
        api: API
            API object with which the operation should be performed. If None the current active (context managed) api object is used.

        Raises
        ------
        CRIPTAPISaveError
            If the API responds with anything other than an HTTP of `200`, the API error is displayed to the user

        Returns
        -------
        None
            Just sends a `POST` or `Patch` request to the API
        """
        from cript.api.api import _get_global_cached_api

        # TODO work on this later to allow for PATCH as well
        if api is None:
            api = _get_global_cached_api()

        response = requests.post(url=f"{api.host}/{self.node_type.lower()}", headers=api._http_headers, data=self.json)

        response = response.json()

        # if htt response is not 200 then show the API error to the user
        if response["code"] != 200:
            raise CRIPTAPISaveError(api_host_domain=api.host, http_code=response["code"], api_response=response["error"])

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
        Collection is a Project node's property that can be set during creation in the constructor
        or later by setting the project's property

        Examples
        --------
        ```python
        my_new_collection = cript.Collection(
            name="my collection name", experiments=[my_experiment_node]
        )

        my_project.collections = my_new_collection
        ```

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
    def materials(self, new_materials: List[Material]) -> None:
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
