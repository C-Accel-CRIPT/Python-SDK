from pprint import pprint

import pytest

import cript
from cript.api.exceptions import InvalidVocabularyCategory, InvalidVocabulary


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
    return cript.API("http://development.api.mycriptapp.org/", "123456789")


def test_create_api(cript_api: cript.API) -> None:
    """
    tests that an API object can be successfully created with host and token
    """
    api = cript.API("http://development.api.mycriptapp.org/", "123456789")

    # assertions
    assert api is not None
    assert isinstance(api, cript.API)


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
    assert len(db_schema) == total_fields_in_db_schema


def test_get_controlled_vocabulary_from_api(cript_api: cript.API) -> None:
    """
    checks if it can successfully get the controlled vocabulary list from CRIPT API
    """
    number_of_vocab_categories = 26
    vocab = cript_api.get_vocab()

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
    assert cript_api.is_vocab_valid(vocab_category="algorithm_key", vocab_word="+my_custom_key") is True

    # valid vocab category and valid word
    assert cript_api.is_vocab_valid(vocab_category="file_type", vocab_word="calibration") is True
    assert cript_api.is_vocab_valid(vocab_category="quantity_key", vocab_word="mass") is True
    assert cript_api.is_vocab_valid(vocab_category="uncertainty_type", vocab_word="fwhm") is True

    # # invalid vocab category but valid word
    with pytest.raises(InvalidVocabularyCategory):
        cript_api.is_vocab_valid(vocab_category="some_invalid_vocab_category", vocab_word="calibration")

    # valid vocab category but invalid vocab word
    with pytest.raises(InvalidVocabulary):
        cript_api.is_vocab_valid(vocab_category="file_type", vocab_word="some_invalid_word")

    # invalid vocab category and invalid vocab word
    with pytest.raises(InvalidVocabularyCategory):
        cript_api.is_vocab_valid(vocab_category="some_invalid_vocab_category", vocab_word="some_invalid_word")


def test_get_db_schema_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the db schema from API
    """
    db_schema = cript_api._get_db_schema()

    assert bool(db_schema)
    assert isinstance(db_schema, dict)

    total_fields_in_db_schema = 69
    assert len(db_schema) == total_fields_in_db_schema


def test_is_node_schema_valid(cript_api: cript.API) -> None:
    """
    test that a CRIPT node can be correctly validated and invalidated with the db schema
    """
    # valid node schema

    # invalid node schema
    # with pytest.raises(CRIPTNodeSchemaError):
    pass


def test_api_save_material(cript_api: cript.API) -> None:
    """
    Tests if API object can successfully save a node
    """
    pass


def test_api_search_material_by_uuid(cript_api: cript.API) -> None:
    """
    tests if the api can get a node via its UUID
    """
    pass


def test_api_search_material_by_url(cript_api: cript.API) -> None:
    """
    Tests if the api can get the node it saved previously from the backend.
    Tests search function directly, and indirectly tests if the material
    that was already saved is actually saved and can be gotten
    """
    pass


def test_api_material_exact_search(cript_api: cript.API) -> None:
    """
    test if a material can be successfully gotten via its name
    """
    pass


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
