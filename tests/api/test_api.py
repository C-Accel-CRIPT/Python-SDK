from pprint import pprint

import pytest

import cript


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


def test_api_context(cript_api: cript.API) -> None:
    assert cript.api.api._global_cached_api is not None
    assert cript.api.api._get_global_cached_api() is not None


def test_api_http_warning(cript_api: cript.API) -> None:
    """
    testing that the API class throws a warning if the host is `http` instead of `https`
    """
    pass


def test_get_db_schema_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the db schema from API
    """
    pass


def test_get_controlled_vocabulary_from_api(cript_api: cript.API) -> None:
    """
    checks if it can successfully get the controlled vocabulary list from CRIPT API
    """
    vocab = cript_api._get_and_set_vocab()


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
