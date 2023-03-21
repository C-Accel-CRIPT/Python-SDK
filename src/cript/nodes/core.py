import copy
import json
from abc import ABC
from dataclasses import asdict, dataclass, replace



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
        attrs = cls.JsonAttributes(**json)
        node._update_json_attrs_if_valid(attrs)
        return node

    @property
    def json(self):
        """
        User facing access to get the JSON of a node.
        """
        # Delayed import to avoid circular imports
        from cript.nodes.util import NodeEncoder

        return json.dumps(self, cls=NodeEncoder)

    def remove_child(self, child) -> bool:
        """
        This safely removes the first found child node from the parent.
        This requires exact node as we test with `is` instead of `==`.

        returns True if child was found and deleted, False if child not found, raise DB schema exception if deletion violates DB schema.
        """

        # If we delete a child, we have to replace that with a default value.
        # The easiest way to access this default value is to get it from the the default JsonAttribute of that class
        default_json_attrs = self.JsonAttributes()
        new_attrs = self._json_attrs
        for field in self._json_attrs.__dataclass_fields__:
            value = getattr(self._json_attrs, field)
            if value is child:
                new_attrs = replace(
                    new_attrs, **{field: getattr(default_json_attrs, field)}
                )
                # We only want to delete the first found child
            elif not isinstance(
                value, str
            ):  # Strings are iterable, but we don't want them
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
