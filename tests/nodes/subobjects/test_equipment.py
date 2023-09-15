import copy
import json
import uuid

from integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from util import strip_uid_from_dict


def test_json(complex_equipment_node, complex_equipment_dict):
    e = complex_equipment_node
    e_dict = strip_uid_from_dict(json.loads(e.get_json(condense_to_uuid={}).json))
    assert strip_uid_from_dict(e_dict) == strip_uid_from_dict(complex_equipment_dict)
    e2 = copy.deepcopy(e)

    assert strip_uid_from_dict(json.loads(e.get_json(condense_to_uuid={}).json)) == strip_uid_from_dict(json.loads(e2.get_json(condense_to_uuid={}).json))


def test_setter_getter(complex_equipment_node, complex_condition_node, complex_file_node, complex_citation_node):
    """
    test that getters and setters are working fine
    """
    complex_equipment_node.key = "glass_beaker"
    assert complex_equipment_node.key == "glass_beaker"

    complex_equipment_node.description = "Fancy glassware"
    assert complex_equipment_node.description == "Fancy glassware"

    assert len(complex_equipment_node.condition) == 1
    complex_equipment_node.condition += [complex_condition_node]
    assert complex_equipment_node.condition[1] == complex_condition_node

    assert len(complex_equipment_node.file) == 0
    complex_equipment_node.file += [complex_file_node]
    assert complex_equipment_node.file[-1] is complex_file_node

    assert len(complex_equipment_node.citation) == 1
    complex_equipment_node.citation += [complex_citation_node]
    assert complex_equipment_node.citation[1] == complex_citation_node

    # remove optional attributes
    complex_equipment_node.description = ""
    complex_equipment_node.condition = []
    complex_equipment_node.file = []
    complex_equipment_node.citation = []

    # assert that optional attributes have been removed
    assert complex_equipment_node.description == ""
    assert complex_equipment_node.condition == []
    assert complex_equipment_node.file == []
    assert complex_equipment_node.citation == []


def test_integration_equipment(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_process_node, simple_equipment_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_equipment_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]
    simple_project_node.collection[0].experiment = [simple_experiment_node]
    simple_project_node.collection[0].experiment[0].process = [simple_process_node]
    simple_project_node.collection[0].experiment[0].process[0].equipment = [simple_equipment_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].process[0].equipment[0].description = "equipment description UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_equipment_node)
