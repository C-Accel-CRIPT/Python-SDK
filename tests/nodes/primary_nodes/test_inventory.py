import json

import cript


def test_get_and_set_inventory(simple_inventory_node) -> None:
    """
    tests that a material list for the inventory node can be gotten and set correctly

    1. create new material nodes
    2. set the material's list
    3. get the material's list
    4. assert that the materials list set and the one gotten are the same
    """
    # create new materials
    material_1 = cript.Material(name="new material 1", identifiers=[{"alternative_names": "new material 1 alternative name"}])

    material_2 = cript.Material(name="new material 2", identifiers=[{"alternative_names": "new material 2 alternative name"}])

    # set inventory materials
    simple_inventory_node.materials = [material_1, material_2]

    # get and check inventory materials
    assert isinstance(simple_inventory_node, cript.Inventory)
    assert simple_inventory_node.materials == [material_1, material_2]


def test_inventory_serialization(simple_inventory_node) -> None:
    """
    test that the inventory is correctly serializing into JSON
    """
    expected_dict = {
        "node": ["Inventory"],
        "name": "my inventory name",
        "materials": [
            {"node": ["Material"], "name": "material 1", "identifiers": [{"alternative_names": "material 1 alternative name"}]},
            {
                "node": ["Material"],
                "name": "material 2",
                "identifiers": [{"alternative_names": "material 2 alternative name"}],
            },
        ],
    }

    # TODO this needs better testing
    assert expected_dict == json.loads(simple_inventory_node.json)


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
