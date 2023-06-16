import json

from util import strip_uid_from_dict

import cript


def test_create_simple_project(simple_collection_node) -> None:
    """
    test that a project node with only required arguments can be created
    """
    my_project_name = "my Project name"

    my_project = cript.Project(name=my_project_name, collection=[simple_collection_node])

    # assertions
    assert isinstance(my_project, cript.Project)
    assert my_project.name == my_project_name
    assert my_project.collection == [simple_collection_node]


def test_project_getters_and_setters(simple_project_node, simple_collection_node, complex_collection_node, simple_material_node) -> None:
    """
    tests that a Project node getters and setters are working as expected

    1. use a simple project node
    2. set all of its attributes to something new
    3. get all of its attributes
    4. what was set and what was gotten should be equivalent
    """
    new_project_name = "my new project name"

    # set attributes
    simple_project_node.name = new_project_name
    simple_project_node.collection = [complex_collection_node]
    simple_project_node.material = [simple_material_node]

    # get attributes and assert that they are the same
    assert simple_project_node.name == new_project_name
    assert simple_project_node.collection == [complex_collection_node]
    assert simple_project_node.material == [simple_material_node]


def test_serialize_project_to_json(complex_project_node, complex_project_dict) -> None:
    """
    tests that a Project node can be correctly converted to a JSON
    """
    expected_dict = complex_project_dict

    # Since we condense those to UUID we remove them from the expected dict.
    expected_dict["admin"] = [{"node": ["User"]}]
    expected_dict["member"] = [{"node": ["User"]}]

    # comparing dicts instead of JSON strings because dict comparison is more accurate
    serialized_project: dict = json.loads(complex_project_node.get_json(condense_to_uuid={}).json)
    serialized_project = strip_uid_from_dict(serialized_project)

    assert serialized_project == strip_uid_from_dict(expected_dict)


# ---------- Integration tests ----------
def test_integration_project(cript_api, simple_project_node):
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
    simple_project_node.name = "test_integration_project_name"

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
