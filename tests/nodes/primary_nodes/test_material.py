import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_create_complex_material(simple_material_node, simple_computational_forcefield_node, simple_process_node) -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    material_name = "my material name"
    identifiers = [{"bigsmiles": "1234"}, {"bigsmiles": "4567"}]
    keyword = ["acetylene"]

    component = [simple_material_node]
    forcefield = [simple_computational_forcefield_node]

    my_property = [cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")]

    my_material = cript.Material(name=material_name, identifiers=identifiers, keyword=keyword, component=component, process=simple_process_node, property=my_property, computational_forcefield=forcefield)

    assert isinstance(my_material, cript.Material)
    assert my_material.name == material_name
    assert my_material.identifiers == identifiers
    assert my_material.keyword == keyword
    assert my_material.component == component
    assert my_material.process == simple_process_node
    assert my_material.property == my_property
    assert my_material.computational_forcefield == forcefield


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

    new_identifiers = [{"bigsmiles": "6789"}]

    new_parent_material = cript.Material(
        name="my parent material",
        identifiers=[
            {"bigsmiles": "9876"},
        ],
    )

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(
            name="my component material 1",
            identifiers=[
                {"bigsmiles": "654321"},
            ],
        ),
    ]

    # set all attributes for Material node
    simple_material_node.name = new_name
    simple_material_node.identifiers = new_identifiers
    simple_material_node.property = [simple_property_node]
    simple_material_node.parent_material = new_parent_material
    simple_material_node.computational_forcefield = simple_computational_forcefield_node
    simple_material_node.keyword = new_material_keywords
    simple_material_node.component = new_components

    # get all attributes and assert that they are equal to the setter
    assert simple_material_node.name == new_name
    assert simple_material_node.identifiers == new_identifiers
    assert simple_material_node.property == [simple_property_node]
    assert simple_material_node.parent_material == new_parent_material
    assert simple_material_node.computational_forcefield == simple_computational_forcefield_node
    assert simple_material_node.keyword == new_material_keywords
    assert simple_material_node.component == new_components


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

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update material attribute to trigger update
    simple_project_node.material[0].identifiers = [{"bigsmiles": "my bigsmiles UPDATED"}]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
