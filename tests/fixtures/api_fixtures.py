import pytest

import cript


@pytest.fixture
def sodium_polystyrene_uuid(cript_api: cript.API) -> str:
    """
    Get the UUID of the material, "Sodium polystyrene sulfonate" based on its EXACT_NAME from the API.

    This fixture uses the `cript.API.search`
    method to fetch the material and extract its UUID.

    This can be particularly useful in testing scenarios where you need to perform actions based on the
    material's UUID without directly knowing it since the same material will have different UUID
    within different server environments such as production, staging, and development.
    """
    material_name = "Sodium polystyrene sulfonate"

    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=material_name)

    return exact_name_paginator.current_page_results[0]["uuid"]
