import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_simple_process() -> None:
    """
    tests that a simple process node can be correctly created
    """

    # process fields
    my_process_type = "affinity_pure"
    my_process_description = "my simple material description"
    my_process_keywords = ["anionic"]

    # create process node
    my_process = cript.Process(name="my process name", type=my_process_type, description=my_process_description, keyword=my_process_keywords)

    # assertions
    assert isinstance(my_process, cript.Process)
    assert my_process.type == my_process_type
    assert my_process.description == my_process_description
    assert my_process.keyword == my_process_keywords


def test_complex_process_node(complex_ingredient_node, simple_equipment_node, complex_citation_node, simple_property_node, simple_condition_node, simple_material_node, simple_process_node, complex_equipment_node, complex_condition_node) -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """
    # TODO clean up this test and use fixtures from conftest.py

    my_process_name = "my complex process node name"
    my_process_type = "affinity_pure"
    my_process_description = "my simple material description"

    process_waste = [
        cript.Material(name="my process waste material 1", identifiers=[{"bigsmiles": "process waste bigsmiles"}]),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    # create complex process
    citation = copy.deepcopy(complex_citation_node)
    prop = cript.Property("n_neighbor", "value", 2.0, None)

    my_complex_process = cript.Process(
        name=my_process_name,
        type=my_process_type,
        ingredient=[complex_ingredient_node],
        description=my_process_description,
        equipment=[complex_equipment_node],
        product=[simple_material_node],
        waste=process_waste,
        prerequisite_process=[simple_process_node],
        condition=[complex_condition_node],
        property=[prop],
        keyword=my_process_keywords,
        citation=[citation],
    )
    # assertions
    assert my_complex_process.type == my_process_type
    assert my_complex_process.ingredient == [complex_ingredient_node]
    assert my_complex_process.description == my_process_description
    assert my_complex_process.equipment == [complex_equipment_node]
    assert my_complex_process.product == [simple_material_node]
    assert my_complex_process.waste == process_waste
    assert my_complex_process.prerequisite_process[-1] == simple_process_node
    assert my_complex_process.condition[-1] == complex_condition_node
    assert my_complex_process.property[-1] == prop
    assert my_complex_process.keyword[-1] == my_process_keywords[-1]
    assert my_complex_process.citation[-1] == citation


def test_process_getters_and_setters(
    simple_process_node,
    complex_ingredient_node,
    complex_equipment_node,
    simple_material_node,
    complex_condition_node,
    simple_property_node,
    complex_citation_node,
) -> None:
    """
    test getters and setters and be sure they are working correctly

    1. set simple_process_node attributes to something new
    2. get all attributes and check that they have been set correctly

    Notes
    -----
    indirectly tests setting the data type to correct vocabulary
    """
    new_process_type = "blow_molding"
    new_process_description = "my new process description"
    new_process_keywords = "annealing_sol"

    # test setters
    simple_process_node.type = new_process_type
    simple_process_node.ingredient = [complex_ingredient_node]
    simple_process_node.description = new_process_description
    equipment = complex_equipment_node
    simple_process_node.equipment = [equipment]
    product = simple_material_node
    simple_process_node.product = [product]
    simple_process_node.waste = [simple_material_node]
    simple_process_node.prerequisite_process = [simple_process_node]
    simple_process_node.condition = [complex_condition_node]
    prop = cript.Property("n_neighbor", "value", 2.0, None)
    simple_process_node.property += [prop]
    simple_process_node.keyword = [new_process_keywords]
    citation = copy.deepcopy(complex_citation_node)
    simple_process_node.citation = [citation]

    # test getters
    assert simple_process_node.type == new_process_type
    assert simple_process_node.ingredient == [complex_ingredient_node]
    assert simple_process_node.description == new_process_description
    assert simple_process_node.equipment[-1] == equipment
    assert simple_process_node.product[-1] == product
    assert simple_process_node.waste == [simple_material_node]
    assert simple_process_node.prerequisite_process == [simple_process_node]
    assert simple_process_node.condition == [complex_condition_node]
    assert simple_process_node.property[-1] == prop
    assert simple_process_node.keyword == [new_process_keywords]
    assert simple_process_node.citation[-1] == citation

    # test that optional attributes can be successfully removed
    simple_process_node.ingredient = []
    simple_process_node.description = ""
    simple_process_node.equipment = []
    simple_process_node.product = []
    simple_process_node.waste = []
    simple_process_node.prerequisite_process = []
    simple_process_node.condition = []
    simple_process_node.property = []
    simple_process_node.keyword = []
    simple_process_node.citation = []

    # assert that optional attributes have been removed
    assert simple_process_node.ingredient == []
    assert simple_process_node.description == ""
    assert simple_process_node.equipment == []
    assert simple_process_node.product == []
    assert simple_process_node.waste == []
    assert simple_process_node.prerequisite_process == []
    assert simple_process_node.condition == []
    assert simple_process_node.property == []
    assert simple_process_node.keyword == []
    assert simple_process_node.citation == []


def test_serialize_process_to_json(simple_process_node) -> None:
    """
    test serializing process node to JSON
    """
    expected_process_dict = {"node": ["Process"], "name": "my process name", "type": "affinity_pure"}

    # comparing dicts because they are more accurate
    ref_dict = json.loads(simple_process_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_process_dict


def test_integration_simple_process(cript_api, simple_project_node, simple_process_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    simple_project_node.name = f"test_integration_process_name_{uuid.uuid4().hex}"

    simple_project_node.collection[0].experiment[0].process = [simple_process_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)


def test_integration_complex_process(cript_api, simple_project_node, simple_process_node, simple_material_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_process_name_{uuid.uuid4().hex}"

    # rename material to not get duplicate error
    simple_material_node.name += f"{simple_material_node.name} {uuid.uuid4().hex}"

    # add material to the project to not get OrphanedNodeError
    simple_project_node.material += [simple_material_node]

    simple_project_node.collection[0].experiment[0].process = [simple_process_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].process[0].description = "process description UPDATED"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
