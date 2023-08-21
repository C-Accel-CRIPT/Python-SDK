import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_json(complex_citation_node, complex_citation_dict):
    c = complex_citation_node
    c_dict = strip_uid_from_dict(json.loads(c.json))
    assert c_dict == complex_citation_dict
    c2 = cript.load_nodes_from_json(c.json)
    c2_dict = strip_uid_from_dict(json.loads(c2.json))
    assert c_dict == c2_dict


def test_setter_getter(complex_citation_node, complex_reference_node):
    """
    test getters and setters are working fine
    """
    complex_citation_node.type = "replicated"
    assert complex_citation_node.type == "replicated"

    new_ref = complex_reference_node
    new_ref.title = "foo bar"
    complex_citation_node.reference = new_ref
    assert complex_citation_node.reference == new_ref


def test_integration_citation(cript_api, simple_project_node, simple_collection_node, complex_citation_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_citation_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].citation = [complex_citation_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].citation[0].type = "extracted_by_human"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
