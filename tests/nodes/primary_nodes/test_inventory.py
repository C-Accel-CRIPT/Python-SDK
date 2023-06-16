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


# ---------- Integration tests ----------
def test_integration_inventory(cript_api, simple_project_node, simple_inventory_node):
    """
    integration test between Python SDK and API Client
    tests both POST and GET
    1. create a project
    1. save the project
    1. get the project
    1. deserialize the project to node
    1. convert the new node to JSON
    1. compare the project node JSON that was sent to API and the node the API gave, have the same JSON
    Notes
    -----
    comparing JSON because it is easier to compare than an object
    """

    simple_project_node.collection[0].inventory = [simple_inventory_node]

    # exception handling in case the project node already exists in DB
    try:
        cript_api.save(project=simple_project_node)
    except Exception as error:
        # handling duplicate project name errors
        if "http:409 duplicate item" in str(error):
            pass
        else:
            raise Exception(error)

    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=simple_project_node.name)

    my_project_from_api_dict = my_paginator.current_page_results[0]

    print("\n\n------------------------------------------------------")
    print(json.dumps(my_project_from_api_dict))
    print("------------------------------------------------------")

    print("\n\n------------------------------------------------------")
    print(simple_project_node.json)
    print("------------------------------------------------------")

    # my_project_from_api_node = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))

    # check equivalent JSON dicts
    # assert json.dumps(my_paginator.current_page_results[0]) == simple_project_node.json
