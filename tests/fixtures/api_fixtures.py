from typing import Dict

import pytest

import cript


@pytest.fixture(scope="function")
def dynamic_material_data(cript_api: cript.API) -> Dict[str, str]:
    """
    Get the UUID and name of the material, "Sodium polystyrene sulfonate" based on its EXACT_NAME from the API.

    This fixture uses the `cript.API.search` method to fetch the material from the API.

    This can be particularly useful in testing scenarios where you need to perform actions based on the
    material's UUID without directly knowing it since the same material will have different UUID
    within different server environments such as production, staging, and development.

    Returns
    -------
    Dict[str, str]
        A dictionary containing {"uuid": uuid, "name": "Sodium polystyrene sulfonate"}.
        This provides the test with access to both the name and UUID for verification.
    """
    material_name: str = "Sodium polystyrene sulfonate"

    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=material_name)

    material = next(exact_name_paginator)
    material_uuid: str = str(material.uuid)

    return {"name": material_name, "uuid": material_uuid}
