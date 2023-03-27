import pytest

from cript import File


@pytest.fixture(scope="session")
def file_object() -> File:
    """
    test just to see if a file object can be made without any issues
    with just the required arguments

    Notes
    -----
    this object is later used for other test

    Returns
    -------
    File
    """
    pass


def test_file_type_invalid_vocabulary() -> None:
    """
    tests that setting the file type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_file_getters_and_setters() -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the file type to correct vocabulary

    Returns
    -------
    None
    """
    pass


def test_serialize_file_to_json() -> None:
    """
    tests that it can correctly turn the file node into its equivalent JSON
    """
    pass


# ---------- Integration tests ----------
def test_save_file_to_api() -> None:
    """
    tests if the file node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_file_from_api() -> None:
    """
    integration test: gets the file node from the api that was saved prior
    """
    pass


def test_serialize_json_to_file() -> None:
    """
    tests that a JSON of a file node can be correctly converted to python object
    """
    pass


def test_update_file_in_api() -> None:
    """
    tests that the file node can be correctly updated within the API
    """
    pass


def test_delete_file_from_api() -> None:
    """
    integration test: tests that the file node can be deleted correctly from the API
    tries to get the file from API, and it is expected for the API to give an error response
    """
    pass
