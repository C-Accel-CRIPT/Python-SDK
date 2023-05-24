import json

from util import strip_uid_from_dict

import cript


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


# --------------- Integration Tests ---------------
def test_save_inventory(cript_api) -> None:
    """
    test that an inventory node can be saved correctly to the API

    Notes
    -----
    indirectly tests getting an inventory node

    1. create a valid inventory node
    2. convert inventory node to JSON
    3. convert JSON to node
    4. assert that both nodes are equal to each other

    Returns
    -------
    None
    """
    pass


def test_get_inventory_from_api(cript_api) -> None:
    """
    test getting inventory node from the API
    """
    pass


def test_update_inventory(cript_api) -> None:
    """
    test an inventory node can be correctly updated in the API

    Notes
    -----
    This test indirectly tests that the node can be gotten correctly.

    Returns
    -------
    None
    """
    pass


def test_delete_inventory(cript_api) -> None:
    """
    simply test that an inventory node can be correctly deleted from the API

    Returns
    -------
    None
    """
