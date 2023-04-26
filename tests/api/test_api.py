import json

import pytest
import requests

import cript
from cript.api.exceptions import InvalidVocabulary, InvalidVocabularyCategory
from cript.api.paginator import Paginator
from cript.nodes.exceptions import CRIPTNodeSchemaError


# TODO use the cript_api from conftest.py
@pytest.fixture(scope="session")
def cript_api() -> cript.API:
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """

    # assert cript.api.api._global_cached_api is None
    # with cript.API("http://development.api.mycriptapp.org/", "123456789") as api:
    #     yield api
    # assert cript.api.api._global_cached_api is None
    token: str = open("../../.env").read()

    return cript.API(host="http://development.api.mycriptapp.org/", token=token)


def test_create_api() -> None:
    """
    tests that an API object can be successfully created with host and token
    """
    api = cript.API("http://development.api.mycriptapp.org/", "123456789")

    # assertions
    assert api is not None
    assert isinstance(api, cript.API)


def test_api_with_invalid_host() -> None:
    """
    this mostly tests the _prepare_host() function to be sure it is working as expected
    * attempting to create an api client with invalid host appropriately throws a `CRIPTConnectionError`
    * giving a host that does not start with http such as "criptapp.org" should throw an InvalidHostError
    """
    with pytest.raises((requests.ConnectionError, cript.api.exceptions.CRIPTConnectionError)):
        cript.API("https://some_invalid_host", "123456789")

    with pytest.raises(cript.api.exceptions.InvalidHostError):
        cript.API("no_http_host.org", "123456789")


def test_prepare_host(cript_api: cript.API) -> None:
    """
    tests API _prepare_host function
    """
    host = " http://myhost.com/ "
    prepared_host = cript.api.api._prepare_host(host)

    assert prepared_host == "http://myhost.com/api/v1"


# def test_api_context(cript_api: cript.API) -> None:
#     assert cript.api.api._global_cached_api is not None
#     assert cript.api.api._get_global_cached_api() is not None


def test_get_db_schema_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the db schema from API
    """
    db_schema = cript_api._get_db_schema()

    assert bool(db_schema)
    assert isinstance(db_schema, dict)

    total_fields_in_db_schema = 69
    assert len(db_schema["$defs"]) == total_fields_in_db_schema


def test_is_node_schema_valid(cript_api: cript.API) -> None:
    """
    test that a CRIPT node can be correctly validated and invalidated with the db schema

    * test a couple of nodes to be sure db schema validation is working fine
        * material node
        * file node
    * test db schema validation with an invalid node, and it should be invalid

    Notes
    -----
    * does not test if serialization/deserialization works correctly,
    just tests if the node schema can work correctly if serialization was correct
    """

    # ------ invalid node schema------
    invalid_schema = {"invalid key": "invalid value", "node": ["Material"]}

    with pytest.raises(CRIPTNodeSchemaError):
        cript_api._is_node_schema_valid(node_json=json.dumps(invalid_schema))

    # ------ valid material schema ------
    # valid material node
    valid_material_dict = {"node": ["Material"], "name": "0.053 volume fraction CM gel", "uid": "_:0.053 volume fraction CM gel"}

    # convert dict to JSON string because method expects JSON string
    assert cript_api._is_node_schema_valid(node_json=json.dumps(valid_material_dict)) is True

    # ------ valid file schema ------
    valid_file_dict = {
        "node": ["File"],
        "source": "https://criptapp.org",
        "type": "calibration",
        "extension": ".csv",
        "data_dictionary": "my file's data dictionary",
    }

    # convert dict to JSON string because method expects JSON string
    assert cript_api._is_node_schema_valid(node_json=json.dumps(valid_file_dict)) is True


def test_get_controlled_vocabulary_from_api(cript_api: cript.API) -> None:
    """
    checks if it can successfully get the controlled vocabulary list from CRIPT API
    """
    number_of_vocab_categories = 26
    vocab = cript_api._get_vocab()

    # assertions
    # check vocabulary list is not empty
    assert bool(vocab) is True
    assert len(vocab) == number_of_vocab_categories


def test_is_vocab_valid(cript_api: cript.API) -> None:
    """
    tests if the method for vocabulary is validating and invalidating correctly

    * test with custom key to check it automatically gives valid
    * test with a few vocabulary_category and vocabulary_words
        * valid category and valid vocabulary word
    * test that invalid category throws the correct error
        * invalid category and valid vocabulary word
    * test that invalid vocabulary word throws the correct error
        * valid category and invalid vocabulary word
    tests invalid category and invalid vocabulary word
    """
    # custom vocab
    assert cript_api._is_vocab_valid(vocab_category="algorithm_key", vocab_word="+my_custom_key") is True

    # valid vocab category and valid word
    assert cript_api._is_vocab_valid(vocab_category="file_type", vocab_word="calibration") is True
    assert cript_api._is_vocab_valid(vocab_category="quantity_key", vocab_word="mass") is True
    assert cript_api._is_vocab_valid(vocab_category="uncertainty_type", vocab_word="fwhm") is True

    # # invalid vocab category but valid word
    with pytest.raises(InvalidVocabularyCategory):
        cript_api._is_vocab_valid(vocab_category="some_invalid_vocab_category", vocab_word="calibration")

    # valid vocab category but invalid vocab word
    with pytest.raises(InvalidVocabulary):
        cript_api._is_vocab_valid(vocab_category="file_type", vocab_word="some_invalid_word")

    # invalid vocab category and invalid vocab word
    with pytest.raises(InvalidVocabularyCategory):
        cript_api._is_vocab_valid(vocab_category="some_invalid_vocab_category", vocab_word="some_invalid_word")


def test_api_save_project(cript_api: cript.API, simple_project_node) -> None:
    """
    Tests if API object can successfully save a node
    """
    cript_api.save(simple_project_node)


def test_api_search_node_type(cript_api: cript.API) -> None:
    """
    tests the api.search() method with just a node type material search

    Notes
    -----
    * also tests that it can go to the next page and previous page
    * later this test should be expanded to test things that it should expect an error for as well.
    * test checks if there are at least 5 things in the paginator
        *  each page should have a max of 10 results and there should be close to 5k materials in db,
        * more than enough to at least have 5 in the paginator
    """

    materials_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.NODE_TYPE, value_to_search=None)

    # test search results
    assert isinstance(materials_paginator, Paginator)
    assert len(materials_paginator.current_page_results) > 5
    assert materials_paginator.current_page_results[0]["name"] == "(2-Chlorophenyl) 2,4-dichlorobenzoate"

    # tests that it can correctly go to the next page
    materials_paginator.next_page()
    assert len(materials_paginator.current_page_results) > 5
    assert materials_paginator.current_page_results[0]["name"] == "2,4-Dichloro-N-(1-methylbutyl)benzamide"

    # tests that it can correctly go to the previous page
    materials_paginator.previous_page()
    assert len(materials_paginator.current_page_results) > 5
    assert materials_paginator.current_page_results[0]["name"] == "(2-Chlorophenyl) 2,4-dichlorobenzoate"


def test_api_search_contains_name(cript_api: cript.API) -> None:
    """
    tests that it can correctly search with contains name mode
    searches for a material that contains the name "poly"
    """
    contains_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.CONTAINS_NAME, value_to_search="poly")

    assert isinstance(contains_name_paginator, Paginator)
    assert len(contains_name_paginator.current_page_results) > 5
    assert contains_name_paginator.current_page_results[0]["name"] == "Pilocarpine polyacrylate"


def test_api_search_exact_name(cript_api: cript.API) -> None:
    """
    tests search method with exact name search
    searches for material "Sodium polystyrene sulfonate"
    """
    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search="Sodium polystyrene sulfonate")

    assert isinstance(exact_name_paginator, Paginator)
    assert len(exact_name_paginator.current_page_results) == 1
    assert exact_name_paginator.current_page_results[0]["name"] == "Sodium polystyrene sulfonate"


def test_api_search_uuid(cript_api: cript.API) -> None:
    """
    tests search with UUID
    searches for Sodium polystyrene sulfonate material that has a UUID of "fcc6ed9d-22a8-4c21-bcc6-25a88a06c5ad"
    """
    uuid_to_search = "fcc6ed9d-22a8-4c21-bcc6-25a88a06c5ad"

    uuid_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.UUID, value_to_search=uuid_to_search)

    assert isinstance(uuid_paginator, Paginator)
    assert len(uuid_paginator.current_page_results) == 1
    assert uuid_paginator.current_page_results[0]["name"] == "Sodium polystyrene sulfonate"
    assert uuid_paginator.current_page_results[0]["uuid"] == uuid_to_search


def test_api_update_material(cript_api: cript.API) -> None:
    """
    Tests if the API can get a material and then update it and save it in the database,
    and after save it gets the material again and checks if the update was done successfully.
    """
    pass


def test_api_delete_material(cript_api: cript.API) -> None:
    """
    Tests if API can successfully delete a material.
    After deleting it from the backend, it tries to get it, and it should not be able to
    """
    pass


def test_get_my_user_node_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the user node associated with the API Token
    """
    pass


def test_get_my_group_node_from_api(cript_api: cript.API) -> None:
    """
    tests that group node that is associated with their API Token can be gotten correctly
    """
    pass


def test_get_my_projects_from_api(cript_api: cript.API) -> None:
    """
    get a page of project nodes that is associated with the API token
    """
    pass
