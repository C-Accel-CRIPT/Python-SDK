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
