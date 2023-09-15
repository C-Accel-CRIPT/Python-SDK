import json
import uuid

from integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
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
    complex_condition_node.key = "pressure"
    assert complex_condition_node.key == "pressure"
    complex_condition_node.type = "avg"
    assert complex_condition_node.type == "avg"

    complex_condition_node.set_value(1, "bar")
    assert complex_condition_node.value == 1
    assert complex_condition_node.unit == "bar"

    complex_condition_node.descriptor = "ambient pressure"
    assert complex_condition_node.descriptor == "ambient pressure"

    complex_condition_node.set_uncertainty(0.1, "stdev")
    assert complex_condition_node.uncertainty == 0.1
    assert complex_condition_node.uncertainty_type == "stdev"

    complex_condition_node.set_id = None
    assert complex_condition_node.set_id is None
    complex_condition_node.measurement_id = None
    assert complex_condition_node.measurement_id is None

    complex_condition_node.data = [complex_data_node]
    assert complex_condition_node.data[0] is complex_data_node

    # remove optional attributes
    complex_condition_node.descriptor = ""
    complex_condition_node.set_id = None
    complex_condition_node.measurement_id = None
    complex_condition_node.set_uncertainty(new_uncertainty_type="", new_uncertainty=None)

    # TODO getting `CRIPTNodeSchemaError` when removing this data node from condition
    # complex_condition_node.data = None

    # assert the optional node attributes have been removed
    assert complex_condition_node.descriptor == ""
    assert complex_condition_node.set_id is None
    assert complex_condition_node.measurement_id is None
    assert complex_condition_node.uncertainty is None
    assert complex_condition_node.uncertainty_type == ""
    # assert complex_condition_node.data is Non


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

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].condition[0].descriptor = "condition descriptor UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_condition_node)
