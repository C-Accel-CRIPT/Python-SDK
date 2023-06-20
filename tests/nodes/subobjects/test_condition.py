import json
import uuid

from util import strip_uid_from_dict

from tests.test_integration import integrate_nodes_helper


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


def test_integration_process_condition(cript_api, simple_project_node, simple_process_node, complex_condition_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    simple_project_node.name = f"test_integration_condition_{uuid.uuid4().hex}"

    simple_process_node.condition = [complex_condition_node]

    simple_project_node.collection[0].experiment[0].process = [simple_process_node]

    # TODO getting CRIPTOrphanedMaterialError
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

