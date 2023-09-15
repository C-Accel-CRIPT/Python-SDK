import copy
import json
import uuid

import pytest
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict

import cript
from cript.api.exceptions import APIError


def test_json(complex_software_node, complex_software_dict):
    s = complex_software_node
    s_dict = strip_uid_from_dict(json.loads(s.json))
    assert s_dict == complex_software_dict
    s2 = cript.load_nodes_from_json(s.json)
    assert s2.json == s.json


def test_setter_getter(complex_software_node):
    complex_software_node.name = "PySAGES"
    assert complex_software_node.name == "PySAGES"

    complex_software_node.version = "v0.3.0"
    assert complex_software_node.version == "v0.3.0"

    complex_software_node.source = "https://github.com/SSAGESLabs/PySAGES"
    assert complex_software_node.source == "https://github.com/SSAGESLabs/PySAGES"

    # remove optional attributes
    complex_software_node.source = ""

    # assert optional attributes have been removed
    assert complex_software_node.source == ""


def test_uuid(complex_software_node):
    s = complex_software_node

    # Deep copies should not share uuid (or uids) or urls
    s2 = copy.deepcopy(complex_software_node)
    assert s.uuid != s2.uuid
    assert s.uid != s2.uid
    assert s.url != s2.url

    # Loads from json have the same uuid and url
    s3 = cript.load_nodes_from_json(s.json)
    assert s3.uuid == s.uuid
    assert s3.url == s.url


def test_integration_software(cript_api, simple_project_node, simple_computation_node, simple_software_configuration, complex_software_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal

    Notes
    -----
    indirectly tests citation node along with reference node
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_software_name_{uuid.uuid4().hex}"

    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration = [simple_software_configuration]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].software = complex_software_node

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].software.version = "software version UPDATED"
    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    # software nodes are frozen nodes and cannot be deleted
    # we expect the API to give an error when trying to delete a frozen node
    with pytest.raises(APIError) as error:
        delete_integration_node_helper(cript_api=cript_api, node_to_delete=complex_software_node)

        # the current error that the API gives
        assert "The browser (or proxy) sent a request that this server could not understand." in str(error)
