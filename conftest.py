# trunk-ignore-all(ruff/F403)
"""
This conftest file contains simple nodes (nodes with minimal required arguments)
and complex node (nodes that have all possible arguments), to use for testing.

Since nodes often depend on other nodes copying and pasting nodes is not ideal,
and keeping all nodes in one file makes it easier/cleaner to create tests.

The fixtures are all functional fixtures that stay consistent between all tests.
"""
import os

import pytest

import cript
from tests.fixtures.api_fixtures import *
from tests.fixtures.primary_nodes import *
from tests.fixtures.subobjects import *
from tests.fixtures.supporting_nodes import *


def _get_cript_tests_env() -> bool:
    """
    Gets `CRIPT_TESTS` value from env variable and converts it to boolean.
    If `CRIPT_TESTS` env var does not exist then it will default it to False.
    """
    try:
        has_integration_tests_enabled = os.getenv("CRIPT_TESTS").title().strip() == "True"
    except AttributeError:
        has_integration_tests_enabled = True

    return has_integration_tests_enabled


# flip integration tests ON or OFF with this boolean
# automatically gets value env vars to run integration tests
HAS_INTEGRATION_TESTS_ENABLED: bool = _get_cript_tests_env()


@pytest.fixture(scope="session", autouse=True)
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns
    -------
    API: cript.API
        The created CRIPT API instance.
    """
    storage_token = os.getenv("CRIPT_STORAGE_TOKEN")

    with cript.API(host=None, api_token=None, storage_token=storage_token) as api:
        # overriding AWS S3 cognito variables to be sure we do not upload test data to production storage
        # staging AWS S3 cognito storage variables
        api._IDENTITY_POOL_ID = "us-east-1:25043452-a922-43af-b8a6-7e938a9e55c1"
        api._COGNITO_LOGIN_PROVIDER = "cognito-idp.us-east-1.amazonaws.com/us-east-1_vyK1N9p22"
        api._BUCKET_NAME = "cript-stage-user-data"
        # using the tests folder name within our cloud storage
        api._BUCKET_DIRECTORY_NAME = "tests"

        yield api


@pytest.fixture(autouse=True)
def inject_doctest_namespace(doctest_namespace, cript_api):
    doctest_namespace["api"] = cript_api
