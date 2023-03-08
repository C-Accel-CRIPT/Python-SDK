from abc import ABC


class PrimaryNode(ABC):
    """
    Abstract class that defines what it means to be a PrimaryNode,
    and other primary nodes can inherit from.
    """

    def __str__(self) -> str:
        """
        Return a string representation of a primary node.

        Returns
        -------
        str: A string representation of a primary node.
        """

