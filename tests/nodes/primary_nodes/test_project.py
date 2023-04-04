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


def test_project_getters_and_setters(
    simple_project_node, simple_collection_node, complex_collection_node, simple_material_node
) -> None:
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


def test_serialize_project_to_json(complex_project_node) -> None:
    """
    tests that a Project node can be correctly converted to a JSON
    """
    expected_dict: dict = {
        "node": "Project",
        "name": "my project name",
        "collections": [
            {
                "name": "my complex collection name",
                "node": "Collection",
                "citations": [
                    {
                        "node": "Citation",
                        "reference": {
                            "authors": None,
                            "node": "Reference",
                            "pages": None,
                            "title": "'Living' Polymers",
                            "type": "journal_article",
                        },
                        "type": "derived_from",
                    }
                ],
                "cript_doi": "10.1038/1781168a0",
                "experiments": [{"name": "my experiment name", "node": "Experiment"}],
                "inventories": [
                    {
                        "node": "Inventory",
                        "materials": [
                            {
                                "identifiers": [{"alternative_names": "material 1 alternative name"}],
                                "name": "material 1",
                                "node": "Material",
                            },
                            {
                                "identifiers": [{"alternative_names": "material 2 alternative name"}],
                                "name": "material 2",
                                "node": "Material",
                            },
                        ],
                    }
                ],
            }
        ],
        "materials": [
            {
                "node": "Material",
                "name": "my complex material",
                "components": [
                    {
                        "identifiers": [{"alternative_names": "component 1 alternative name"}],
                        "name": "my component material 1",
                        "node": "Material",
                    },
                    {
                        "identifiers": [{"alternative_names": "component 2 alternative name"}],
                        "name": "my component material 2",
                        "node": "Material",
                    },
                ],
                "computation_forcefield": {"building_block": "atom", "key": "amber", "node": "ComputationForcefield"},
                "identifiers": [{"alternative_names": "my material alternative name"}],
                "keywords": ["acetylene"],
                "parent_materials": {
                    "identifiers": [{"alternative_names": "parent material 1"}],
                    "name": "my parent material",
                    "node": "Material",
                },
                "process": {"keywords": [], "node": "Process", "type": "affinity_pure"},
                "properties": {"key": "modulus_shear", "node": "Property", "type": "min", "unit": "gram", "value": 1.23},
            }
        ],
    }

    # comparing dicts instead of JSON strings because dict comparison is more accurate
    assert json.loads(complex_project_node.json) == expected_dict
