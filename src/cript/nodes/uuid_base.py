import uuid
from abc import ABC
from dataclasses import dataclass, replace

from cript.nodes.core import BaseNode


def get_uuid_from_uid(uid):
    return str(uuid.UUID(uid[2:]))


class UUIDBaseNode(BaseNode, ABC):
    """
    Base node that handles UUIDs and URLs.
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        All shared attributes between all Primary nodes and set to their default values
        """

        uuid: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, **kwargs):
        # initialize Base class with node
        super().__init__(**kwargs)
        # Resepect uuid if passed as argument, otherwise construct uuid from uid
        uuid = kwargs.get("uuid", get_uuid_from_uid(self.uid))
        # replace name and notes within PrimaryBase
        self._json_attrs = replace(self._json_attrs, uuid=uuid)

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID(self._json_attrs.uuid)

    @property
    def url(self):
        from cript.api.api import _get_global_cached_api

        api = _get_global_cached_api()
        return f"{api.host}/{self.uuid}"

    def __deepcopy__(self, memo):
        node = super().__deepcopy__(memo)
        node._json_attrs = replace(node._json_attrs, uuid=get_uuid_from_uid(node.uid))
        return node
