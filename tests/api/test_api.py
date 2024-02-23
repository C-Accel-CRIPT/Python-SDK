import datetime
import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import Dict

import pytest
import requests

import cript
from conftest import HAS_INTEGRATION_TESTS_ENABLED
from cript.api.paginator import Paginator


def test_api_with_invalid_host() -> None:
    """
    this mostly tests the _prepare_host() function to be sure it is working as expected
    * attempting to create an api client with invalid host appropriately throws a `CRIPTConnectionError`
    * giving a host that does not start with http such as "criptapp.org" should throw an InvalidHostError
    """
    with pytest.raises((requests.ConnectionError, cript.api.exceptions.CRIPTConnectionError)):
        cript.API(host="https://some_invalid_host", api_token="123456789", storage_token="123456")

    with pytest.raises(cript.api.exceptions.InvalidHostError):
        cript.API(host="no_http_host.org", api_token="123456789", storage_token="987654321")


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="skipping because API client needs API token")
def test_api_context(cript_api: cript.API) -> None:
    assert cript.api.api._global_cached_api is not None
    assert cript.api.api._get_global_cached_api() is not None


def test_create_api_with_none() -> None:
    """
    tests that when the cript.API is given None for host, api_token, storage_token that it can correctly
    retrieve things from the env variable.
    assert that the values found from the environment are equal to what the SDK API class
    correctly got for `_host`, `_api_token`, and `_storage_token`

    Notes
    -----
    This test is dependent on the environment (local computer or CI), where it expects
    `CRIPT_HOST`, `CRIPT_TOKEN` and `CRIPT_STORAGE_TOKEN` to be in the environment variables,
    otherwise, it will not be able to find the needed environment variables and the test will fail
    """
    # set env vars
    # strip end slash to make all hosts uniform for comparison
    #   regardless of how it was entered in the env var
    env_var_host = os.environ["CRIPT_HOST"].rstrip("/")

    # create an API instance with `None`
    api = cript.API(host=None, api_token=None, storage_token=None)

    # assert SDK correctly got env vars to create cript.API with
    # host/api/v1
    assert api._host == f"{env_var_host}"
    assert api._api_token == os.environ["CRIPT_TOKEN"]
    assert api._storage_token == os.environ["CRIPT_STORAGE_TOKEN"]


def test_config_file() -> None:
    """
    test if the api can read configurations from `config.json`
    """

    config_file_texts = {"host": "https://lb-stage.mycriptapp.org", "api_token": "I am token", "storage_token": "I am storage token"}

    with tempfile.NamedTemporaryFile(mode="w+t", suffix=".json", delete=False) as temp_file:
        # absolute file path
        config_file_path = temp_file.name

        # write JSON to temporary file
        temp_file.write(json.dumps(config_file_texts))

        # force text to be written to file
        temp_file.flush()

        api = cript.API(config_file_path=config_file_path)

        assert api._host == config_file_texts["host"]
        assert api._api_token == config_file_texts["api_token"]


def test_download_file_from_url(cript_api: cript.API, tmp_path) -> None:
    """
    downloads the file from a URL and writes it to disk
    then opens, reads, and compares that the file was gotten and written correctly
    """
    url_to_download_file: str = "https://criptscripts.org/cript_graph_json/JSON/cao_protein.json"

    # `download_file()` will get the file extension from the end of the URL and add it onto the name
    # the path it will save it to will be `tmp_path/downloaded_file_name.json`
    path_to_save_file: Path = tmp_path / "downloaded_file_name"

    cript_api.download_file(url_to_download_file, str(path_to_save_file))

    # add file extension to file path and convert it to file path object
    path_to_read_file = Path(str(path_to_save_file) + ".json").resolve()

    # open the file that was just saved and read the contents
    saved_file_contents = json.loads(path_to_read_file.read_text())

    # make a request manually to get the contents and check that the contents are the same
    response: Dict = requests.get(url=url_to_download_file).json()

    # assert that the file I've save and the one on the web are the same
    assert response == saved_file_contents


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real storage_token from a real frontend")
def test_upload_and_download_local_file(cript_api, tmp_path_factory) -> None:
    """
    tests file upload to cloud storage
    test by uploading a local file to AWS S3 using cognito mode
    and then downloading the same file and checking their contents are the same
    proving that the file was uploaded and downloaded correctly

    1. create a temporary file
        1. write a unique string to the temporary file via UUID4 and date
            so when downloading it later the downloaded file cannot possibly be a mistake and we know
            for sure that it is the correct file uploaded and downloaded
    1. upload to AWS S3 `tests/` directory
    1. we can be sure that the file has been correctly uploaded to AWS S3 if we can download the same file
        and assert that the file contents are the same as original
    """
    file_text: str = (
        f"This is an automated test from the Python SDK within `tests/api/test_api.py` " f"within the `test_upload_file_to_aws_s3()` test function " f"on UTC time of '{datetime.datetime.utcnow()}' " f"with the unique UUID of '{str(uuid.uuid4())}'"
    )

    # Create a temporary file with unique contents
    upload_test_file = tmp_path_factory.mktemp("test_api_file_upload") / "temp_upload_file.txt"
    upload_test_file.write_text(file_text)

    # upload file to AWS S3
    my_file_cloud_storage_object_name = cript_api.upload_file(file_path=upload_test_file)

    # temporary file path and new file to write the cloud storage file contents to
    download_test_file = tmp_path_factory.mktemp("test_api_file_download") / "temp_download_file.txt"

    # download file from cloud storage
    cript_api.download_file(file_source=my_file_cloud_storage_object_name, destination_path=str(download_test_file))

    # read file contents
    downloaded_file_contents = download_test_file.read_text()

    # assert download file contents are the same as uploaded file contents
    assert downloaded_file_contents == file_text


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_node_type(cript_api: cript.API) -> None:
    """
    tests the api.search() method with just a node type material search

    just testing that something comes back from the server

    Notes
    -----
    * also tests that it can go to the next page and previous page
    * later this test should be expanded to test things that it should expect an error for as well.
    * test checks if there are at least 5 things in the paginator
        *  each page should have a max of 10 results and there should be close to 5k materials in db,
        * more than enough to at least have 5 in the paginator
    """
    materials_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.NODE_TYPE, value_to_search=None)

    # test search results
    assert isinstance(materials_paginator, Paginator)
    assert len(materials_paginator.current_page_results) > 5
    first_page_first_result = materials_paginator.current_page_results[0]["name"]

    # just checking that the word has a few characters in it
    assert len(first_page_first_result) > 3

    # tests that it can correctly go to the next page
    materials_paginator.next_page()
    assert len(materials_paginator.current_page_results) > 5
    second_page_first_result = materials_paginator.current_page_results[0]["name"]

    assert len(second_page_first_result) > 3

    # tests that it can correctly go to the previous page
    materials_paginator.previous_page()
    assert len(materials_paginator.current_page_results) > 5

    assert len(first_page_first_result) > 3


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_contains_name(cript_api: cript.API) -> None:
    """
    tests that it can correctly search with contains name mode
    searches for a material that contains the name "poly"
    """
    contains_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.CONTAINS_NAME, value_to_search="poly")

    assert isinstance(contains_name_paginator, Paginator)
    assert len(contains_name_paginator.current_page_results) > 5

    contains_name_first_result = contains_name_paginator.current_page_results[0]["name"]

    # just checking that the result has a few characters in it
    assert len(contains_name_first_result) > 3


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_exact_name(cript_api: cript.API) -> None:
    """
    tests search method with exact name search
    searches for material "Sodium polystyrene sulfonate"
    """
    exact_name_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.EXACT_NAME, value_to_search="Sodium polystyrene sulfonate")

    assert isinstance(exact_name_paginator, Paginator)
    assert len(exact_name_paginator.current_page_results) == 1
    assert exact_name_paginator.current_page_results[0]["name"] == "Sodium polystyrene sulfonate"


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_uuid(cript_api: cript.API, dynamic_material_data) -> None:
    """
    tests search with UUID
    searches for `Sodium polystyrene sulfonate` material via UUID

    The test is made dynamic to work with any server environment
    1. gets the material via `exact name search` and gets the full node
    2. takes the UUID from the full node and puts it into the `UUID search`
    3. asserts everything is as expected
    """
    uuid_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.UUID, value_to_search=dynamic_material_data["uuid"])

    assert isinstance(uuid_paginator, Paginator)
    assert len(uuid_paginator.current_page_results) == 1
    assert uuid_paginator.current_page_results[0]["name"] == dynamic_material_data["name"]
    assert uuid_paginator.current_page_results[0]["uuid"] == dynamic_material_data["uuid"]


@pytest.mark.skipif(not HAS_INTEGRATION_TESTS_ENABLED, reason="requires a real cript_api_token")
def test_api_search_bigsmiles(cript_api: cript.API) -> None:
    """
    tests search method with bigsmiles SearchMode to see if we just get at least one match
    searches for material
    "{[][<]C(C)C(=O)O[>][<]}{[$][$]CCC(C)C[$],[$]CC(C(C)C)[$],[$]CC(C)(CC)[$][]}"

    another good example can be "{[][$]CC(C)(C(=O)OCCCC)[$][]}"
    """
    bigsmiles_search_value = "{[][<]C(C)C(=O)O[>][<]}{[$][$]CCC(C)C[$],[$]CC(C(C)C)[$],[$]CC(C)(CC)[$][]}"

    bigsmiles_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.BIGSMILES, value_to_search=bigsmiles_search_value)

    assert isinstance(bigsmiles_paginator, Paginator)
    assert len(bigsmiles_paginator.current_page_results) >= 1
    # not sure if this will always be in this position in every server environment, so commenting it out for now
    # assert bigsmiles_paginator.current_page_results[1]["name"] == "BCDB_Material_285"


def test_get_my_user_node_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the user node associated with the API Token
    """
    pass


def test_get_my_group_node_from_api(cript_api: cript.API) -> None:
    """
    tests that group node that is associated with their API Token can be gotten correctly
    """
    pass


def test_get_my_projects_from_api(cript_api: cript.API) -> None:
    """
    get a page of project nodes that is associated with the API token
    """
    pass
