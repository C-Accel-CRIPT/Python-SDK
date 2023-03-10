import json

from .primary_nodes.primary_base_node import PrimaryBaseNode


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PrimaryBaseNode):
            return obj._json_attrs
        return json.JSONEncoder.default(self, obj)
