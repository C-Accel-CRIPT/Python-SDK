import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_json(complex_property_node, complex_property_dict):
    p = complex_property_node
    p_dict = strip_uid_from_dict(json.loads(p.get_json(condense_to_uuid={}).json))
    assert p_dict == complex_property_dict
    p2 = cript.load_nodes_from_json(p.get_json(condense_to_uuid={}).json)

    assert strip_uid_from_dict(json.loads(p2.get_json(condense_to_uuid={}).json)) == strip_uid_from_dict(json.loads(p.get_json(condense_to_uuid={}).json))


def test_setter_getter(complex_property_node, simple_material_node, simple_process_node, complex_condition_node, simple_data_node, simple_computation_node, complex_citation_node):
    p2 = complex_property_node
    p2.key = "modulus_loss"
    assert p2.key == "modulus_loss"
    p2.type = "min"
    assert p2.type == "min"
    p2.set_value(600.1, "MPa")
    assert p2.value == 600.1
    assert p2.unit == "MPa"

    p2.set_uncertainty(10.5, "stdev")
    assert p2.uncertainty == 10.5
    assert p2.uncertainty_type == "stdev"

    p2.component += [simple_material_node]
    assert p2.component[-1] is simple_material_node
    p2.structure = "structure2"
    assert p2.structure == "structure2"

    p2.method = "scale"
    assert p2.method == "scale"

    p2.sample_preparation = simple_process_node
    assert p2.sample_preparation is simple_process_node
    assert len(p2.condition) == 1
    p2.condition += [complex_condition_node]
    assert len(p2.condition) == 2
    p2.data = [simple_data_node]
    assert p2.data[0] is simple_data_node

    p2.computation += [simple_computation_node]
    assert p2.computation[-1] is simple_computation_node

    assert len(p2.citation) == 1
    cit2 = copy.deepcopy(complex_citation_node)
    p2.citation += [cit2]
    assert len(p2.citation) == 2
    assert p2.citation[-1] == cit2
    p2.notes = "notes2"
    assert p2.notes == "notes2"


def test_integration_material_property(cript_api, simple_project_node, simple_material_node, simple_property_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
        Project with material
            Material has property sub-object
    1. GET JSON from API
    1. check their fields equal
    """
    # ========= test create =========
    # rename property and material to avoid duplicate node API error
    simple_project_node.name = f"test_integration_material_property_{uuid.uuid4().hex}"
    simple_material_node.name = f"{simple_material_node.name}_{uuid.uuid4().hex}"

    simple_project_node.material = [simple_material_node]
    simple_project_node.material[0].property = [simple_property_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.material[0].property[0].notes = "property sub-object notes UPDATED"
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
