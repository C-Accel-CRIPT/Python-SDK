import pytest

from cript import Data


@pytest.fixture(scope="session")
def data_object() -> Data:
    """
    test just to see if a data object can be made without any issues
    with just the required arguments

    Notes
    -----
    this object is later used for other test

    Returns
    -------
    Data
    """
    pass


def test_data_type_invalid_vocabulary() -> None:
    """
    tests that setting the data type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_data_getters_and_setters() -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the data type to correct vocabulary

    Returns
    -------
    None
    """
    pass


def test_serialize_data_to_json() -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """
    pass


# ---------- Integration tests ----------
def test_save_data_to_api() -> None:
    """
    tests if the data node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_data_from_api() -> None:
    """
    integration test: gets the data node from the api that was saved prior
    """
    pass


def test_serialize_json_to_data() -> None:
    """
    tests that a JSON of a data node can be correctly converted to python object
    """
    pass


def test_update_data_in_api() -> None:
    """
    tests that the data node can be correctly updated within the API
    """
    pass


def test_delete_data_from_api() -> None:
    """
    integration test: tests that the data node can be deleted correctly from the API
    tries to get the data from API, and it is expected for the API to give an error response
    """
    pass
