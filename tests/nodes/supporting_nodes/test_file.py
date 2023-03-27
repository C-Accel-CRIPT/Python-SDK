import pytest

import cript


def test_create_file() -> None:
    """
    tests that a simple file with only required attributes can be created
    """
    file_node = cript.File(source="https://google.com", type="calibration")


@pytest.fixture(scope="session")
def file_node() -> cript.File:
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
    my_file = cript.File(source="https://google.com", type="calibration")
    return my_file


def test_file_type_invalid_vocabulary() -> None:
    """
    tests that setting the file type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_file_getters_and_setters(file_node) -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the file type to correct vocabulary
    """
    # ------- new properties -------
    new_source = "https://bing.com"
    new_file_type = "computation_config"
    new_file_extension = ".csv"
    new_data_dictionary = "new data dictionary"

    # ------- set properties -------
    file_node.source = new_source
    file_node.type = new_file_type
    file_node.extension = new_file_extension
    file_node.data_dictionary = new_data_dictionary

    # ------- assert set and get properties are the same -------
    assert file_node.source == new_source
    assert file_node.type == new_file_type
    assert file_node.extension == new_file_extension
    assert file_node.data_dictionary == new_data_dictionary


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
