import uuid
from abc import ABC
from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional

from beartype import beartype

from cript.nodes.core import BaseNode
from cript.nodes.exceptions import CRIPTUUIDException
from cript.nodes.node_iterator import NodeIterator


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

        uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
        updated_by: Any = None
        created_by: Any = None
        created_at: str = ""
        updated_at: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __new__(cls, *args, **kwargs):
        uuid: Optional[str] = str(kwargs.get("uuid"))
        if uuid and uuid in UUIDBaseNode._uuid_cache:
            existing_node_to_overwrite = UUIDBaseNode._uuid_cache[uuid]
            if type(existing_node_to_overwrite) is not cls:
                raise CRIPTUUIDException(uuid, type(existing_node_to_overwrite), cls)
            return existing_node_to_overwrite
        new_uuid_node = super().__new__(cls)
        return new_uuid_node

    def __init__(self, **kwargs):
        from cript.nodes.util.core import get_uuid_from_uid

        # initialize Base class with node
        super().__init__(**kwargs)
        # Respect uuid if passed as argument, otherwise construct uuid from uid
        uuid: str = kwargs.get("uuid", get_uuid_from_uid(self.uid))
        # replace name and notes within PrimaryBase
        self._json_attrs = replace(self._json_attrs, uuid=uuid)
        UUIDBaseNode._uuid_cache[uuid] = self

    @property
    @beartype
    def uuid(self) -> str:
        if not isinstance(self._json_attrs.uuid, str):
            # Some JSON decoding automatically converted this to UUID objects, which we don't want
            self._json_attrs = replace(self._json_attrs, uuid=str(self._json_attrs.uuid))

        return self._json_attrs.uuid

    @property
    def url(self):
        from cript.api.api import _get_global_cached_api

        api = _get_global_cached_api()
        return f"{api.host}/{api.api_prefix}/{api.api_version}/{self.uuid}"

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

    def __iter__(self) -> NodeIterator:
        """Enables DFS iteration over all children."""
        return NodeIterator(self)
