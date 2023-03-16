from dataclasses import dataclass, replace
from cript.nodes.core import BaseNode


class Software(BaseNode):
    """
    Software node
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Software"
        url: str = ""
        name: str = ""
        version: str = ""
        source: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()
    def __init__(self, name:str, version:str, source:str="", **kwargs):
        super().__init__(node="Software")
        self._json_attrs = replace(self._json_attrs, name=name, version=version, source=source)
        self.validate()

    @property
    def url(self) -> str:
        return self._json_attrs.url

    @property
    def name(self) -> str:
        return self._json_attrs.name
    @name.setter
    def name(self, new_name:str):
        new_attr = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attr)

    @property
    def version(self) -> str:
        return self._json_attrs.version
    @version.setter
    def version(self, new_version:str):
        new_attr = replace(self._json_attrs, version=new_version)
        self._update_json_attrs_if_valid(new_attr)

    @property
    def source(self) -> str:
        return self._json_attrs.source
    @source.setter
    def source(self, new_source:str):
        new_attr = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attr)
