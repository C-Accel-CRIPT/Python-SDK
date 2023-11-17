import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


def test_json(complex_software_configuration_node, complex_software_configuration_dict):
    sc = complex_software_configuration_node
    sc_dict = strip_uid_from_dict(json.loads(sc.json))
    assert sc_dict == complex_software_configuration_dict
    sc2 = cript.load_nodes_from_json(sc.json)

    assert strip_uid_from_dict(json.loads(sc2.json)) == strip_uid_from_dict(json.loads(sc.json))


def test_setter_getter(simple_software_configuration, simple_algorithm_node, complex_citation_node):
    """
    test setters and getters for `SoftwareConfiguration` and be sure it works fine
    also test that the node can be set and also reset
    """
    new_notes: str = "my new notes"

    # use setters
    simple_software_configuration.algorithm = [simple_algorithm_node]
    simple_software_configuration.citation = [complex_citation_node]
    simple_software_configuration.notes = new_notes

    # assert getters and setters are same
    assert simple_software_configuration.algorithm == [simple_algorithm_node]
    assert simple_software_configuration.citation == [complex_citation_node]
    assert simple_software_configuration.notes == new_notes

    # remove optional attributes
    simple_software_configuration.algorithm = []
    simple_software_configuration.citation = []
    simple_software_configuration.notes = ""

    # assert that optional attributes have been removed from data node
    assert simple_software_configuration.algorithm == []
    assert simple_software_configuration.citation == []
    assert simple_software_configuration.notes == ""


def test_integration_software_configuration(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_software_configuration_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]
    simple_project_node.collection[0].experiment = [simple_experiment_node]
    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration = [simple_software_configuration]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].notes = "software configuration integration test UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_software_configuration)
