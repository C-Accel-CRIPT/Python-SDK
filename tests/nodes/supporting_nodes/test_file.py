import copy
import json

import pytest
from util import strip_uid_from_dict

import cript


def test_create_file() -> None:
    """
    tests that a simple file with only required attributes can be created
    """
    file_node = cript.File(source="https://google.com", type="calibration")

    assert isinstance(file_node, cript.File)


def test_create_file_local_source(tmp_path) -> None:
    """
    tests that a simple file with only required attributes can be created
    with source pointing to a local file on storage

    create a temporary directory with temporary file
    """

    # create a temporary file in the temporary directory to test with
    file_path = tmp_path / "test.txt"
    with open(file_path, "w") as temporary_file:
        temporary_file.write("hello world!")

    assert cript.File(source=str(file_path), type="calibration")


@pytest.fixture(scope="session")
def file_node() -> cript.File:
    """
    create a file node for other tests to use

    Returns
    -------
    File
    """

    # create a File node with all fields
    my_file = cript.File(source="https://criptapp.com", type="calibration", extension=".pdf", data_dictionary="my data dictionary")
    # use the file node for tests
    yield my_file

    # clean up file node after each test, so the file test is always uniform
    # set the file node to original state
    my_file = cript.File(source="https://criptapp.com", type="calibration", extension=".pdf", data_dictionary="my data dictionary ")


def test_file_type_invalid_vocabulary() -> None:
    """
    tests that setting the file type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_file_getters_and_setters(complex_file_node) -> None:
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
    complex_file_node.source = new_source
    complex_file_node.type = new_file_type
    complex_file_node.extension = new_file_extension
    complex_file_node.data_dictionary = new_data_dictionary

    # ------- assert set and get properties are the same -------
    assert complex_file_node.source == new_source
    assert complex_file_node.type == new_file_type
    assert complex_file_node.extension == new_file_extension
    assert complex_file_node.data_dictionary == new_data_dictionary


def test_serialize_file_to_json(complex_file_node) -> None:
    """
    tests that it can correctly turn the file node into its equivalent JSON
    """

    expected_file_node_dict = {
        "node": ["File"],
        "source": "https://criptapp.org",
        "type": "calibration",
        "extension": ".csv",
        "data_dictionary": "my file's data dictionary",
    }

    # compare dicts for more accurate comparison
    assert strip_uid_from_dict(json.loads(complex_file_node.json)) == expected_file_node_dict


def test_uuid(complex_file_node):
    file_node = complex_file_node

    # Deep copies should not share uuid (or uids) or urls
    file_node2 = copy.deepcopy(complex_file_node)
    assert file_node.uuid != file_node2.uuid
    assert file_node.uid != file_node2.uid
    assert file_node.url != file_node2.url

    # Loads from json have the same uuid and url
    file_node3 = cript.load_nodes_from_json(file_node.json)
    assert file_node3.uuid == file_node.uuid
    assert file_node3.url == file_node.url


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
