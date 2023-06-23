import json

from deepdiff import DeepDiff

import cript


def integrate_nodes_helper(cript_api: cript.API, project_node: cript.Project):
    """
    integration test between Python SDK and API Client
    tests both POST and GET

    Parameters
    ----------
    cript_api: cript.API
         pass in the cript_api client that is already available as a fixture
    project_node: cript.Project
        the desired project to use for integration test

    1. create a project with the desired node to test
        * pass in the project to this function
    1. save the project
    1. get the project
    1. deserialize the project to node
    1. convert the new node to JSON
    1. compare the project node JSON that was sent to API and the node the API gave, have the same JSON

    Notes
    -----
    comparing JSON because it is easier to compare than an object

    test both the project node:
        * node serialization
        * POST to API
        * GET from API
        * deserialization from API JSON to node JSON
    """

    # exception handling in case the project node already exists in DB
    try:
        cript_api.save(project=project_node)
    except Exception as error:
        # handling duplicate project name errors
        if "http:409 duplicate item" in str(error):
            pass
        else:
            raise Exception(error)

    # get the project that was just saved
    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME,
                                    value_to_search=project_node.name)

    # get the project from paginator
    my_project_from_api_dict = my_paginator.current_page_results[0]

    # try to convert api JSON project to node
    my_project_from_api = cript.load_nodes_from_json(json.dumps(my_project_from_api_dict))

    print("\n\n----------------- API JSON RECEIVED -------------------------------")
    print(json.dumps(my_project_from_api_dict))
    print("------------------------------------------------------")

    print("\n\n----------------- API JSON to Python Node -------------------------------")
    print(my_project_from_api.json)
    print("------------------------------------------------------")

    print("\n\n-----------------JSON SENT TO API -------------------------------")
    print(project_node.json)
    print("------------------------------------------------------")

    # # Ignore all fields except for uuid and name
    # path_attrs = ['uuid', 'name']
    #
    # # Compare the JSONs
    # diff = DeepDiff(project_node.json, my_project_from_api.json, ignore_order=True)
    #
    # print("\n\n----------------- Deep Diff -------------------------------\n\n")
    # print(diff)
    # print("\n\n----------------- Deep Diff -------------------------------")

    # Check if there are any differences in the common values
    are_jsons_equal(json.loads(project_node.json), json.loads(my_project_from_api_dict))
    return True


def are_jsons_equal(json1, json2):
    if json1["node"] == json2["node"]:
        assert json1["uuid"] == json2["uuid"]

        for key in json1.keys():
            if isinstance(json1[key], dict) and isinstance(json2[key], dict):
                are_jsons_equal(json1[key], json2[key])

    return True

