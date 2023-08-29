import json
import uuid

from integration_test_helper import (
    delete_integration_node_helper,
    integrate_nodes_helper,
)
from util import strip_uid_from_dict

import cript


def test_json(complex_quantity_node, complex_quantity_dict):
    q = complex_quantity_node
    q_dict = json.loads(q.json)
    assert strip_uid_from_dict(q_dict) == complex_quantity_dict
    q2 = cript.load_nodes_from_json(q.json)
    assert q2.json == q.json


def test_getter_setter(complex_quantity_node):
    complex_quantity_node.value = 0.5
    assert complex_quantity_node.value == 0.5

    complex_quantity_node.set_uncertainty(uncertainty=0.1, type="stderr")
    assert complex_quantity_node.uncertainty == 0.1
    assert complex_quantity_node.uncertainty_type == "stderr"

    complex_quantity_node.set_key_unit(new_key="volume", new_unit="m**3")
    assert complex_quantity_node.key == "volume"
    assert complex_quantity_node.unit == "m**3"

    # remove optional attributes
    complex_quantity_node.set_uncertainty(uncertainty=None, type="")

    # assert optional attributes have been removed
    assert complex_quantity_node.uncertainty is None
    assert complex_quantity_node.uncertainty_type == ""


def test_integration_quantity(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_process_node, simple_ingredient_node, simple_material_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
        Project with material
            Material has ingredient sub-object
    1. GET JSON from API
    1. check their fields equal
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_quantity_{uuid.uuid4().hex}"

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
    simple_project_node.collection[0].experiment[0].process[0].ingredient[0].quantity[0].value = 123456789
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    # isolate quantity from ingredient
    quantity_subobject: cript.Quantity = simple_ingredient_node.quantity[0]

    # each ingredient is required to have a quantity,
    # so deleting the only quantity that it has is illegal because then it would make it invalid
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=quantity_subobject)
