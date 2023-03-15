import json
import inspect

from dataclasses import asdict
from cript.nodes.core import BaseNode
import cript.nodes


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseNode):
            return asdict(obj._json_attrs)
        return json.JSONEncoder.default(self, obj)


def _node_json_hook(node_str:str):
    """
    Internal function, used as a hook for json deserialization.
    """
    node_dict = dict(node_str)

    # Iterate over all nodes in cript to find the correct one here
    for key, pyclass in inspect.getmembers(cript.nodes, inspect.isclass):
        if BaseNode in pyclass.__bases__:
            if key == node_dict.get("node"):
                try:
                    return pyclass._from_json(node_dict)
                except Exception as exc:
                    print(f"JSON deserialization failed for Node type {key} with JSON str: {node_str}")
                    raise exc
    # Fall back
    return node_dict

def load_nodes_from_json(nodes_json:str):
    """
    User facing function, that return a node and all its children from a json input.
    """
    return json.loads(nodes_json, object_hook=_node_json_hook)
