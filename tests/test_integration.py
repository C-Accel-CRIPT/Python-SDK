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

    # TODO needs more explanation of the deepDiff and how it works
    """

    cript_api.save(project=project_node)

    # get the project that was just saved
    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME,
                                    value_to_search=project_node.name)

    # get the project from paginator
    my_project_from_api_dict = my_paginator.current_page_results[0]

    # try to convert api JSON project to node
    my_project_from_api = cript.load_nodes_from_json(json.dumps(my_project_from_api_dict))

    # Configure keys and blocks to be ignored by deepdiff using exclude_regex_path
    exclude_regex_paths = [
        r"root(\[.*\])?\['uid'\]"
    ]

    # Compare the JSONs
    diff = DeepDiff(json.loads(project_node.json), json.loads(my_project_from_api.json),
                    exclude_regex_paths=exclude_regex_paths)

    assert len(diff.get("values_changed", {})) == 0
