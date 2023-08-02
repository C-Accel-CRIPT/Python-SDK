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
from fixtures.primary_nodes import *
from fixtures.subobjects import *
from fixtures.supporting_nodes import *

import cript


def _get_cript_tests_env() -> bool:
    """
    A little helper function, that ensure to mostly default to True.
    Except if an explicit spelling of False is detected.
    """
    env_var = os.getenv("CRIPT_TESTS")
    if env_var in ("false", "FALSE", "False"):
        return False
    return True


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
    storage_token = "my storage token"

    assert cript.api.api._global_cached_api is None
    with cript.API(host=None, api_token=None, storage_token=storage_token) as api:
        # using the tests folder name within our cloud storage
        api._BUCKET_DIRECTORY_NAME = "tests"
        yield api
    assert cript.api.api._global_cached_api is None
