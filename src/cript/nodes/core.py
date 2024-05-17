import copy
import dataclasses
import json
import re
import uuid
from abc import ABC
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Set

from cript.nodes.exceptions import (
    CRIPTAttributeModificationError,
    CRIPTExtraJsonAttributes,
    CRIPTJsonSerializationError,
)
from cript.nodes.node_iterator import NodeIterator

tolerated_extra_json = []


def add_tolerated_extra_json(additional_tolerated_json: str):
    """
    In case a node should be loaded from JSON (such as `getting` them from the API),
    but the API sends additional JSON attributes, these can be set to tolerated temporarily with this routine.
    """
    tolerated_extra_json.append(additional_tolerated_json)


def get_new_uid():
    return "_:" + str(uuid.uuid4())


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        if obj is None:
            return self.f(owner)
        return self.f(obj)


class BaseNode(ABC):
    """
    This abstract class is the base of all CRIPT nodes.
    It offers access to a json attribute class,
    which reflects the data model JSON attributes.
    Also, some basic shared functionality is provided by this base class.
    """

    @dataclass(frozen=True)
    class JsonAttributes:
        node: List[str] = dataclasses.field(default_factory=list)
        uid: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @classproperty
    def node_type(self):
        name = type(self).__name__
        if name == "ABCMeta":
            name = self.__name__
        return name

    @classproperty
    def node_type_snake_case(self):
        camel_case = self.node_type
        # Regex to convert camel case to snake case.
        snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case).lower()
        return snake_case

    # Prevent new attributes being set.
    # This might just be temporary, but for now, I don't want to accidentally add new attributes, when I mean to modify one.
    def __setattr__(self, key, value):
        if not hasattr(self, key):
            raise CRIPTAttributeModificationError(self.node_type, key, value)
        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            if kwarg not in tolerated_extra_json:
                if kwarg.endswith("_count"):
                    try:
                        possible_array = getattr(self._json_attrs.kwarg[: -len("_count")])
                        if not isinstance(possible_array, list):
                            raise CRIPTExtraJsonAttributes(self.node_type, kwarg)
                    except AttributeError:
                        raise CRIPTExtraJsonAttributes(self.node_type, kwarg)
                else:
                    try:
                        getattr(self._json_attrs, kwarg)
                    except AttributeError:
                        raise CRIPTExtraJsonAttributes(self.node_type, kwarg)

        uid = get_new_uid()
        self._json_attrs = replace(self._json_attrs, node=[self.node_type], uid=uid)

    def __str__(self) -> str:
        """
        Return a string representation of a node data model attributes.

        Returns
        -------
        str
            A string representation of the node.
        """
        return str(self._json_attrs)

    @property
    def uid(self):
        return self._json_attrs.uid

    @property
    def node(self):
        return self._json_attrs.node

    def _update_json_attrs_if_valid(self, new_json_attr: JsonAttributes) -> None:
        """
        tries to update the node if valid and then checks if it is valid or not

        1. updates the node with the new information
        1. run db schema validation on it
            1. if db schema validation succeeds then update and continue
            1. else: raise an error and tell the user what went wrong

        Parameters
        ----------
        new_json_attr

        Raises
        ------
        Exception

        Returns
        -------
        None
        """
        old_json_attrs = self._json_attrs
        self._json_attrs = new_json_attr

        try:
            self.validate()
        except Exception as exc:
            self._json_attrs = old_json_attrs
            raise exc

    def validate(self, api=None, is_patch: bool = False, force_validation: bool = False) -> None:
        """
        Validate this node (and all its children) against the schema provided by the data bank.

        Raises:
        -------
        Exception with more error information.
        """
        from cript.api.api import _get_global_cached_api

        if api is None:
            api = _get_global_cached_api()
        api.schema.is_node_schema_valid(self.get_json(is_patch=is_patch).json, is_patch=is_patch, force_validation=force_validation)

    @classmethod
    def _from_json(cls, json_dict: dict):
        # TODO find a way to handle uuid nodes only

        # Child nodes can inherit and overwrite this.
        # They should call super()._from_json first, and modified the returned object after if necessary
        # We create manually a dict that contains all elements from the send dict.
        # That eliminates additional fields and doesn't require asdict.
        arguments = {}
        default_dataclass = cls.JsonAttributes()
        for field in json_dict:
            try:
                getattr(default_dataclass, field)
            except AttributeError:
                pass
            else:
                arguments[field] = json_dict[field]
        try:  # TODO remove this hack to work with compatible model versions
            del arguments["model_version"]
        except KeyError:
            pass

        # add omitted fields from default (necessary if they are required)
        for field_name in [field.name for field in dataclasses.fields(default_dataclass)]:
            if field_name not in arguments:
                arguments[field_name] = getattr(default_dataclass, field_name)

        try:
            node = cls(**arguments)
        # TODO we should not catch all exceptions if we are handling them, and instead let it fail
        #  to create a good error message that points to the correct place that it failed to make debugging easier
        except Exception as exc:
            print(cls, arguments)
            raise exc

        attrs = cls.JsonAttributes(**arguments)

        # Handle default attributes manually.
        for field in attrs.__dict__:
            # Conserve newly assigned uid if uid is default (empty)
            if getattr(attrs, field) == getattr(default_dataclass, field):
                attrs = replace(attrs, **{str(field): getattr(node, field)})

        try:  # TODO remove this temporary solution
            if not attrs.uid.startswith("_:"):
                attrs = replace(attrs, uid="_:" + attrs.uid)
        except AttributeError:
            pass

        # But here we force even usually unwritable fields to be set.
        node._update_json_attrs_if_valid(attrs)

        return node

    def __deepcopy__(self, memo):
        from cript.nodes.util.core import get_uuid_from_uid

        # Ideally I would call `asdict`, but that is not allowed inside a deepcopy chain.
        # Making a manual transform into a dictionary here.
        arguments = {}
        for field in self.JsonAttributes().__dataclass_fields__:
            arguments[field] = copy.deepcopy(getattr(self._json_attrs, field), memo)
        # TODO URL handling

        # Since we excluded 'uuid' from arguments,
        # a new uid will prompt the creation of a new matching uuid.
        uid = get_new_uid()
        arguments["uid"] = uid
        if "uuid" in arguments:
            arguments["uuid"] = get_uuid_from_uid(uid)

        # Create node and init constructor attributes
        node = self.__class__(**arguments)
        # Update none constructor writable attributes.
        node._update_json_attrs_if_valid(self.JsonAttributes(**arguments))
        return node

    @property
    def json(self):
        """
        Property to obtain a simple json string.
        Calls `get_json` with default arguments.
        """
        # We cannot validate in `get_json` because we call it inside `validate`.
        # But most uses are probably the property, so we can validate the node here.
        json_string: str = self.get_json().json

        from cript.api.api import _get_global_cached_api

        api = _get_global_cached_api()
        api.schema.is_node_schema_valid(json_string, force_validation=True)

        return json_string

    def get_expanded_json(self, **kwargs) -> str:
        """
        Generates a long-form JSON representation of the current node and its hierarchy.

        The long-form JSON includes complete details of the node, eliminating the need for
         references to UUIDs to nodes stored in the CRIPT database. This comprehensive representation
         is useful for offline storage of CRIPT nodes, transferring nodes between different CRIPT instances,
         or for backup purposes.

        The generated long-form JSON can be reloaded into the SDK using
        [`cript.load_nodes_from_json()`](../../../utility_functions/#cript.nodes.util.load_nodes_from_json),
        ensuring consistency and completeness of the node data.
        However, it's important to note that this long-form JSON might not comply directly with the JSON schema
        required for POST or PATCH requests to the CRIPT API.

        Optional keyword arguments (`kwargs`) are supported and are passed directly to `json.dumps()`.
        These arguments allow customization of the JSON output, such as formatting for readability
        or pretty printing.

        Parameters
        ----------
        **kwargs : dict, optional
            Additional keyword arguments for `json.dumps()` to customize the JSON output, such as `indent`
            for pretty-printing.

        Returns
        -------
        str
            A comprehensive JSON string representing the current node and its entire hierarchy in long-form.

        Notes
        -----
        The `get_expanded_json()` method differs from the standard [`json`](./#cript.nodes.core.BaseNode.json)
        property or method, which might provide a more condensed version of the node's data.

        > For more information on condensed JSON and deserialization, please feel free to reference our discussion
        > on [deserializing Python nodes to JSON](https://github.com/C-Accel-CRIPT/Python-SDK/discussions/177)

        Examples
        --------
        >>> import cript
        >>> # ============= Create all needed nodes =============
        >>> my_project = cript.Project(name=f"my_Project")
        >>> my_collection = cript.Collection(name="my collection")
        >>> my_material_1 = cript.Material(
        ...     name="my material 1", bigsmiles = "my material 1 bigsmiles"
        ... )
        >>> my_material_2 = cript.Material(
        ...     name="my material 2", bigsmiles = "my material 2 bigsmiles"
        ... )
        >>> my_inventory = cript.Inventory(
        ...     name="my inventory", material=[my_material_1, my_material_2]
        ... )
        >>> #  ============= Assemble nodes =============
        >>> my_project.collection = [my_collection]
        >>> my_project.collection[0].inventory = [my_inventory]
        >>> #  ============= Get long form JSON =============
        >>> long_form_json = my_project.get_expanded_json(indent=4)

        ???+ info "Condensed JSON VS Expanded JSON"
            # Default Condensed JSON
            > This is the JSON when `my_project.json` is called

            ```json linenums="1"
            {
               "node":[
                  "Project"
               ],
               "uid":"_:d0d1b3c9-d552-4d4f-afd2-76f01538b87a",
               "uuid":"d0d1b3c9-d552-4d4f-afd2-76f01538b87a",
               "name":"my_Project",
               "collection":[
                  {
                     "node":[
                        "Collection"
                     ],
                     "uid":"_:07765ac8-862a-459e-9d99-d0439d6a6a09",
                     "uuid":"07765ac8-862a-459e-9d99-d0439d6a6a09",
                     "name":"my collection",
                     "inventory":[
                        {
                           "node":[
                              "Inventory"
                           ],
                           "uid":"_:4cf2bbee-3dc0-400b-8269-709f99d89d9f",
                           "uuid":"4cf2bbee-3dc0-400b-8269-709f99d89d9f",
                           "name":"my inventory",
                           "material":[
                              {
                                 "uuid":"0cf14572-4da2-43f2-8cb9-e8374086368e"
                              },
                              {
                                 "uuid":"6302a8b0-4265-4a3a-a40f-bbcbb7293046"
                              }
                           ]
                        }
                     ]
                  }
               ]
            }
            ```

            # Expanded JSON
            > This is what is created when `my_project.get_expanded_json()`

            ```json linenums="1"
            {
               "node":[
                  "Project"
               ],
               "uid":"_:afe4bb2f-fa75-4736-b692-418a5143e6f5",
               "uuid":"afe4bb2f-fa75-4736-b692-418a5143e6f5",
               "name":"my_Project",
               "collection":[
                  {
                     "node":[
                        "Collection"
                     ],
                     "uid":"_:8b5c8125-c956-472a-9d07-8cb7b402b101",
                     "uuid":"8b5c8125-c956-472a-9d07-8cb7b402b101",
                     "name":"my collection",
                     "inventory":[
                        {
                           "node":[
                              "Inventory"
                           ],
                           "uid":"_:1bd3c966-cb35-494d-85cd-3515cde570f3",
                           "uuid":"1bd3c966-cb35-494d-85cd-3515cde570f3",
                           "name":"my inventory",
                           "material":[
                              {
                                 "node":[
                                    "Material"
                                 ],
                                 "uid":"_:07bc3e4f-757f-4ac7-ae8a-7a0c68272531",
                                 "uuid":"07bc3e4f-757f-4ac7-ae8a-7a0c68272531",
                                 "name":"my material 1",
                                 "bigsmiles":"my material 1 bigsmiles"
                              },
                              {
                                 "node":[
                                    "Material"
                                 ],
                                 "uid":"_:64565687-5707-4d67-860f-5ee4a057a45f",
                                 "uuid":"64565687-5707-4d67-860f-5ee4a057a45f",
                                 "name":"my material 2",
                                 "bigsmiles":"my material 2 bigsmiles"
                              }
                           ]
                        }
                     ]
                  }
               ]
            }
            ```
        """
        return self.get_json(handled_ids=None, known_uuid=None, suppress_attributes=None, is_patch=False, condense_to_uuid={}, **kwargs).json

    def get_json(
        self,
        handled_ids: Optional[Set[str]] = None,
        known_uuid: Optional[Set[str]] = None,
        suppress_attributes: Optional[Dict[str, Set[str]]] = None,
        is_patch: bool = False,
        condense_to_uuid: Dict[str, Set[str]] = {
            "Material": {"parent_material", "component"},
            "Experiment": {"data"},
            "Inventory": {"material"},
            "Ingredient": {"material"},
            "Property": {"component"},
            "ComputationProcess": {"material"},
            "Data": {"material"},
            "Process": {"product", "waste"},
            "Project": {"member", "admin"},
            "Collection": {"member", "admin"},
        },
        **kwargs
    ):
        """
        User facing access to get the JSON of a node.
        Opposed to the also available property json this functions allows further control.
        Additionally, this function does not call `self.validate()` but the property `json` does.
        We also accept `kwargs`, that are passed on to the JSON decoding via `json.dumps()` this can be used for example to prettify the output.


        Returns named tuple with json and handled ids as result.
        """

        @dataclass(frozen=True)
        class ReturnTuple:
            json: str
            json_dict: dict
            handled_ids: set

        # Do not check for circular references, since we handle them manually
        kwargs["check_circular"] = kwargs.get("check_circular", False)

        # Delayed import to avoid circular imports
        from cript.nodes.util import NodeEncoder

        if handled_ids is None:
            handled_ids = set()
        previous_handled_nodes = copy.deepcopy(NodeEncoder.handled_ids)
        NodeEncoder.handled_ids = handled_ids

        # Similar to uid, we handle pre-saved known uuid such that they are UUID edges only
        if known_uuid is None:
            known_uuid = set()
        previous_known_uuid = copy.deepcopy(NodeEncoder.known_uuid)
        NodeEncoder.known_uuid = known_uuid
        previous_suppress_attributes = copy.deepcopy(NodeEncoder.suppress_attributes)
        NodeEncoder.suppress_attributes = suppress_attributes
        previous_condense_to_uuid = copy.deepcopy(NodeEncoder.condense_to_uuid)
        NodeEncoder.condense_to_uuid = condense_to_uuid

        try:
            tmp_json = json.dumps(self, cls=NodeEncoder, **kwargs)
            tmp_dict = json.loads(tmp_json)
            if is_patch:
                del tmp_dict["uuid"]  # patches do not allow UUID is the parent most node

            return ReturnTuple(json.dumps(tmp_dict, **kwargs), tmp_dict, NodeEncoder.handled_ids)
        except Exception as exc:
            # TODO this handling that doesn't tell the user what happened and how they can fix it
            #   this just tells the user that something is wrong
            #   this should be improved to tell the user what went wrong and where
            raise CRIPTJsonSerializationError(str(type(self)), str(self._json_attrs)) from exc
        finally:
            NodeEncoder.handled_ids = previous_handled_nodes
            NodeEncoder.known_uuid = previous_known_uuid
            NodeEncoder.suppress_attributes = previous_suppress_attributes
            NodeEncoder.condense_to_uuid = previous_condense_to_uuid

    def find_children(self, search_attr: dict, search_depth: int = -1, handled_nodes: Optional[List] = None) -> List:
        """
        Finds all the children in a given tree of nodes (specified by its root),
        that match the criteria of search_attr.
        If a node is present multiple times in the graph, it is only once in the search results.

        Parameters
        ----------
        search_attr: dict
            What you are searching for within the JSON.
            Dictionary that specifies which JSON attributes have to be present in a given node.
            If an attribute is a list, it is sufficient if the specified attributes are in the list,
            if others are present too, that does not exclude the child.
        search_depth: int default -1
            Max depth of the search into the tree. Helpful if circles are expected. -1 specifies no limit
        handled_nodes: Optional[List] default None
            A list used to track nodes that have already been processed during the search.
            This parameter is primarily used internally to prevent infinite loops in cases
            where the node graph contains cycles. When a node is processed, it is added to this list.
            If a node is encountered that is already in this list, it is skipped to avoid redundant processing.
            By default, this parameter is `None`, which means that the search starts with an empty list of handled nodes.
            In most use cases, users do not need to provide this parameter, as it is managed internally by the
            method.

        Returns
        -------
        List
            list of all nodes that match the criteria found within the graph

        Examples
        --------
        >>> import cript
        >>> # ============= Create nodes =============
        >>> my_project = cript.Project(name=f"my_Project")
        >>> my_collection = cript.Collection(name="my collection")
        >>> my_material_1 = cript.Material(
        ...     name="my material 1", bigsmiles = "my material 1 bigsmiles"
        ... )
        >>> my_material_2 = cript.Material(
        ...     name="my material 2", bigsmiles = "my material 2 bigsmiles"
        ... )
        >>> my_inventory = cript.Inventory(
        ...     name="my inventory", material=[my_material_1, my_material_2]
        ... )
        >>> #  ============= Assemble nodes =============
        >>> my_project.collection = [my_collection]
        >>> my_project.collection[0].inventory = [my_inventory]
        >>> #  ============= Get list of all material nodes in project =============
        >>> all_materials_in_project: list = my_project.find_children({"node": ["Material"]})

        Notes
        -----
        The `find_children` method is versatile and can be used to search for nodes based on various criteria.
        Here are some examples to illustrate its usage:

        * Searching for Specific Node Types:
          `search_attr = {"node": ["Parameter"]}` will find all nodes of type "Parameter".
        * Searching with Additional Attributes:
          `search_attr = {"node": ["Algorithm"], "parameter": {"name" : "update_frequency"}}`
          will locate "Algorithm" nodes containing a parameter named "update_frequency".
          Note: For list attributes, a match occurs if the specified attribute is part of the list.
            * Alternate notation: `{"node": ["Algorithm"], "parameter": [{"name" : "update_frequency"}]}`.
          In this case, nodes with additional parameters are also included.
        * Combining Multiple Search Criteria:
          ```python
          search_attr = {
              "node": ["Algorithm"],
              "parameter": [{"name": "update_frequency"}, {"name": "cutoff_distance"}]
          }
          ```
          This finds all "Algorithm" nodes with both "update_frequency" and "cutoff_distance" parameters.

        The `search_depth` parameter controls how deep the search goes into the node tree.
        A value of `-1` indicates no depth limit.
        The method effectively handles cycles in the graph by ensuring each node is processed only once.
        This makes the function suitable for complex node structures.
        """

        def is_attr_present(node: BaseNode, key, value):
            """
            Helper function that checks if an attribute is present in a node.
            """
            try:
                attr_key = getattr(node._json_attrs, key)
            except AttributeError:
                return False

            # To save code paths, I convert non-lists into lists with one element.
            if not isinstance(attr_key, list):
                attr_key = [attr_key]
            if not isinstance(value, list):
                value = [value]

            # The definition of search is, that all values in a list have to be present.
            # To fulfill this AND condition, we count the number of occurrences of that value condition
            number_values_found = 0
            # Runtime contribution: O(m), where is is the number of search keys
            for v in value:
                # Test for simple values (not-nodes)
                if v in attr_key:
                    number_values_found += 1

                # Test if value is present in one of the specified attributes (OR condition)
                # Runtime contribution: O(m), where m is the number of nodes in the attribute list.
                for attr in attr_key:
                    # if the attribute is a node and the search value is a dictionary,
                    # we can verify that this condition is met if it finds the node itself with `find_children`.
                    if isinstance(attr, BaseNode) and isinstance(v, dict):
                        # Since we only want to test the node itself and not any of its children, we set recursion to 0.
                        # Runtime contribution: recursive call, with depth search depth of the search dictionary O(h)
                        if len(attr.find_children(v, 0)) > 0:
                            number_values_found += 1
                            # Since this an OR condition, we abort early.
                            # This also doesn't inflate the number_values_count,
                            # since every OR condition should only add a max of 1.
                            break
            # Check if the AND condition of the values is met
            return number_values_found == len(value)

        if handled_nodes is None:
            handled_nodes = []

        found_children = []

        node_iterator = NodeIterator(self, search_depth)
        for node in node_iterator:
            found_attr = 0
            for key, value in search_attr.items():
                if is_attr_present(node, key, value):
                    found_attr += 1
            # If exactly all attributes are found, it matches the search criterion
            if found_attr == len(search_attr):
                found_children += [node]

        return found_children

    def remove_child(self, child) -> bool:
        """
        This safely removes the first found child node from the parent.
        This requires exact node as we test with `is` instead of `==`.

        returns True if child was found and deleted, False if child not found,
        raise DB schema exception if deletion violates DB schema.
        """

        # If we delete a child, we have to replace that with a default value.
        # The easiest way to access this default value is to get it from the the default JsonAttribute of that class
        default_json_attrs = self.JsonAttributes()
        new_attrs = self._json_attrs
        for field in self._json_attrs.__dataclass_fields__:
            value = getattr(self._json_attrs, field)
            if value is child:
                new_attrs = replace(new_attrs, **{field: getattr(default_json_attrs, field)})
                # We only want to delete the first found child
            elif not isinstance(value, str):  # Strings are iterable, but we don't want them
                try:  # Try if we are facing a list at the moment
                    new_attr_list = [element for element in value]
                except TypeError:
                    pass  # It is OK if this field is not a list
                else:
                    found_child = False
                    for i, list_value in enumerate(value):
                        if list_value is child:
                            found_child = True
                            del new_attr_list[i]
                            # Only delete first child.
                            # Important to break loop here, since value and new_attr_list are not identical any more.
                    if found_child:
                        new_attrs = replace(new_attrs, **{field: new_attr_list})  # type: ignore
                        # Again only first found place is removed
                        break
        # Let's see if we found the child aka the new_attrs are different than the old ones
        if new_attrs is self._json_attrs:
            return False
        self._update_json_attrs_if_valid(new_attrs)
        return True
