import json
import uuid

from integration_test_helper import integrate_nodes_helper, delete_integration_node_helper
from util import strip_uid_from_dict

import cript


def test_parameter_setter_getter(complex_parameter_node):
    complex_parameter_node.key = "damping_time"
    complex_parameter_node.value = 15.0
    complex_parameter_node.unit = "m"

    assert complex_parameter_node.value == 15.0
    assert complex_parameter_node.key == "damping_time"
    assert complex_parameter_node.unit == "m"

    # remove optional attributes
    complex_parameter_node.unit = ""

    # assert optional attributes have been removed
    assert complex_parameter_node.unit == ""


def test_parameter_json_serialization(complex_parameter_node, complex_parameter_dict):
    p = complex_parameter_node
    p_str = p.json
    p2 = cript.load_nodes_from_json(p_str)
    p_dict = json.loads(p2.json)
    assert strip_uid_from_dict(p_dict) == complex_parameter_dict
    assert p2.json == p.json


def test_integration_parameter(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration, simple_algorithm_node, complex_parameter_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_parameter_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]
    simple_project_node.collection[0].experiment = [simple_experiment_node]
    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration = [simple_software_configuration]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm = [simple_algorithm_node]
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm[0].parameter = [complex_parameter_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm[0].parameter[0].value = 123456789

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=complex_parameter_node)
