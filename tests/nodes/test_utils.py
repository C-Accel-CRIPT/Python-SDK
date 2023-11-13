import cript
from cript.nodes.util import _is_node_field_valid


def test_is_node_field_valid() -> None:
    """
    test the `_is_node_field_valid()` function to be sure it does the node type check correctly

    checks both in places it should be valid and invalid
    """
    assert _is_node_field_valid(node_type_list=["Project"]) is True

    assert _is_node_field_valid(node_type_list=["Project", "Material"]) is False

    assert _is_node_field_valid(node_type_list=[""]) is False

    assert _is_node_field_valid(node_type_list="Project") is False

    assert _is_node_field_valid(node_type_list=[]) is False


def test_load_node_from_json_dict_argument() -> None:
    """
    tests that `cript.load_nodes_from_json` can correctly load the material node from a dict
    instead of JSON string
    """
    material_name = "my material name"
    material_notes = "my material node notes"
    material_bigsmiles = "my bigsmiles"
    material_uuid = "29c796a1-8f08-41ea-8524-29e925f384af"

    material_dict = {
        "node": ["Material"],
        "uid": f"_:{material_uuid}",
        "uuid": material_uuid,
        "name": material_name,
        "notes": material_notes,
        "property": [{"node": ["Property"], "uid": "_:aedce614-7acb-49d2-a2f6-47463f15b707", "uuid": "aedce614-7acb-49d2-a2f6-47463f15b707", "key": "modulus_shear", "type": "value", "value": 5.0, "unit": "GPa"}],
        "computational_forcefield": {"node": ["ComputationalForcefield"], "uid": "_:059952a3-20f2-4739-96bd-a5ea43068065", "uuid": "059952a3-20f2-4739-96bd-a5ea43068065", "key": "amber", "building_block": "atom"},
        "keyword": ["acetylene"],
        "bigsmiles": material_bigsmiles,
    }

    # convert material from dict to node
    my_material_node_from_dict = cript.load_nodes_from_json(nodes_json=material_dict)

    # assert material is correctly deserialized from JSON dict to Material Python object
    assert type(my_material_node_from_dict) == cript.Material
    assert my_material_node_from_dict.name == material_name
    assert my_material_node_from_dict.identifier[0]["bigsmiles"] == "my bigsmiles"

    # convert UUID object to UUID str and compare
    assert str(my_material_node_from_dict.uuid) == material_uuid
