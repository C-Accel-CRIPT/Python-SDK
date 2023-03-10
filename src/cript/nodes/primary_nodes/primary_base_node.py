import dataclasses
from abc import ABC
from dataclasses import dataclass, asdict

from src.nodes.supporting_nodes.user import User


class PrimaryBaseNode(ABC):
    """
    Abstract class that defines what it means to be a PrimaryNode,
    and other primary nodes can inherit from.
    """

    @dataclass(frozen=True)
    class JsonAttributes:
        """
        All shared attributes between all Primary nodes and set to their default values
        """
        url: str = ""
        uid: str = ""
        locked: bool = False
        model_version: str = ""
        updated_by: User = None
        created_by: User = None
        public: bool = False
        name: str = ""
        notes: str = ""

    _json_attrs: JsonAttributes

    def __str__(self) -> str:
        """
        Return a string representation of a primary node dataclass attributes.
        Every node that inherits from this class should overwrite it to best fit
        their use case, but this provides a nice default value just in case

        Examples
        --------
        {
        'url': '',
        'uid': '',
        'locked': False,
        'model_version': '',
        'updated_by': None,
        'created_by': None,
        'public': False,
        'notes': ''
        }


        Returns
        -------
        str
            A string representation of the primary node common attributes.
        """
        return str(asdict(self._json_attrs))
