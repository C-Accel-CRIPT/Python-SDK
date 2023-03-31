import copy
import json
from abc import ABC
from dataclasses import asdict, dataclass, replace
from typing import List

from cript.nodes.exceptions import CRIPTJsonSerializationError


class BaseNode(ABC):
    """
    This abstract class is the base of all CRIPT nodes.
    It offers access to a json attribute class,
    which reflects the data model JSON attributes.
    Also, some basic shared functionality is provided by this base class.
    """

    @dataclass(frozen=True)
    class JsonAttributes:
        node: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, node):
        self._json_attrs = replace(self._json_attrs, node=node)

    def __str__(self) -> str:
        """
        Return a string representation of a node data model attributes.

        Returns
        -------
        str
            A string representation of the node.
        """
        return str(asdict(self._json_attrs))

    def _update_json_attrs_if_valid(self, new_json_attr: JsonAttributes):
        tmp_obj = copy.copy(self)
        tmp_obj._json_attrs = new_json_attr
        # Throws invalid exception before object is modified.
        tmp_obj.validate()
        # After validation we can assign the attributes to actual object
        self._json_attrs = new_json_attr

    def validate(self) -> None:
        """
        Validate this node (and all its children) against the schema provided by the data bank.

        Raises:
        -------
        Exception with more error information.
        """

        pass

    @classmethod
    def _from_json(cls, json: dict):
        # Child nodes can inherit and overwrite this.
        # They should call super()._from_json first, and modified the returned object after if necessary.
        # This creates a basic version of the intended node.
        # All attributes from the backend are passed over, but some like created_by are ignored
        node = cls(**json)
        # Now we push the full json attributes into the class if it is valid

        valid_keyword_dict = {}
        reference_nodes = asdict(node._json_attrs)
        for key in reference_nodes:
            if key in json:
                valid_keyword_dict[key] = json[key]

        attrs = cls.JsonAttributes(**valid_keyword_dict)
        node._update_json_attrs_if_valid(attrs)
        return node

    @property
    def json(self):
        """
        User facing access to get the JSON of a node.
        """
        # Delayed import to avoid circular imports
        from cript.nodes.util import NodeEncoder

        try:
            self.validate()
            return json.dumps(self, cls=NodeEncoder, sort_keys=True)
        except Exception as exc:
            raise CRIPTJsonSerializationError(str(type(self)), self._json_attrs) from exc

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

           Example: search_attr = `{"node": "Parameter"}` finds all "Parameter" nodes.
                    search_attr = `{"node": "Algorithm", "parameter": {"name" : "update_frequency"}}`
                                           finds all "Algorithm" nodes, that have a parameter "update_frequency".
                                           Since parameter is a list an alternative notation is
                                           ``{"node": "Algorithm", "parameter": [{"name" : "update_frequency"}]}`
                                           and Algorithms are not excluded they have more paramters.
                    search_attr = `{"node": "Algorithm", "parameter": [{"name" : "update_frequency"},
                                           {"name" : "cutoff_distance"}]}`
                                           finds all algoritms that have a parameter "update_frequency" and "cutoff_distance".

        """

        def is_attr_present(node: BaseNode, key, value):
            """
            Helper function that checks if an attribute is present in a node.
            """

            attr_key = asdict(node._json_attrs).get(key)

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
