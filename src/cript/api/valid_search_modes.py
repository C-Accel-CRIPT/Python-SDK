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
        search materials by bigsmiles.

    Examples
    -------
    >>> import cript
    >>> # search by node type
    >>> materials_paginator = api.search(
    ...     node_type=cript.Material,
    ...     search_mode=cript.SearchModes.NODE_TYPE,
    ...     value_to_search=None,
    ... )   # doctest: +SKIP

    For more details and code examples,
    please check the [cript.API.search( ) method](../api/#cript.api.api.API.search)
    """

    NODE_TYPE: str = ""
    EXACT_NAME: str = "exact_name"
    CONTAINS_NAME: str = "contains_name"
    UUID: str = "uuid"
    # UUID_CHILDREN = "uuid_children"
    BIGSMILES: str = "bigsmiles"
