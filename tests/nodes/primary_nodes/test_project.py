import copy
import json
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


@pytest.mark.skip(reason="api")
def test_save_project_node(cript_api, simple_project_node, complex_project_node):
    """
    pytest nodes/primary_nodes/test_project.py::test_save_project_node
    """

    # with cript.API(host="https://lb-stage.mycriptapp.org/") as api:
    #     with open("new_project.json") as json_handle:
    #         proj_json = json.load(json_handle)

    # proj = cript_api.load_nodes_from_json(nodes_json=proj_json)
    # Modify deep in the tree
    print("------------\nstarting")
    proj0 = copy.deepcopy(complex_project_node)
    proj_json = proj0.get_json().json
    cript_api.save_new(proj0)

    proj = cript.load_nodes_from_json(nodes_json=json.dumps(proj_json))
    print("\n----proj_loaded")
    print(proj)

    print("------------\n1111111")
    print(type(proj))
    print("why is this returning a string and not a node?")
    quit()
    print(proj.get_json().json)
    material_to_modify = proj.collection[0].inventory[0].material[0]
    print("\n\nproj.collection[0].inventory[0].material[0]")
    print(proj.collection[0].inventory[0].material[0])
    material_to_modify.name = "this is sure to be a new name"

    # Delete a node
    proj.material[0].property = []

    cript_api.save_new(proj)

    # now we need to reload the test in

    print("------------\n2222222")
    print(proj.get_json().json)
    quit()
