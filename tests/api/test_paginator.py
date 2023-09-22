from typing import Dict

import cript


def test_paginator_get_node_by_name(cript_api: cript.API) -> None:
    """
    Test if the paginator can retrieve a material by name from the current page.
    """
    # Fetch all materials using the paginator
    materials_paginator = cript_api.search(
        node_type=cript.Material,
        search_mode=cript.SearchModes.NODE_TYPE,
        value_to_search=None
    )

    # Choose a random material name from the current page for testing.
    # The index 3 is arbitrary and can be changed.
    test_material_name: str = materials_paginator.current_page_results[3]["name"]

    # Attempt to retrieve the material by name using the paginator
    retrieved_material: Dict = materials_paginator.get_node_by_name(node_name=test_material_name)

    # Verify the retrieved material is a dictionary and its name matches the test material name
    assert isinstance(retrieved_material, dict)
    assert retrieved_material["name"] == test_material_name
