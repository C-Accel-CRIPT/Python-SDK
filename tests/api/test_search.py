import pytest

import cript
from conftest import HAS_INTEGRATION_TESTS_ENABLED
from cript.api.paginator import Paginator


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_node_type(cript_api: cript.API) -> None:
    """
    tests the api.search() method with just a node type material search

    just testing that something comes back from the server

    Notes
    -----
    * also tests that it can go to the next page and previous page
    * later this test should be expanded to test things that it should expect an error for as well.
    * test checks if there are at least 5 things in the paginator
        *  each page should have a max of 10 results and there should be close to 5k materials in db,
        * more than enough to at least have 5 in the paginator
    """
    materials_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.NODE_TYPE)

    # test search results
    assert isinstance(materials_paginator, Paginator)
    materials_list = list(materials_paginator)
    # Assure that we paginated more then one page
    assert materials_paginator._current_page_number > 0
    assert len(materials_list) > 5
    first_page_first_result = materials_list[0]["name"]
    # just checking that the word has a few characters in it
    assert len(first_page_first_result) > 3


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_contains_name(cript_api: cript.API) -> None:
    """
    tests that it can correctly search with contains name mode
    searches for a material that contains the name "poly"
    """
    contains_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.CONTAINS_NAME, value_to_search="poly")

    assert isinstance(contains_name_paginator, Paginator)
    contains_name_list = list(contains_name_paginator)
    # Assure that we paginated more then one page
    assert contains_name_paginator._current_page_number > 0
    assert len(contains_name_list) > 5

    contains_name_first_result = contains_name_list["name"]

    # just checking that the result has a few characters in it
    assert len(contains_name_first_result) > 3


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_exact_name(cript_api: cript.API) -> None:
    """
    tests search method with exact name search
    searches for material "Sodium polystyrene sulfonate"
    """
    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search="Sodium polystyrene sulfonate")

    assert isinstance(exact_name_paginator, Paginator)
    exact_name_list = list(exact_name_paginator)
    assert len(exact_name_list) == 1
    assert exact_name_paginator.current_page_results[0]["name"] == "Sodium polystyrene sulfonate"


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_uuid(cript_api: cript.API, dynamic_material_data) -> None:
    """
    tests search with UUID
    searches for `Sodium polystyrene sulfonate` material via UUID

    The test is made dynamic to work with any server environment
    1. gets the material via `exact name search` and gets the full node
    2. takes the UUID from the full node and puts it into the `UUID search`
    3. asserts everything is as expected
    """
    uuid_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.UUID, value_to_search=dynamic_material_data["uuid"])

    assert isinstance(uuid_paginator, Paginator)
    uuid_list = list(uuid_paginator)
    assert len(uuid_list) == 1
    assert uuid_paginator.current_page_results[0]["name"] == dynamic_material_data["name"]
    assert uuid_paginator.current_page_results[0]["uuid"] == dynamic_material_data["uuid"]


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_bigsmiles(cript_api: cript.API) -> None:
    """
    tests search method with bigsmiles SearchMode to see if we just get at least one match
    searches for material
    "{[][<]C(C)C(=O)O[>][<]}{[$][$]CCC(C)C[$],[$]CC(C(C)C)[$],[$]CC(C)(CC)[$][]}"

    another good example can be "{[][$]CC(C)(C(=O)OCCCC)[$][]}"
    """
    bigsmiles_search_value = "{[][<]C(C)C(=O)O[>][<]}{[$][$]CCC(C)C[$],[$]CC(C(C)C)[$],[$]CC(C)(CC)[$][]}"

    bigsmiles_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.BIGSMILES, value_to_search=bigsmiles_search_value)

    assert isinstance(bigsmiles_paginator, Paginator)
    bigsmiles_list = list(bigsmiles_paginator)
    assert len(bigsmiles_list) >= 1
