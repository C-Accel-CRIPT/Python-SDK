import uuid
from dataclasses import dataclass, replace

from cript.nodes.core import BaseNode, get_uuid_from_uid


class Software(BaseNode):
    """
    Software node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        name: str = ""
        version: str = ""
        source: str = ""
        uuid: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, version: str, source: str = "", **kwargs):
        super().__init__()
        # Resepect uuid if passed as argument, otherwise construct uuid from uid
        uuid = kwargs.get("uuid", get_uuid_from_uid(self.uid))

        self._json_attrs = replace(self._json_attrs, name=name, version=version, source=source, uuid=uuid)
        self.validate()

    @property
    def uuid(self) -> uuid.UUID:
        return uuid.UUID(self._json_attrs.uuid)

    @property
    def url(self):
        from cript.api.api import _API_VERSION_STRING, _get_global_cached_api

        api = _get_global_cached_api()
        return f"{api.host}/api/{_API_VERSION_STRING}/{self.uuid}"

    @property
    def name(self) -> str:
        return self._json_attrs.name

    @name.setter
    def name(self, new_name: str):
        new_attr = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attr)

    @property
    def version(self) -> str:
        return self._json_attrs.version

    @version.setter
    def version(self, new_version: str):
        new_attr = replace(self._json_attrs, version=new_version)
        self._update_json_attrs_if_valid(new_attr)

    @property
    def source(self) -> str:
        return self._json_attrs.source

    @source.setter
    def source(self, new_source: str):
        new_attr = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attr)
