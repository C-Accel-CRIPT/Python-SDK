import pytest

from cript import Computation


@pytest.fixture(scope="session")
def computation_node() -> Computation:
    """
    test just to see if a Computation node can be made without any issues
    with just the required arguments

    Notes
    -----
    this object is later used for other test

    Returns
    -------
    Computation
    """
    pass


def test_computation_type_invalid_vocabulary() -> None:
    """
    tests that setting the Computation type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_computation_getters_and_setters() -> None:
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


def test_serialize_computation_to_json() -> None:
    """
    tests that it can correctly turn the computation node into its equivalent JSON
    """
    pass


# ---------- Integration tests ----------


def test_save_computation_to_api() -> None:
    """
    tests if the computation node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_computation_from_api() -> None:
    """
    integration test: gets the computation node from the api that was saved prior
    """
    pass


def test_serialize_json_to_computation() -> None:
    """
    tests that a JSON of a computation node can be correctly converted to python object
    """
    pass


def test_update_computation_in_api() -> None:
    """
    tests that the computation node can be correctly updated within the API
    """
    pass


def test_delete_computation_from_api() -> None:
    """
    integration test: tests that the computation node can be deleted correctly from the API
    tries to get the computation from API, and it is expected for the API to give an error response
    """
    pass
