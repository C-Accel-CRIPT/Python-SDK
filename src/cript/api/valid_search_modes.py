from enum import Enum


class SearchModes(Enum):
    """
    Available search modes to use with the CRIPT API search

    > For more details and code examples,
    > please check the [cript.API.search( ) method](../api/#cript.api.api.API.search)

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
        search materials by bigsmiles identifier.

    Examples
    -------
    >>> import cript
    >>> # search by node type
    >>> materials_paginator = api.search(
    ...     node_type=cript.Material,
    ...     search_mode=cript.SearchModes.NODE_TYPE,
    ...     value_to_search=None,
    ... )   # doctest: +SKIP
    """

    NODE_TYPE: str = ""
    EXACT_NAME: str = "exact_name"
    CONTAINS_NAME: str = "contains_name"
    UUID: str = "uuid"
    # UUID_CHILDREN = "uuid_children"
    BIGSMILES: str = "bigsmiles"


class ExactSearchModes(Enum):
    """
    Available exact search modes to use with the
    [cript.API.get_node_by_exact_match() method](../api/#cript.api.api.API.get_node_by_exact_match)
    to retrieving single nodes.

    > For more details and code examples, please review
    > [cript.API.get_node_by_exact_match() method](../api/#cript.api.api.API.get_node_by_exact_match)

    Attributes
    ----------
    UUID : str
        Search by unique node UUID.
    EXACT_NAME : str
        Search by unique exact node name.
    BIGSMILES: str
        Search materials by BigSmiles identifier for an exact match.

    Examples
    -------
    >>> import cript
    >>> # Retrieve a node by its exact UUID
    >>> my_material_node = api.get_node_by_exact_match(
    ...     node_type=cript.Material,
    ...     search_mode=cript.ExactSearchModes.UUID,
    ...     value_to_search="e1b41d34-3bf2-4cd8-9a19-6412df7e7efc"
    ... )   # doctest: +SKIP

    >>> # Retrieve a node by its exact name
    >>> my_project_node = api.get_node_by_exact_match(
    ...     node_type=cript.Material,
    ...     search_mode=cript.ExactSearchModes.EXACT_NAME,
    ...     value_to_search="Sodium polystyrene sulfonate"
    ... )  # doctest: +SKIP

    >>> # Retrieve a material by its BigSmiles identifier
    >>> my_material_node = api.get_node_by_exact_match(
    ...     node_type=cript.Material,
    ...     search_mode=cript.ExactSearchModes.BIGSMILES,
    ...     value_to_search="{[][$]CC(C)(C(=O)OCCCC)[$][]}"
    ... )  # doctest: +SKIP
    """

    UUID: str = "uuid"
    EXACT_NAME: str = "exact_name"
    BIGSMILES: str = "bigsmiles"
