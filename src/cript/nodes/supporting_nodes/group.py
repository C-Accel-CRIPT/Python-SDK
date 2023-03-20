from dataclasses import dataclass

from cript.nodes.core import BaseNode


class Group(BaseNode):
    """
    CRIPT Group node as described in the CRIPT data model
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        pass

    pass
