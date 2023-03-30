import pytest

from cript import Reference


def test_create_complex_reference_node() -> None:
    """
    tests that a complex reference node with all optional parameters can be made
    """
    pass


@pytest.fixture(scope="session")
def reference_node() -> Reference:
    """
    test just to see if a reference object can be made without any issues
    with just the required arguments

    Notes
    -----
    this object is later used for other test

    Returns
    -------
    Reference
    """
    pass


def test_reference_getters_and_setters() -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the reference type to correct vocabulary

    Returns
    -------
    None
    """
    pass


def test_serialize_reference_to_json() -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """
    pass


# ---------- Integration tests ----------
def test_save_reference_to_api() -> None:
    """
    tests if the reference node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_reference_from_api() -> None:
    """
    integration test: gets the reference node from the api that was saved prior
    """
    pass


def test_serialize_json_to_data() -> None:
    """
    tests that a JSON of a reference node can be correctly converted to python object
    """
    pass


def test_update_data_in_api() -> None:
    """
    reference nodes are immutable
    attempting to update a reference node should return an error from the API
    """
    pass


def test_delete_reference_from_api() -> None:
    """
    reference nodes are immutable, attempting to delete a reference node should return an error from the API
    """
    pass


def test_reference_url() -> None:
    """
    tests that the reference URL is correctly made using the UUID

    Returns
    -------
    None
    """
    pass
