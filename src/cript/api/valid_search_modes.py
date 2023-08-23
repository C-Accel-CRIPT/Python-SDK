from enum import Enum


class SearchModes(Enum):
    """
    Available search modes to use with the CRIPT API search

    Attributes
    ----------
    NODE_TYPE : str
        Search by node type.
    EXACT_NAME : str
        Search by exact node name.
    CONTAINS_NAME : str
        Search by node name containing a given string.
    UUID : str
        Search by node UUID.
    BIGSMILES: str
        Search materials by bigsmiles identifier.
    NODE_TYPE_WITHIN_PARENT: str
        Search for a node type within a parent.
        > Example: Find all the materials within this specific project.

    Examples
    -------
    ```python
    # search by node type
    materials_paginator = cript_api.search(
        node_type=cript.Material,
        search_mode=cript.SearchModes.NODE_TYPE,
        value_to_search=None,
    )
    ```
    """

    NODE_TYPE: str = ""
    EXACT_NAME: str = "exact_name"
    CONTAINS_NAME: str = "contains_name"
    UUID: str = "uuid"
    BIGSMILES: str = "bigsmiles"
    NODE_TYPE_WITHIN_PARENT: str = "node_type_within_parent"
