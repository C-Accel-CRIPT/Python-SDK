import pytest

import cript


def test_create_simple_material() -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    my_identifiers = [
        {
            "alternative_names": "my material alternative name"
        }
    ]

    my_material = cript.Material(identifiers=my_identifiers)

    assert my_material.identifiers == my_identifiers


def test_create_full_material() -> None:
    """
    tests that a material can be created with all optional arguments
    """
    my_identifier = [
        {
            "alternative_names": "my material alternative name"
        }
    ]

    my_components = [

    ]


@pytest.fixture(scope="session")
def simple_material() -> cript.Material:
    """
    tests that it can create a material node with only required arguments

    Returns
    -------
    Material
    """
    pass


def test_invalid_material_keywords() -> None:
    """
    tries to create a material with invalid keywords and expects to get an Exception
    """
    # with pytest.raises(InvalidVocabulary):
    pass


def test_all_getters_and_setters() -> None:
    """
    tests the getters and setters for the simple material object

    1. sets every possible attribute for the simple_material object
    2. gets every possible attribute for the simple_material object
    3. asserts that what was set and what was gotten are the same
    """
    pass


def test_serialize_material_to_json() -> None:
    """
    tests that it can correctly turn the material node into its equivalent JSON
    """
    pass


# ---------- Integration Tests ----------
def test_save_material_to_api() -> None:
    """
    tests if the material can be saved to the API without errors and status code of 200
    """
    pass


def test_get_material_from_api() -> None:
    """
    integration test: gets the material from the api that was saved prior
    """
    pass


def test_deserialize_material_from_json() -> None:
    """
    tests that a JSON of a material node can be correctly converted to python object
    """
    pass


def test_update_material_to_api() -> None:
    """
    tests that the material can be correctly updated within the API
    """
    pass


def test_delete_material_from_api() -> None:
    """
    integration test: tests that the material can be deleted correctly from the API
    tries to get the material from API, and it is expected for the API to give an error response
    """
    pass
