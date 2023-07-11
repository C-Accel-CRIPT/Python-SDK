import uuid
from abc import ABC
from dataclasses import dataclass, replace
from typing import Any, Dict

from cript.nodes.core import BaseNode


def get_uuid_from_uid(uid):
    return str(uuid.UUID(uid[2:]))


class UUIDBaseNode(BaseNode, ABC):
    """
    Base node that handles UUIDs and URLs.
    """

    # Class attribute that caches all nodes created
    _uuid_cache: Dict = {}

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        All shared attributes between all Primary nodes and set to their default values
        """

        uuid: str = ""
        updated_by: Any = None
        created_by: Any = None
        created_at: str = ""
        updated_at: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, **kwargs):
        # initialize Base class with node
        super().__init__(**kwargs)
        # Respect uuid if passed as argument, otherwise construct uuid from uid
        uuid = kwargs.get("uuid", get_uuid_from_uid(self.uid))
        # replace name and notes within PrimaryBase
        self._json_attrs = replace(self._json_attrs, uuid=uuid)

        # Place successfully created node in the UUID cache
        self._uuid_cache[uuid] = self

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

    @property
    def updated_by(self):
        return self._json_attrs.updated_by

    @property
    def created_by(self):
        return self._json_attrs.created_by

    @property
    def updated_at(self):
        return self._json_attrs.updated_at

    @property
    def created_at(self):
        return self._json_attrs.created_at
