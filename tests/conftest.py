import pytest

import cript


@pytest.fixture(scope="session")
def cript_api():
    """
    creates a CRIPT API object, used for integration tests for all nodes

    * saving
    * getting
    * updating
    * deleting

    Returns
    -------
    cript.API
        api object used to interact with CRIPT
    """
    return cript.API(host="https://cript.org", token="123465")
