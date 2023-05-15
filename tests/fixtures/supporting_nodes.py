import datetime
import json

import pytest

import cript


@pytest.fixture(scope="function")
def complex_file_node() -> cript.File:
    """
    complex file node with only required arguments
    """
    my_file = cript.File(source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary")

    return my_file


@pytest.fixture(scope="function")
def complex_user_dict() -> dict:
    user_dict = {"node": ["User"]}
    user_dict["created_at"] = str(datetime.datetime.now())
    user_dict["model_version"] = "0.0.1"
    user_dict["picture"] = "/my/picture/path"
    user_dict["updated_at"] = str(datetime.datetime.now())
    user_dict["username"] = "testuser"
    user_dict["email"] = "test@emai.com"
    user_dict["orcid"] = "0000-0002-0000-0000"
    return user_dict


@pytest.fixture(scope="function")
def complex_user_node(complex_user_dict) -> cript.User:
    user_node = cript.load_nodes_from_json(json.dumps(complex_user_dict))
    return user_node
