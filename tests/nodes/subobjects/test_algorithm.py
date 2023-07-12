import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_setter_getter(complex_algorithm_node, complex_citation_node):
    a = complex_algorithm_node
    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"
    a.citation += [complex_citation_node]
    assert strip_uid_from_dict(json.loads(a.citation[0].json)) == strip_uid_from_dict(json.loads(complex_citation_node.json))


def test_json(complex_algorithm_node, complex_algorithm_dict, complex_citation_node):
    a = complex_algorithm_node
    a_dict = json.loads(a.json)
    assert strip_uid_from_dict(a_dict) == complex_algorithm_dict
    print(a.get_json(indent=2).json)
    a2 = cript.load_nodes_from_json(a.json)
    assert strip_uid_from_dict(json.loads(a2.json)) == strip_uid_from_dict(a_dict)


def test_integration_algorithm(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration, complex_algorithm_node):
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

    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm = [complex_algorithm_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change a simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm[0].type = "integration"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
