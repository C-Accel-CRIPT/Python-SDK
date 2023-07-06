import json
import uuid

from test_integration import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


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


def test_integration_quantity(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_process_node, simple_ingredient_node, simple_material_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
        Project with material
            Material has ingredient sub-object
    1. GET JSON from API
    1. check their fields equal
    """

    simple_project_node.name = f"test_integration_quantity_{uuid.uuid4().hex}"

    # assemble needed nodes
    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].experiment = [simple_experiment_node]

    # add ingredient to process
    simple_process_node.ingredient = [simple_ingredient_node]

    # continue assembling
    simple_project_node.collection[0].experiment[0].process = [simple_process_node]

    # add orphaned material node to project
    simple_project_node.material = [simple_material_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
