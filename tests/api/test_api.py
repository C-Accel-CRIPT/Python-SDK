import cript
import pytest


@pytest.fixture(scope="session")
def cript_api():
    """
    create api for the rest of the tests to use
    """
    host = "http://development.api.criptapp.org/"
    token = "123456"

    return cript.API(host, token)


def test_get_db_schema(cript_api):
    cript_api._get_db_schema()


def search_material_by_url(cript_api):
    pass
