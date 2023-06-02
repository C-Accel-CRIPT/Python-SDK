import copy
import datetime
import json
import uuid

import pytest
from util import strip_uid_from_dict

import cript


def test_create_file() -> None:
    """
    tests that a simple file with only required attributes can be created
    """
    file_node = cript.File(source="https://google.com", type="calibration")

    assert isinstance(file_node, cript.File)


def test_local_file_source_upload_and_download(tmp_path_factory) -> None:
    """
    upload a file and download it and be sure the contents are the same

    1. create a temporary file and get its file path
    1. create a unique string
    1. write unique string to temporary file
    1. create a file node with the source being the temporary file
        1. the file should then be automatically uploaded to cloud storage
        and the source should be replaced with cloud storage source beginning with `https://`
    1. download the file to a temporary path
        1. read that file text and assert that the string written and read are the same
    """
    file_text: str = (
        f"This is an automated test from the Python SDK within "
        f"`tests/nodes/supporting_nodes/test_file.py/test_local_file_source_upload_and_download()` "
        f"checking that the file source is automatically and correctly uploaded to AWS S3. "
        f"The test is conducted on UTC time of '{datetime.datetime.utcnow()}' "
        f"with the unique UUID of '{str(uuid.uuid4())}'"
    )

    # create a temp file and write to it
    upload_file_dir = tmp_path_factory.mktemp("file_test_upload_file_dir")
    local_file_path = upload_file_dir / "my_upload_file.txt"
    local_file_path.write_text(file_text)

    # create a file node with a local file path
    my_file = cript.File(source=str(local_file_path), type="data")

    # check that the file source has been uploaded to cloud storage and source has changed to reflect that
    assert my_file.source.startswith("https://cript-development-user-data.s3.amazonaws.com")

    # Get the temporary directory path and clean up handled by pytest
    download_file_dir = tmp_path_factory.mktemp("file_test_download_file_dir")
    download_file_name = "my_downloaded_file.txt"

    # download file
    my_file.download(destination_directory_path=download_file_dir, file_name=download_file_name)

    # the path the file was downloaded to and can be read from
    downloaded_local_file_path = download_file_dir / download_file_name

    # read file contents from where the file was downloaded
    downloaded_file_contents = downloaded_local_file_path.read_text()

    # assert file contents for upload and download are the same
    assert downloaded_file_contents == file_text


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


def test_source_setter_local_file(tmp_path_factory, complex_file_node) -> None:
    """
    test to be sure that giving a local file path to the File node setter works just as well as the constructor

    change the File node source to a local file path the file node should upload the file to cloud storage

    then download the file node and compare to be sure that it is correct
    """

    file_text: str = (
        f"This is an automated test from the Python SDK within "
        f"`tests/nodes/supporting_nodes/test_file.py/test_source_setter_local_file()` "
        f"checking that the file source is automatically and correctly uploaded to AWS S3. "
        f"The test is conducted on UTC time of '{datetime.datetime.utcnow()}' "
        f"with the unique UUID of '{str(uuid.uuid4())}'"
    )

    # create a temp file and write to it
    upload_file_dir = tmp_path_factory.mktemp("file_source_test_upload_file_dir")
    local_file_path = upload_file_dir / "my_upload_file.csv"
    local_file_path.write_text(file_text)

    # change file source to a local file source
    complex_file_node.source = str(local_file_path)

    # check that the file source has been uploaded to cloud storage and source has changed to reflect that
    assert complex_file_node.source.startswith("https://cript-development-user-data.s3.amazonaws.com")

    # Get the temporary directory path and clean up handled by pytest
    download_file_dir = tmp_path_factory.mktemp("file_source_test_download_file_dir")
    download_file_name = "my_downloaded_file.csv"

    # download file
    complex_file_node.download(destination_directory_path=download_file_dir, file_name=download_file_name)

    # the path the file was downloaded to and can be read from
    downloaded_local_file_path = download_file_dir / download_file_name

    # read file contents from where the file was downloaded
    downloaded_file_contents = downloaded_local_file_path.read_text()

    # assert file contents for upload and download are the same
    assert downloaded_file_contents == file_text


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
