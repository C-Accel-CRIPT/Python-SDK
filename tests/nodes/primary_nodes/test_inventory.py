import json
import uuid

from util import strip_uid_from_dict

import cript
from tests.test_integration import integrate_nodes_helper


def test_get_and_set_inventory(simple_inventory_node) -> None:
    """
    tests that a material list for the inventory node can be gotten and set correctly

    1. create new material node
    2. set the material's list
    3. get the material's list
        1. originally in simple_inventory it has 2 materials, but after the setter it should have only 1
    4. assert that the materials list set and the one gotten are the same
    """
    # create new materials
    material_1 = cript.Material(name="new material 1", identifiers=[{"names": ["new material 1 alternative name"]}])

    # set inventory materials
    simple_inventory_node.material = [material_1]

    # get and check inventory materials
    assert isinstance(simple_inventory_node, cript.Inventory)
    assert simple_inventory_node.material[-1] == material_1


def test_inventory_serialization(simple_inventory_node, simple_material_dict) -> None:
    """
    test that the inventory is correctly serializing into JSON

    1. converts inventory json string to dict
    2. strips the UID from all the nodes within that dict
    3. compares the expected_dict written to what JSON deserializes
    """
    expected_dict = {"node": ["Inventory"], "name": "my inventory name", "material": [simple_material_dict, {"node": ["Material"], "name": "material 2", "bigsmiles": "my big smiles"}]}

    # TODO this needs better testing
    # force not condensing to edge uuid during json serialization
    deserialized_inventory: dict = json.loads(simple_inventory_node.get_json(condense_to_uuid={}).json)
    deserialized_inventory = strip_uid_from_dict(deserialized_inventory)

    assert expected_dict == deserialized_inventory


def test_integration_inventory(cript_api, simple_project_node, simple_inventory_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # putting UUID in name so it doesn't bump into uniqueness errors
    simple_project_node.name = f"project_name_{uuid.uuid4().hex}"
    simple_project_node.collection[0].name = f"collection_name_{uuid.uuid4().hex}"
    simple_inventory_node.name = f"inventory_name_{uuid.uuid4().hex}"

    simple_project_node.collection[0].inventory = [simple_inventory_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
