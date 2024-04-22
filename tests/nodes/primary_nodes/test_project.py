import copy
import json
import time
import uuid

import pytest

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


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
    new_project_notes = "my new project notes"

    # set attributes
    simple_project_node.name = new_project_name
    simple_project_node.collection = [complex_collection_node]
    simple_project_node.material = [simple_material_node]
    simple_project_node.notes = new_project_notes

    # get attributes and assert that they are the same
    assert simple_project_node.name == new_project_name
    assert simple_project_node.collection == [complex_collection_node]
    assert simple_project_node.material == [simple_material_node]
    assert simple_project_node.notes == new_project_notes

    # remove optional attributes
    simple_project_node.collection = []
    simple_project_node.material = []
    simple_project_node.notes = ""

    # assert optional attributes have been removed
    assert simple_project_node.collection == []
    assert simple_project_node.material == []
    assert simple_project_node.notes == ""


def test_serialize_project_to_json(complex_project_node, complex_project_dict) -> None:
    """
    tests that a Project node can be correctly converted to a JSON
    """
    expected_dict = complex_project_dict

    # Since we condense those to UUID we remove them from the expected dict.
    expected_dict["admin"] = [{}]
    expected_dict["member"] = [{}]

    # comparing dicts instead of JSON strings because dict comparison is more accurate
    serialized_project: dict = json.loads(complex_project_node.get_json(condense_to_uuid={}).json)
    serialized_project = strip_uid_from_dict(serialized_project)

    assert serialized_project == strip_uid_from_dict(expected_dict)


def test_integration_project(cript_api, simple_project_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_project_name_{uuid.uuid4().hex}"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    simple_project_node.notes = "project notes UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_project_node)


# @pytest.mark.skip(reason="api, and we overrode save_new to save ")


def test_save_project_change_material(cript_api, simple_project_node, complex_project_node):
    """

    pytest nodes/primary_nodes/test_project.py::test_save_project_change_material
    """

    # Modify deep in the tree
    proj0 = copy.deepcopy(complex_project_node)
    print("----proj0 w name")
    epoch_name = str(int(time.time()))
    proj0.name = f"sure to be a new name {epoch_name}"
    print(proj0.name)

    proj_json = proj0.get_expanded_json()  # .get_json().json
    cript_api.save(proj0)
    # --- finished save --- now load node
    # making sure this is a different object loaded , instead of comparing the same object
    proj_loaded, proj_cache = cript.load_nodes_from_json(nodes_json=proj_json, _use_uuid_cache={})

    print("~~ proj_loaded")
    print(proj_loaded)
    print("\n")
    print("type ~~ proj_loaded")
    print(type(proj_loaded))
    print("proj_loaded.collection")
    print(proj_loaded.collection[0])
    print(proj_loaded.collection[0].inventory[0])
    try:
        print(proj_loaded.collection[0].inventory[0].material[0])
    except:
        print("we didnt get material in inventory")
        print("somehow we are not saving materials to inventory")
    quit()

    material_to_modify = proj_loaded.collection[0].inventory[0].material[0]

    material_to_modify.name = "this is sure to be a new name"
    # Delete a node
    proj_loaded.material[0].property = []
    cript_api.save(proj_loaded)
    # now we need to reload the test in
    proj_loaded2, proj2_cache = cript.load_nodes_from_json(nodes_json=proj_loaded.get_expanded_json(), _use_uuid_cache={})
    # asserting
    assert proj_loaded2.collection[0].inventory[0].material[0].name == "this is sure to be a new name"
