import pytest

import cript


@pytest.fixture(scope="session")
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """
    host: str = "http://development.api.criptapp.org/"
    token: str = "123456" * 9

    assert cript.api.api._global_cached_api is None
    with cript.API(host, token) as api:
        yield api
    assert cript.api.api._global_cached_api is None


def test_api_context(cript_api):
    assert cript.api.api._global_cached_api is not None
    assert cript.api.api._get_global_cached_api() is not None


def test_api_save_material(cript_api):
    """
    Tests if API object can successfully save a node

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_api_search_material_by_url(cript_api):
    """
    Tests if the api can get the node it saved previously from the backend.
    Tests search function directly, and indirectly tests if the material
    that was already saved is actually saved and can be gotten

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_api_update_material(cript_api):
    """
    Tests if the API can get a material and then update it and save it in the database,
    and after save it gets the material again and checks if the update was done successfully.

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_api_delete_material(cript_api):
    """
    Tests if API can successfully delete a material.
    After deleting it from the backend, it tries to get it, and it should not be able to

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass
