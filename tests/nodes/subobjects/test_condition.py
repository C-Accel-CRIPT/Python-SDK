import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict


def test_json(complex_condition_node, complex_condition_dict):
    c = complex_condition_node
    c_dict = json.loads(c.get_json(condense_to_uuid={}).json)
    assert strip_uid_from_dict(c_dict) == strip_uid_from_dict(complex_condition_dict)
    ## TODO address deserialization of uid and uuid nodes
    # c_deepcopy = copy.deepcopy(c)
    # c2 = cript.load_nodes_from_json(c_deepcopy.get_json(condense_to_uuid={}).json)
    # assert strip_uid_from_dict(json.loads(c2.get_json(condense_to_uuid={}).json)) == strip_uid_from_dict(json.loads(c.get_json(condense_to_uuid={}).json))


def test_setter_getters(complex_condition_node, complex_data_node):
    c2 = complex_condition_node
    c2.key = "pressure"
    assert c2.key == "pressure"
    c2.type = "avg"
    assert c2.type == "avg"

    c2.set_value(1, "bar")
    assert c2.value == 1
    assert c2.unit == "bar"

    c2.descriptor = "ambient pressure"
    assert c2.descriptor == "ambient pressure"

    c2.set_uncertainty(0.1, "stdev")
    assert c2.uncertainty == 0.1
    assert c2.uncertainty_type == "stdev"

    c2.set_id = None
    assert c2.set_id is None
    c2.measurement_id = None
    assert c2.measurement_id is None

    c2.data = [complex_data_node]
    assert c2.data[0] is complex_data_node


def test_integration_process_condition(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_condition_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # ========= test create =========
    # renamed project node to avoid duplicate project node API error
    simple_project_node.name = f"{simple_project_node.name}_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].experiment = [simple_experiment_node]

    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]

    simple_project_node.collection[0].experiment[0].computation[0].condition = [simple_condition_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].condition[0].descriptor = "condition descriptor UPDATED"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
