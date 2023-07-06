import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_parameter_setter_getter(complex_parameter_node):
    p = complex_parameter_node
    p.key = "damping_time"
    assert p.key == "damping_time"
    p.value = 15.0
    assert p.value == 15.0
    p.unit = "m"
    assert p.unit == "m"


def test_parameter_json_serialization(complex_parameter_node, complex_parameter_dict):
    p = complex_parameter_node
    p_str = p.json
    p2 = cript.load_nodes_from_json(p_str)
    p_dict = json.loads(p2.json)
    assert strip_uid_from_dict(p_dict) == complex_parameter_dict
    assert p2.json == p.json


def test_integration_parameter(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration, complex_algorithm_node, complex_parameter_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    simple_project_node.name = f"test_integration_parameter_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].experiment = [simple_experiment_node]

    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]

    simple_project_node.collection[0].experiment[0].computation[0].software_configuration = [simple_software_configuration]

    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm = [complex_algorithm_node]

    simple_project_node.collection[0].experiment[0].computation[0].software_configuration[0].algorithm[0].parameter = [complex_parameter_node]

    # TODO getting CRIPTJsonDeserializationError
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
