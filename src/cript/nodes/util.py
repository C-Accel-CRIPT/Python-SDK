import inspect
import json
from dataclasses import asdict

import cript.nodes
from cript.nodes.core import BaseNode


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseNode):
            return asdict(obj._json_attrs)
        return json.JSONEncoder.default(self, obj)


def _node_json_hook(node_str: str):
    """
    Internal function, used as a hook for json deserialization.
    """
    node_dict = dict(node_str)

    # Iterate over all nodes in cript to find the correct one here
    for key, pyclass in inspect.getmembers(cript.nodes, inspect.isclass):
        if BaseNode in pyclass.__bases__:
            if key == node_dict.get("node"):
                return pyclass._from_json(node_dict)
    # Fall back
    return node_dict


def load_nodes_from_json(nodes_json: str):
    """
    User facing function, that return a node and all its children from a json input.
    """
    return json.loads(nodes_json, object_hook=_node_json_hook)
