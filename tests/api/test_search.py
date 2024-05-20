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
    materials_paginator.limit_node_fetches(15)
    materials_list = []
    while True:
        try:
            try:
                material_node = next(materials_paginator)
                materials_list += [material_node]
            except cript.CRIPTException:
                materials_paginator.auto_load_nodes = False
                material_json = next(materials_paginator)
                materials_list.append(material_json)
            finally:
                materials_paginator.auto_load_nodes = True
        except StopIteration:
            break

    # Assure that we paginated more then one page
    assert len(materials_list) == 15
    first_page_first_result = materials_list[0]["name"]
    assert first_page_first_result

    materials_paginator2 = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.NODE_TYPE)
    materials_paginator2.limit_node_fetches(21)
    uuid_list = []
    for mat in materials_list:
        try:
            uuid = mat.uuid
        except AttributeError:
            uuid = mat["uuid"]
        uuid_list.append(uuid)

    materials_paginator2.start_after_uuid(uuid_list[-1])
    materials_paginator2.auto_load_nodes = False

    for i, mat in enumerate(materials_paginator2):
        if mat["uuid"] in uuid_list:
            print(mat["uuid"])

        assert mat["uuid"] not in uuid_list
        assert i < 21


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_contains_name(cript_api: cript.API) -> None:
    """
    tests that it can correctly search with contains name mode
    searches for a material that contains the name "polystyrene"
    """
    query = "act"
    contains_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.CONTAINS_NAME, value_to_search=query)

    contains_name_paginator.auto_load_nodes = False
    assert isinstance(contains_name_paginator, Paginator)
    contains_name_list = [mat["name"] for mat in contains_name_paginator]
    # Assure that we paginated more then one page
    assert len(contains_name_list) > 50

    for name in contains_name_list:
        assert query.upper() in name.upper()


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_exact_name(cript_api: cript.API) -> None:
    """
    tests search method with exact name search
    searches for material "Sodium polystyrene sulfonate"
    """
    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search="Sodium polystyrene sulfonate")

    assert isinstance(exact_name_paginator, Paginator)
    exact_name_paginator.auto_load_nodes = False
    exact_name_list = list(exact_name_paginator)
    assert len(exact_name_list) == 1
    assert exact_name_list[0]["name"] == "Sodium polystyrene sulfonate"


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

    uuid_paginator.auto_load_nodes = False
    assert isinstance(uuid_paginator, Paginator)
    uuid_list = list(uuid_paginator)
    assert len(uuid_list) == 1
    assert uuid_list[0]["name"] == dynamic_material_data["name"]
    assert uuid_list[0]["uuid"] == dynamic_material_data["uuid"]


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_empty_paginator(cript_api: cript.API) -> None:
    non_existent_name = "This is an nonsensical name for a material and should never exist. %^&*()_"
    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=non_existent_name)
    with pytest.raises(StopIteration):
        next(exact_name_paginator)
    exact_name_paginator.auto_load_nodes = False
    with pytest.raises(StopIteration):
        next(exact_name_paginator)

    # Special 0 UUID should not exist
    uuid_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.UUID, value_to_search="00000000-0000-0000-0000-000000000000")
    with pytest.raises(StopIteration):
        next(uuid_paginator)
    exact_name_paginator.auto_load_nodes = False
    with pytest.raises(StopIteration):
        next(uuid_paginator)


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

    bigsmiles_paginator.limit_node_fetches(15)

    bigsmiles_paginator.auto_load_nodes = False
    assert isinstance(bigsmiles_paginator, Paginator)
    bigsmiles_list = list(bigsmiles_paginator)
    assert len(bigsmiles_list) == 15
    uuid_list = [mat["uuid"] for mat in bigsmiles_list]
    # Check that we don't have duplicates

    for uuid in uuid_list:
        print(uuid, bigsmiles_paginator.get_bigsmiles_search_score(uuid), uuid_list.count(uuid))

    # Enable duplicate test
    # assert len(set(uuid_list)) == len(uuid_list)
