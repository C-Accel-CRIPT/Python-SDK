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
