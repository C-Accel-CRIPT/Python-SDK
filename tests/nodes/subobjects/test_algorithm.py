import json
import uuid

from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict

import cript


def test_setter_getter(simple_algorithm_node, complex_citation_node, complex_parameter_node):
    """
    test that getters and setters are working correctly in algorithm sub-object
    """
    simple_algorithm_node.key = "berendsen"
    assert simple_algorithm_node.key == "berendsen"

    simple_algorithm_node.type = "integration"
    assert simple_algorithm_node.type == "integration"

    simple_algorithm_node.parameter = [complex_parameter_node]
    assert simple_algorithm_node.parameter == [complex_parameter_node]

    simple_algorithm_node.citation += [complex_citation_node]
    assert strip_uid_from_dict(json.loads(simple_algorithm_node.citation[0].json)) == strip_uid_from_dict(json.loads(complex_citation_node.json))

    # remove optional attributes
    simple_algorithm_node.parameter = []
    simple_algorithm_node.citation = []

    # assert the optional attributes have been removed
    assert simple_algorithm_node.parameter == []
    assert simple_algorithm_node.citation == []


def test_json(simple_algorithm_node, simple_algorithm_dict, complex_citation_node):
    a = simple_algorithm_node
    a_dict = json.loads(a.json)
    assert strip_uid_from_dict(a_dict) == simple_algorithm_dict
    print(a.get_json(indent=2).json)
    a2 = cript.load_nodes_from_json(a.json)
    assert strip_uid_from_dict(json.loads(a2.json)) == strip_uid_from_dict(a_dict)


def test_integration_algorithm(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration, simple_algorithm_node):
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
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm = [simple_algorithm_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change a simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm[0].type = "integration"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_algorithm_node)
