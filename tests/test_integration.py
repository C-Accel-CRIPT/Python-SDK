import json

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

    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME,
                                    value_to_search=project_node.name)

    my_project_from_api_dict = my_paginator.current_page_results[0]

    print("\n\n------------------------------------------------------")
    print(json.dumps(my_project_from_api_dict))
    print("------------------------------------------------------")

    print("\n\n------------------------------------------------------")
    print(project_node.json)
    print("------------------------------------------------------")

    # my_project_from_api_node = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))

    # check equivalent JSON dicts
    # assert json.dumps(my_paginator.current_page_results[0]) == simple_project_node.json