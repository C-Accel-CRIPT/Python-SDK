# trunk-ignore-all(ruff/F403)
"""
This conftest file contains simple nodes (nodes with minimal required arguments)
and complex node (nodes that have all possible arguments), to use for testing.

Since nodes often depend on other nodes copying and pasting nodes is not ideal,
and keeping all nodes in one file makes it easier/cleaner to create tests.

The fixtures are all functional fixtures that stay consistent between all tests.
"""
import os
from pathlib import Path

import pytest
from fixtures.primary_nodes import *
from fixtures.subobjects import *
from fixtures.supporting_nodes import *

import cript

from test_utils.multiple_environment_config_helper import _get_config_file_path, CRIPTEnvironment

# flip integration tests ON or OFF with this boolean
# automatically gets value env vars to run integration tests
HAS_INTEGRATION_TESTS_ENABLED: bool = os.getenv("CRIPT_TESTS").title() == "True"

SERVER_ENVIRONMENT: str = "production"


@pytest.fixture(scope="session", autouse=True)
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns
    -------
    API: cript.API
        The created CRIPT API instance.
    """
    assert cript.api.api._global_cached_api is None

    config_file_path: Path = Path(__file__).parent / f"{SERVER_ENVIRONMENT.lower()}_config.json"

    with cript.API(config_file_path=config_file_path) as api:
        # using the tests folder name within our cloud storage
        api._BUCKET_DIRECTORY_NAME = "tests"

        print(api.host)
        print(api._api_token)
        print(api._storage_token)

        yield api
    assert cript.api.api._global_cached_api is None
