# import json
import uuid
# from deepdiff import DeepDiff
import warnings

import cript


def integrate_nodes_helper(cript_api: cript.API, project_node: cript.Project):
    """
    integration test between Python SDK and API Client
    tests both POST and GET

    comparing JSON because it is easier to compare than an object

    test both the project node:
        * node serialization
        * POST to API
        * GET from API
        * deserialization from API JSON to node JSON
        * compare the JSON of what was sent and what was deserialized from the API
            * the fields they have in common should be the same

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
    * using deepdiff library to do the nested JSON comparisons
    * ignoring the UID field through all the JSON because those the API changes when responding
    """

    # print("\n\n----------------- Project Node ----------------------------")
    # print(project_node.get_json(indent=2, sort_keys=True, condense_to_uuid={}).json)
    # print("--------------------------------------------------------------")
    #
    # cript_api.save(project_node)
    #
    # # get the project that was just saved
    # my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=project_node.name)
    #
    # # get the project from paginator
    # my_project_from_api_dict = my_paginator.current_page_results[0]
    #
    # print("\n\n----------------- API Response Node ----------------------------")
    # print(json.dumps(my_project_from_api_dict, indent=2, sort_keys=True))
    # print("--------------------------------------------------------------")
    #
    # # try to convert api JSON project to node
    # my_project_from_api = cript.load_nodes_from_json(json.dumps(my_project_from_api_dict))
    #
    # print("\n\n------------------- Project Node Deserialized -------------------------")
    # print(my_project_from_api.get_json(indent=2, sort_keys=True, condense_to_uuid={}).json)
    # print("--------------------------------------------------------------")
    #
    # # Configure keys and blocks to be ignored by deepdiff using exclude_regex_path
    # exclude_regex_paths = [r"root(\[.*\])?\['uid'\]"]
    #
    # # Compare the JSONs
    # diff = DeepDiff(json.loads(project_node.json), json.loads(my_project_from_api.json), exclude_regex_paths=exclude_regex_paths)
    #
    # assert len(diff.get("values_changed", {})) == 0

    warnings.warn("Please uncomment `integrate_nodes_helper` to test with the API")
    pass


def everything_project(cript_api, simple_project_node, complex_collection_node, simple_experiment_node, simple_data_node, complex_citation_node):
    """
    A project that has every possible node in its graph and every attribute set.
    * Validating it against DB schema
    * uploading it to the API
    * search for it,
    * get the JSON from API
    * convert it back to the Python node
    """
    # everything project
    simple_project_node.name = f"everything_project_{uuid.uuid4().hex}"

    # everything collection
    simple_project_node.collection = complex_collection_node
    simple_project_node.collection.name = f"everything_collection_{uuid.uuid4().hex}"

    # everything experiment
    simple_project_node.collection[0].experiment = simple_experiment_node
    simple_project_node.collection[0].experiment[0].name = f"everything_experiment_{uuid.uuid4().hex}"
    simple_project_node.collection[0].experiment[0].process = []
    simple_project_node.collection[0].experiment[0].data = [simple_data_node]
    simple_project_node.collection[0].experiment[0].computation = []
    simple_project_node.collection[0].experiment[0].computation_process = []
    simple_project_node.collection[0].experiment[0].funding = ["NSF", "NIH", "DOE", "ERC", "Wellcome Trust"]
    simple_project_node.collection[0].experiment[0].citation = [complex_citation_node]


