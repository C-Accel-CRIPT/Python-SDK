import cript
import pytest


@pytest.fixture(scope="session")
def cript_api():
    """
    create api for the rest of the tests to use
    """
    host = ""
    token = ""

    return cript.API(host, token)


def search_material_by_url(cript_api):
    pass
