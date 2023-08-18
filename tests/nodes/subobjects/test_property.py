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
    complex_property_node.key = "modulus_loss"
    assert complex_property_node.key == "modulus_loss"

    complex_property_node.type = "min"
    assert complex_property_node.type == "min"

    complex_property_node.set_value(600.1, "MPa")
    assert complex_property_node.value == 600.1
    assert complex_property_node.unit == "MPa"

    complex_property_node.set_uncertainty(10.5, "stdev")
    assert complex_property_node.uncertainty == 10.5
    assert complex_property_node.uncertainty_type == "stdev"

    complex_property_node.component += [simple_material_node]
    assert complex_property_node.component[-1] is simple_material_node
    complex_property_node.structure = "structure2"
    assert complex_property_node.structure == "structure2"

    complex_property_node.method = "scale"
    assert complex_property_node.method == "scale"

    complex_property_node.sample_preparation = simple_process_node
    assert complex_property_node.sample_preparation is simple_process_node

    assert len(complex_property_node.condition) == 1
    complex_property_node.condition += [complex_condition_node]
    assert len(complex_property_node.condition) == 2

    complex_property_node.data = [simple_data_node]
    assert complex_property_node.data[0] is simple_data_node

    complex_property_node.computation += [simple_computation_node]
    assert complex_property_node.computation[-1] is simple_computation_node

    assert len(complex_property_node.citation) == 1
    cit2 = copy.deepcopy(complex_citation_node)
    complex_property_node.citation += [cit2]
    assert len(complex_property_node.citation) == 2
    assert complex_property_node.citation[-1] == cit2

    complex_property_node.notes = "notes2"
    assert complex_property_node.notes == "notes2"

    # remove optional attributes
    complex_property_node.set_value(new_value=None, new_unit="")
    complex_property_node.set_uncertainty(new_uncertainty=None, new_uncertainty_type="")
    complex_property_node.component = []
    complex_property_node.structure = ""
    complex_property_node.method = ""
    complex_property_node.sample_preparation = None
    complex_property_node.condition = []
    complex_property_node.data = []
    complex_property_node.computation = []
    complex_property_node.citation = []
    complex_property_node.notes = ""
    
    # assert optional attributes have been removed
    assert complex_property_node.value is None
    assert complex_property_node.unit == ""
    assert complex_property_node.uncertainty is None
    assert complex_property_node.uncertainty_type == ""
    assert complex_property_node.component == []
    assert complex_property_node.structure == ""
    assert complex_property_node.method == ""
    assert complex_property_node.sample_preparation is None
    assert complex_property_node.condition == []
    assert complex_property_node.data == []
    assert complex_property_node.computation == []
    assert complex_property_node.citation == []
    assert complex_property_node.notes == ""


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
