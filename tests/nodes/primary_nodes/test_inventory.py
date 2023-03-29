import cript
import pytest


def test_create_inventory() -> None:
    """
    tests that an inventory node can be successfully created without errors
    """
    material_1 = cript.Material(name="material 1", identifiers=[{"alternative_names": "material 1 alternative name"}])

    material_2 = cript.Material(name="material 2", identifiers=[{"alternative_names": "material 2 alternative name"}])

    my_inventory = cript.Inventory(materials_list=[material_1, material_2])

    assert isinstance(my_inventory, cript.Inventory)
    assert my_inventory.materials == [material_1, material_2]


@pytest.fixture(scope="session")
def inventory_node():
    """
    create inventory node for other tests to use
    """
    # create an inventory node

    # use inventory node

    # reset inventory node to original state
    pass


def test_get_and_set_inventory() -> None:
    """
    tests that a material list for the inventory node can be gotten and set correctly

    1. create a valid inventory node
    2. set the material's list
    3. get the material's list
    4. assert that the materials list set and the one gotten are the same

    Returns
    -------
    None
    """
    pass


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
