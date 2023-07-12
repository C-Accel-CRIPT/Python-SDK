import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_json(complex_ingredient_node, complex_ingredient_dict):
    i = complex_ingredient_node
    i_dict = json.loads(i.json)
    i_dict["material"] = {}
    j_dict = strip_uid_from_dict(complex_ingredient_dict)
    j_dict["material"] = {}
    assert strip_uid_from_dict(i_dict) == j_dict
    i2 = cript.load_nodes_from_json(i.get_json(condense_to_uuid={}).json)
    ref_dict = strip_uid_from_dict(json.loads(i.get_json(condense_to_uuid={}).json))
    ref_dict["material"] = {}
    ref_dictB = strip_uid_from_dict(json.loads(i2.get_json(condense_to_uuid={}).json))
    ref_dictB["material"] = {}
    assert ref_dict == ref_dictB


def test_getter_setter(complex_ingredient_node, complex_quantity_node, simple_material_node):
    i2 = complex_ingredient_node
    q2 = complex_quantity_node
    i2.set_material(simple_material_node, [complex_quantity_node])
    assert i2.material is simple_material_node
    assert i2.quantity[-1] is q2

    i2.keyword = ["monomer"]
    assert i2.keyword == ["monomer"]


def test_integration_ingredient(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_process_node, simple_ingredient_node, simple_material_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
        Project with material
            Material has ingredient sub-object
    1. GET JSON from API
    1. check their fields equal

    Notes
    ----
    since `ingredient` requires a `quantity` this test also indirectly tests `quantity`
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_ingredient_{uuid.uuid4().hex}"

    # assemble needed nodes
    simple_project_node.collection = [simple_collection_node]
    simple_project_node.collection[0].experiment = [simple_experiment_node]
    simple_project_node.collection[0].experiment[0].process = [simple_process_node]
    simple_project_node.collection[0].experiment[0].process[0].ingredient = [simple_ingredient_node]

    # add orphaned material node to project
    simple_project_node.material = [simple_material_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].process[0].ingredient[0].keyword = ["polymer"]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
