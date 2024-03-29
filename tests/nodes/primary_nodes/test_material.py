import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


def test_create_complex_material(simple_material_node, simple_computational_forcefield_node, simple_process_node) -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    material_name = "my material name"
    identifier = [{"bigsmiles": "1234"}, {"bigsmiles": "4567"}]
    keyword = ["acetylene"]
    material_notes = "my material notes"

    component = [simple_material_node]
    forcefield = [simple_computational_forcefield_node]

    my_property = [cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")]

    my_material = cript.Material(name=material_name, identifier=identifier, keyword=keyword, component=component, process=simple_process_node, property=my_property, computational_forcefield=forcefield, notes=material_notes)

    assert isinstance(my_material, cript.Material)
    assert my_material.name == material_name
    assert my_material.identifier == identifier
    assert my_material.keyword == keyword
    assert my_material.component == component
    assert my_material.process == simple_process_node
    assert my_material.property == my_property
    assert my_material.computational_forcefield == forcefield
    assert my_material.notes == material_notes


def test_invalid_material_keywords() -> None:
    """
    tries to create a material with invalid keywords and expects to get an Exception
    """
    # with pytest.raises(InvalidVocabulary):
    pass


def test_all_getters_and_setters(simple_material_node, simple_property_node, simple_process_node, simple_computational_forcefield_node) -> None:
    """
    tests the getters and setters for the simple material object

    1. sets every possible attribute for the simple_material object
    2. gets every possible attribute for the simple_material object
    3. asserts that what was set and what was gotten are the same
    """
    # new attributes
    new_name = "new material name"
    new_notes = "new material notes"

    new_identifier = [{"bigsmiles": "6789"}]

    new_parent_material = cript.Material(
        name="my parent material",
        identifier=[
            {"bigsmiles": "9876"},
        ],
    )

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(
            name="my component material 1",
            identifier=[
                {"bigsmiles": "654321"},
            ],
        ),
    ]

    # set all attributes for Material node
    simple_material_node.name = new_name
    simple_material_node.identifier = new_identifier
    simple_material_node.property = [simple_property_node]
    simple_material_node.parent_material = new_parent_material
    simple_material_node.computational_forcefield = simple_computational_forcefield_node
    simple_material_node.keyword = new_material_keywords
    simple_material_node.component = new_components
    simple_material_node.notes = new_notes

    # get all attributes and assert that they are equal to the setter
    assert simple_material_node.name == new_name
    assert simple_material_node.identifier == new_identifier
    assert simple_material_node.property == [simple_property_node]
    assert simple_material_node.parent_material == new_parent_material
    assert simple_material_node.computational_forcefield == simple_computational_forcefield_node
    assert simple_material_node.keyword == new_material_keywords
    assert simple_material_node.component == new_components
    assert simple_material_node.notes == new_notes

    # remove optional attributes
    simple_material_node.property = []
    simple_material_node.parent_material = None
    simple_material_node.computational_forcefield = None
    simple_material_node.component = []
    simple_material_node.notes = ""

    # assert optional attributes have been removed
    assert simple_material_node.property == []
    assert simple_material_node.parent_material is None
    assert simple_material_node.computational_forcefield is None
    assert simple_material_node.component == []
    assert simple_material_node.notes == ""


def test_serialize_material_to_json(complex_material_dict, complex_material_node) -> None:
    """
    tests that it can correctly turn the material node into its equivalent JSON
    """
    # the JSON that the material should serialize to

    # compare dicts because that is more accurate
    ref_dict = json.loads(complex_material_node.get_json(condense_to_uuid={}).json)
    ref_dict = strip_uid_from_dict(ref_dict)

    assert ref_dict == complex_material_dict


def test_integration_material(cript_api, simple_project_node, simple_material_node) -> None:
    """
    integration test between Python SDK and API Client

    tests both POST and GET

    1. create a project
    1. create a material
    1. add a material to project
    1. save the project
    1. get the project
    1. deserialize the project
    1. compare the project node that was sent to API and the one API gave, that they are the same
    """
    # ========= test create =========
    # creating unique name to not bump into unique errors
    simple_project_node.name = f"test_integration_project_name_{uuid.uuid4().hex}"
    simple_material_node.name = f"test_integration_material_name_{uuid.uuid4().hex}"

    simple_project_node.material = [simple_material_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update material attribute to trigger update
    simple_project_node.material[0].identifier = [{"bigsmiles": "my bigsmiles UPDATED"}]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_material_node)
