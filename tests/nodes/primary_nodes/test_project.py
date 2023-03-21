import cript
import pytest


@pytest.fixture(scope="session")
def cript_api():
    """
    creates an CRIPT API object, used for
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


def test_creating_project():
    """
    create a project node and then save the project node
    test if a project node can be properly created
    """
    pass


def test_project_to_json():
    """
    test a project node can be correctly converted to JSON form
    """
    pass


def test_project_from_json():
    """
    tests a project node from be created from JSON
    """
    pass


def test_getters_and_setters():
    """
    tests that all getters and setters are working correctly
    1. gets the attributes from the project node
    2. sets all the attributes
    3. gets all the attributes again to be sure they have been set correctly
    """
    pass
