import json

import cript


def test_create_simple_project(simple_collection_node) -> None:
    """
    test that a project node with only required arguments can be created
    """
    my_project_name = "my Project name"

    my_project = cript.Project(name=my_project_name, collections=[simple_collection_node])

    # assertions
    assert isinstance(my_project, cript.Project)
    assert my_project.name == my_project_name
    assert my_project.collections == [simple_collection_node]


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
    simple_project_node.collections = [complex_collection_node]
    simple_project_node.materials = [simple_material_node]

    # get attributes and assert that they are the same
    assert simple_project_node.name == new_project_name
    assert simple_project_node.collections == [complex_collection_node]
    assert simple_project_node.materials == [simple_material_node]


def test_serialize_project_to_json(simple_project_node) -> None:
    """
    tests that a Project node can be correctly converted to a JSON
    """
    expected_dict: dict = {
        "node": ["Project"],
        "name": "my Project name",
        "collections": [
            {
                "node": ["Collection"],
                "name": "my collection name",
                "experiments": [{"node": ["Experiment"], "name": "my experiment name"}],
                "inventories": [],
                "citations": [],
            }
        ],
    }

    # comparing dicts instead of JSON strings because dict comparison is more accurate
    assert json.loads(simple_project_node.json) == expected_dict


# ---------- Integration tests ----------
def test_save_project_to_api() -> None:
    """
    tests if the project node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_project_from_api() -> None:
    """
    gets the project node from the api that was saved prior
    """
    pass


def test_serialize_json_to_project() -> None:
    """
    tests that a JSON of a project node from API can be correctly converted to python object
    """
    pass


def test_update_project_in_api() -> None:
    """
    tests that the project node can be correctly updated within the API
    """
    pass


def test_delete_project_from_api() -> None:
    """
    integration test: tests that the project node can be deleted correctly from the API
    tries to get the project from API, and it is expected for the API to give an error response
    """
    pass
