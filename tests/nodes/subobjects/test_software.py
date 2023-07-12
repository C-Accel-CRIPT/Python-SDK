import copy
import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_json(complex_software_node, complex_software_dict):
    s = complex_software_node
    s_dict = strip_uid_from_dict(json.loads(s.json))
    assert s_dict == complex_software_dict
    s2 = cript.load_nodes_from_json(s.json)
    assert s2.json == s.json


def test_setter_getter(complex_software_node):
    s2 = complex_software_node
    s2.name = "PySAGES"
    assert s2.name == "PySAGES"
    s2.version = "v0.3.0"
    assert s2.version == "v0.3.0"
    s2.source = "https://github.com/SSAGESLabs/PySAGES"
    assert s2.source == "https://github.com/SSAGESLabs/PySAGES"


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

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].software.version = "software version UPDATED"
