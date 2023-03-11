import json

from dataclasses import asdict
from .core import BaseNode


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseNode):
            return asdict(obj._json_attrs)
        return json.JSONEncoder.default(self, obj)
