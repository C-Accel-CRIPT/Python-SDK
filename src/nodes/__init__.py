from abc import ABC
from dataclasses import dataclass, asdict, replace

class BaseNode(ABC):
    @dataclass(frozen=True)
    class JsonAttributes:
        node: str = ""
    _json_attrs: JsonAttributes

    def __init__(self, node:str):
        self._json_attrs = replace(self._json_attrs, node=node)

    def __str__(self) -> str:
        """
        Return a string representation of the node.

        Returns
        -------
        str
            A string representation of the node's common attributes.
        """
        return str(asdict(self._json_attrs))
