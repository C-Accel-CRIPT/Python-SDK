from abc import ABC
from dataclasses import dataclass, field
from typing import Union


class PrimaryNode(ABC):
    """
    Abstract class that defines what it means to be a PrimaryNode,
    and other primary nodes can inherit from.
    """

    @dataclass(frozen=True)
    class NodeAttributes:
        url: Union[str, None] = None
        uid: Union[str, None] = None
        locked: bool = False

    def __str__(self) -> str:
        """
        Return a string representation of a primary node.
        Every node that inherits from this class should overwrite it to best fit
        their use case, but this provides a nice default value just in case

        Returns
        -------
        str: A string representation of a primary node.
        """
