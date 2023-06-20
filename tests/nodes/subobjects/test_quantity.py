import json

from util import strip_uid_from_dict

import cript
from tests.test_integration import integrate_nodes_helper


def test_json(complex_quantity_node, complex_quantity_dict):
    q = complex_quantity_node
    q_dict = json.loads(q.json)
    assert strip_uid_from_dict(q_dict) == complex_quantity_dict
    q2 = cript.load_nodes_from_json(q.json)
    assert q2.json == q.json


def test_getter_setter(complex_quantity_node):
    q = complex_quantity_node
    q.value = 0.5
    assert q.value == 0.5
    q.set_uncertainty(0.1, "stderr")
    assert q.uncertainty == 0.1
    assert q.uncertainty_type == "stderr"

    q.set_key_unit("volume", "m**3")
    assert q.key == "volume"
    assert q.unit == "m**3"


def test_integration_quantity(cript_api, simple_project_node, simple_material_node, complex_material_node, simple_process_node, complex_ingredient_node, complex_quantity_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
        Project with material
            Material has ingredient sub-object
    1. GET JSON from API
    1. check their fields equal
    """

    # add quantity to ingredient
    complex_ingredient_node.set_material = [simple_material_node, complex_quantity_node]

    # add ingredient to process
    simple_process_node.ingredient = [complex_ingredient_node]

    # add process to experiment
    simple_project_node.collection[0].experiment[0].process = [simple_process_node]

    # TODO getting CRIPTOrphanedProcessError
    simple_project_node.material = [simple_material_node, complex_material_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
