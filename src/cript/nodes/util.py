import inspect
import json
from dataclasses import asdict

import cript.nodes
from cript.nodes.core import BaseNode
from cript.nodes.exceptions import CRIPTJsonDeserializationError, CRIPTJsonNodeError


class NodeEncoder(json.JSONEncoder):
    handled_ids = set()

    def default(self, obj):
        if isinstance(obj, BaseNode):
            try:
                uid = obj.uid
            except AttributeError:
                pass
            else:
                if uid in NodeEncoder.handled_ids:
                    return {"node": obj._json_attrs.node, "uid": uid}
                NodeEncoder.handled_ids.add(uid)
            default_values = asdict(obj.JsonAttributes())
            serialize_dict = {}
            # Remove default values from serialization
            for key in default_values:
                if key in obj._json_attrs.__dataclass_fields__:
                    if getattr(obj._json_attrs, key) != default_values[key]:
                        serialize_dict[key] = getattr(obj._json_attrs, key)
            return serialize_dict
        return json.JSONEncoder.default(self, obj)


def _node_json_hook(node_str: str):
    """
    Internal function, used as a hook for json deserialization.
    """
    node_dict = dict(node_str)

    # Iterate over all nodes in cript to find the correct one here
    for key, pyclass in inspect.getmembers(cript.nodes, inspect.isclass):
        if BaseNode in inspect.getmro(pyclass):
            node_list = node_dict.get("node")
            if isinstance(node_list, list) and len(node_list) == 1 and isinstance(node_list[0], str):
                node_str = node_list[0]
            else:
                raise CRIPTJsonNodeError(node_list)

            if key == node_str:
                try:
                    return pyclass._from_json(node_dict)
                except Exception as exc:
                    raise CRIPTJsonDeserializationError(key, node_str) from exc
    # Fall back
    return node_dict


def load_nodes_from_json(nodes_json: str):
    """
    User facing function, that return a node and all its children from a json input.
    """
    return json.loads(nodes_json, object_hook=_node_json_hook)
