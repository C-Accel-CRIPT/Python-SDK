import copy
import dataclasses
import json
import uuid
from abc import ABC
from dataclasses import asdict, dataclass, replace
from typing import List

from cript.nodes.exceptions import (
    CRIPTAttributeModificationError,
    CRIPTExtraJsonAttributes,
    CRIPTJsonSerializationError,
)

tolerated_extra_json = ["component_count", "computational_forcefield_count", "property_count"]


def add_tolerated_extra_json(additional_tolerated_json: str):
    """
    In case a node should be loaded from JSON (such as `getting` them from the API),
    but the API sends additional JSON attributes, these can be set to tolerated temprarily with this routine.
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

    # Prevent new attributes being set.
    # This might just be temporary, but for now, I don't want to acciditentally add new attributes, when I mean to modify one.
    def __setattr__(self, key, value):
        if not hasattr(self, key):
            raise CRIPTAttributeModificationError(self.node_type, key, value)
        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            if kwarg not in tolerated_extra_json + list(self._json_attrs.__dataclass_fields__.keys()):
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
        return str(asdict(self._json_attrs))

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

    def validate(self, api=None) -> None:
        """
        Validate this node (and all its children) against the schema provided by the data bank.

        Raises:
        -------
        Exception with more error information.
        """
        from cript.api.api import _get_global_cached_api

        if api is None:
            api = _get_global_cached_api()
        api._is_node_schema_valid(self.get_json().json)

    @classmethod
    def _from_json(cls, json_dict: dict):
        # Child nodes can inherit and overwrite this.
        # They should call super()._from_json first, and modified the returned object after if necessary
        # We create manually a dict that contains all elements from the send dict.
        # That eliminates additional fields and doesn't require asdict.
        arguments = {}
        for field in cls.JsonAttributes().__dataclass_fields__:
            if field in json_dict:
                arguments[field] = json_dict[field]

        # The call to the constructor might ignore fields that are usually not writable.
        try:
            node = cls(**arguments)
        # TODO we should not catch all exceptions if we are handling them, and instead let it fail
        #  to create a good error message that points to the correct place that it failed to make debugging easier
        except Exception as exc:
            print(cls, arguments)
            raise exc

        attrs = cls.JsonAttributes(**arguments)
        # Handle UID manually. Conserve newly assigned uid if uid is default (empty)
        if attrs.uid == cls.JsonAttributes().uid:
            attrs = replace(attrs, uid=node.uid)

        # But here we force even usually unwritable fields to be set.
        node._update_json_attrs_if_valid(attrs)
        return node

    def __deepcopy__(self, memo):
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
        self.validate()
        return self.get_json().json

    def get_json(
        self,
        handled_ids: set = None,
        condense_to_uuid={"Material": ["parent_material", "component"], "Inventory": ["material"], "Ingredient": ["material"], "Property": ["component"], "ComputatationProcess": ["material"], "Data": ["material"], "Process": ["product", "waste"]},
        **kwargs
    ):
        """
        User facing access to get the JSON of a node.
        Opposed to the also available property json this functions allows further control.
        Additionally, this function does not call `self.validate()` but the property `json` does.

        Returns named tuple with json and handled ids as result.
        """

        @dataclass(frozen=True)
        class ReturnTuple:
            json: str
            handled_ids: set

        # Do not check for circular references, since we handle them manually
        kwargs["check_circular"] = kwargs.get("check_circular", False)

        # Delayed import to avoid circular imports
        from cript.nodes.util import NodeEncoder

        previous_handled_nodes = copy.deepcopy(NodeEncoder.handled_ids)
        if handled_ids is not None:
            NodeEncoder.handled_ids = handled_ids
        previous_condense_to_uuid = copy.deepcopy(NodeEncoder.condense_to_uuid)
        NodeEncoder.condense_to_uuid = condense_to_uuid

        try:
            return ReturnTuple(json.dumps(self, cls=NodeEncoder, **kwargs), NodeEncoder.handled_ids)
        except Exception as exc:
            # TODO this handling that doesn't tell the user what happened and how they can fix it
            #   this just tells the user that something is wrong
            #   this should be improved to tell the user what went wrong and where
            raise CRIPTJsonSerializationError(str(type(self)), self._json_attrs) from exc
        finally:
            NodeEncoder.handled_ids = previous_handled_nodes
            NodeEncoder.condense_to_uuid = previous_condense_to_uuid

    def find_children(self, search_attr: dict, search_depth: int = -1, handled_nodes=None) -> List:
        """
        Finds all the children in a given tree of nodes (specified by its root),
        that match the criteria of search_attr.
        If a node is present multiple times in the graph, it is only once in the search results.

        search_dept: Max depth of the search into the tree. Helpful if circles are expected. -1 specifies no limit

        search_attr: dict
           Dictionary that specifies which JSON attributes have to be present in a given node.
           If an attribute is a list, it it is suffiecient if the specified attributes are in the list,
           if others are present too, that does not exclude the child.

           Example: search_attr = `{"node": ["Parameter"]}` finds all "Parameter" nodes.
                    search_attr = `{"node": ["Algorithm"], "parameter": {"name" : "update_frequency"}}`
                                           finds all "Algorithm" nodes, that have a parameter "update_frequency".
                                           Since parameter is a list an alternative notation is
                                           ``{"node": ["Algorithm"], "parameter": [{"name" : "update_frequency"}]}`
                                           and Algorithms are not excluded they have more paramters.
                    search_attr = `{"node": ["Algorithm"], "parameter": [{"name" : "update_frequency"},
                                           {"name" : "cutoff_distance"}]}`
                                           finds all algoritms that have a parameter "update_frequency" and "cutoff_distance".

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
            # To fulfill this AND condition, we count the number of occurences of that value condition
            number_values_found = 0
            for v in value:
                # Test for simple values (not-nodes)
                if v in attr_key:
                    number_values_found += 1

                # Test if value is present in one of the specified attributes (OR condition)
                for attr in attr_key:
                    # if the attribute is a node and the search value is a dictionary,
                    # we can verify that this condition is met if it finds the node itself with `find_children`.
                    if isinstance(attr, BaseNode) and isinstance(v, dict):
                        # Since we only want to test the node itself and not any of its children, we set recursion to 0.
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

        # Protect agains cycles in graph, by handling every instance of a node only once
        if self in handled_nodes:
            return []
        handled_nodes += [self]

        found_children = []

        # In this search we include the calling node itself.
        # We check for this node if all specified attributes are present by counting them (AND condition).
        found_attr = 0
        for key, value in search_attr.items():
            if is_attr_present(self, key, value):
                found_attr += 1
        # If exactly all attributes are found, it matches the search criterion
        if found_attr == len(search_attr):
            found_children += [self]

        # Recursion according to the recursion depth for all node children.
        if search_depth != 0:
            for field in self._json_attrs.__dataclass_fields__:
                value = getattr(self._json_attrs, field)
                # To save code paths, I convert non-lists into lists with one element.
                if not isinstance(value, list):
                    value = [value]
                for v in value:
                    try:  # Try every attribute for recursion (duck-typing)
                        found_children += v.find_children(search_attr, search_depth - 1, handled_nodes=handled_nodes)
                    except AttributeError:
                        pass
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
                        new_attrs = replace(new_attrs, **{field: new_attr_list})
                        # Again only first found place is removed
                        break
        # Let's see if we found the child aka the new_attrs are different than the old ones
        if new_attrs is self._json_attrs:
            return False
        self._update_json_attrs_if_valid(new_attrs)
        return True
