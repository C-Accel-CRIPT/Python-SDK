import json

import pytest
from conftest import HAS_INTEGRATION_TESTS_ENABLED
from deepdiff import DeepDiff

import cript
from cript.api.exceptions import APIError
from cript.nodes.uuid_base import UUIDBaseNode


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

    # TODO this is temporary and must be removed
    developer_name = "Navid"

    if not HAS_INTEGRATION_TESTS_ENABLED:
        pytest.skip("Integration tests with API requires real API and Storage token")
        return

    print("\n\n=================== Project Node ============================")
    if developer_name == "Navid":
        print(project_node.get_json(sort_keys=False).json)
    else:
        print(project_node.get_json(sort_keys=False, condense_to_uuid={}, indent=2).json)
    print("==============================================================")

    cript_api.save(project_node)

    # get the project that was just saved
    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=project_node.name)

    # get the project from paginator
    my_project_from_api_dict = my_paginator.current_page_results[0]

    print("\n\n================= API Response Node ============================")
    if developer_name == "Navid":
        print(json.dumps(my_project_from_api_dict, sort_keys=False))
    else:
        print(json.dumps(my_project_from_api_dict, sort_keys=False, indent=2))
    print("==============================================================")

    # Configure keys and blocks to be ignored by deepdiff using exclude_regex_path
    # ignores all UID within the JSON because those will always be different
    # and ignores elements that the back ends to graphs.
    exclude_regex_paths = [
        r"root(\[.*\])?\['uid'\]",
        r"root\['\w+_count'\]",  # All the attributes that end with _count
        r"root(\[.*\])?\['\w+_count'\]",  # All the attributes that end with _count
        r"root(\[.*\])?\['locked'\]",
        r"root(\[.*\])?\['admin'\]",
        r"root(\[.*\])?\['created_at'\]",
        r"root(\[.*\])?\['created_by'\]",
        r"root(\[.*\])?\['updated_at'\]",
        r"root(\[.*\])?\['updated_by'\]",
        r"root(\[.*\])?\['public'\]",
        r"root(\[.*\])?\['notes'\]",
        r"root(\[.*\])?\['model_version'\]",
    ]
    # Compare the JSONs
    diff = DeepDiff(json.loads(project_node.json), my_project_from_api_dict, exclude_regex_paths=exclude_regex_paths)
    # with open("la", "a") as file_handle:
    #     file_handle.write(str(diff) + "\n")

    print("diff", diff)
    # assert not list(diff.get("values_changed", []))
    # assert not list(diff.get("dictionary_item_removed", []))
    # assert not list(diff.get("dictionary_item_added", []))

    # try to convert api JSON project to node
    my_project_from_api = cript.load_nodes_from_json(json.dumps(my_project_from_api_dict))
    print("\n\n=================== Project Node Deserialized =========================")
    if developer_name == "Navid":
        print(my_project_from_api.get_json(sort_keys=False).json)
    else:
        print(my_project_from_api.get_json(sort_keys=False, condense_to_uuid={}, indent=2).json)
    print("==============================================================")
    print("\n\n\n######################################## TEST Passed ########################################\n\n\n")


def delete_integration_node_helper(cript_api: cript.API, node_to_delete: UUIDBaseNode) -> None:
    """
    1. takes the node/sub-object that needs to be deleted
    1. checks that it first exists on the API before deleting
    1. sends an HTTP DELETE to API
    1. asserts that the API response is 200
    1. tries to get the same node via UUID from the API and expects that it should fail

    Notes
    ------
    > for future it should also take the project that the node was in, and get the project again
    > then compare that the node was successfully deleted/missing from the project
    """

    if not HAS_INTEGRATION_TESTS_ENABLED:
        pytest.skip("DELETE integration tests with API requires real API and Storage token")
        return

    # check that the node we want to delete first exists on the API
    my_node_paginator = cript_api.search(
        # passing in the full node to get the node type from
        node_type=node_to_delete,
        search_mode=cript.SearchModes.UUID,
        value_to_search=str(node_to_delete.uuid)
    )

    assert len(my_node_paginator.current_page_results) == 1

    # DELETE the project from API
    cript_api.delete(node=node_to_delete)

    # should not be able to get node by UUID anymore because it is deleted and should get an error
    with pytest.raises(APIError):
        cript_api.search(
            node_type=node_to_delete,
            search_mode=cript.SearchModes.UUID,
            value_to_search=str(node_to_delete.uuid)
        )

