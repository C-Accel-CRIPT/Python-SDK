from dataclasses import dataclass, replace
from typing import Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.reference import Reference


class Citation(BaseNode):
    """
    ## Definition
    [Citation](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=27)

    ## Attributes
    | attribute  | type        | example                     | description                                | required | vocab |
    |------------|-------------|-----------------------------|--------------------------------------------|----------|-------|
    | url        | str         |                             | unique ID of the node                      | True     |       |
    | username   | str         | john_doe                    | User’s name                                | True     |       |
    | email      | str         | user@cript.com              | email of the user                          | True     |       |
    | orcid      | str         | 0000-0000-0000-0000         | ORCID ID of the user                       | True     |       |
    | groups     | list[Group] |                             | groups you belong to                       |          |       |
    | updated_at | datetime*   | 2022-06-04T08:24:12.311266Z | last date the node was modified (UTC time) | True     |       |
    | created_at | datetime*   | 2022-02-03T06:14:22.610253Z | date it was created (UTC time)             | True     |       |
        
    ## Available Subobjects
    *
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        type: str = ""
        reference: Union[Reference, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, type: str, reference: Reference, **kwargs):
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, type=type, reference=reference)
        self.validate()

    @property
    def type(self) -> str:
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def reference(self) -> str:
        return self._json_attrs.reference

    @reference.setter
    def reference(self, new_reference: str):
        new_attrs = replace(self._json_attrs, reference=new_reference)
        self._update_json_attrs_if_valid(new_attrs)
