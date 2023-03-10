import dataclasses
from abc import ABC
from dataclasses import dataclass
from typing import Union

from src.nodes.supporting_nodes.user import User


class PrimaryBaseNode(ABC):
    """
    Abstract class that defines what it means to be a PrimaryNode,
    and other primary nodes can inherit from.
    """

    @dataclass(frozen=True)
    class BaseNodeAttributes:
        """
        All shared attributes between all Primary nodes and set to their default values
        """
        url: Union[str, None] = None
        uid: Union[str, None] = None
        locked: bool = False
        model_version: str = ""
        updated_by: User = None
        created_by: User = None
        public: bool = False
        name: str = ""
        notes: str = ""

    def __str__(self) -> str:
        """
        Return a string representation of a primary node dataclass attributes.
        Every node that inherits from this class should overwrite it to best fit
        their use case, but this provides a nice default value just in case

        Returns
        -------
        str
            A string representation of the primary node common attributes.
        """
        attrs_dict = {f.name: getattr(self.BaseNodeAttributes, f.name) for f in
                      dataclasses.fields(self.BaseNodeAttributes)}
        return str(attrs_dict)
