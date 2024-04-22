import datetime
import json

import pytest

import cript


@pytest.fixture(scope="function")
def complex_file_node() -> cript.File:
    """
    complex file node with only required arguments
    """
    # TODO add notes="my complex URL file source notes" since this is a complex node
    #   and update all other tests that depend on this fixture and addition of notes would throw them off
    my_file = cript.File(
        name="my complex file node fixture",
        source="https://criptapp.org",
        type="calibration",
        extension=".csv",
        data_dictionary="my file's data dictionary",
    )

    return my_file


@pytest.fixture(scope="function")
def complex_local_file_node(tmp_path_factory) -> cript.File:
    """
    complex local file node with all possible arguments

    1. create a temporary file and get its file path
    1. create a unique string
    1. write unique string to temporary file
    1. create a file node with the source being the temporary file
    """
    # create unique string
    import datetime
    import uuid

    file_text: str = (
        f"This is an automated test from the Python SDK within "
        f"`tests/nodes/supporting_nodes/test_file.py/test_local_file_source_upload_and_download()` "
        f"checking that the file source is automatically and correctly uploaded to AWS S3. "
        f"The test is conducted on UTC time of '{datetime.datetime.utcnow()}' "
        f"with the unique UUID of '{str(uuid.uuid4())}'"
    )

    # create a temp file and write to it
    local_file_dir = tmp_path_factory.mktemp("complex_local_file_node_fixture_dir")
    local_file_path = local_file_dir / "my_local_file_fixture.txt"
    local_file_path.write_text(file_text)

    # create file node with source being a local file on computer
    my_local_file = cript.File(
        name="my complex local file node fixture", source=str(local_file_path), type="calibration", extension=".csv", data_dictionary="my complex local files fixture data dictionary", notes="my complex local files fixture notes"
    )

    return my_local_file


@pytest.fixture(scope="function")
def complex_user_dict(cript_api) -> dict:
    user_node = next(cript_api.search(node_type=cript.User, search_mode=cript.SearchModes.NODE_TYPE))

    user_dict = json.loads(user_node.get_json().json)
    print("8888888--------")
    print(user_dict)
    return user_dict


@pytest.fixture(scope="function")
def complex_user_node(complex_user_dict) -> cript.User:
    user_node = cript.load_nodes_from_json(json.dumps(complex_user_dict))
    return user_node
