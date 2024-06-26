import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


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


def test_complex_process_node(complex_ingredient_node, complex_citation_node, simple_property_node, simple_material_node, simple_process_node, complex_equipment_node, complex_condition_node) -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """
    my_process_name = "my complex process node name"
    my_process_type = "affinity_pure"
    my_process_description = "my simple material description"

    process_waste = [
        cript.Material(name="my process waste material 1", bigsmiles="process waste bigsmiles"),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    my_notes = "my complex process notes"

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
        property=[simple_property_node],
        keyword=my_process_keywords,
        citation=[complex_citation_node],
        notes=my_notes,
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
    assert my_complex_process.property[-1] == simple_property_node
    assert my_complex_process.keyword[-1] == my_process_keywords[-1]
    assert my_complex_process.citation[-1] == complex_citation_node
    assert my_complex_process.notes == my_notes


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
    new_process_notes = "new process notes"

    # test setters
    simple_process_node.type = new_process_type
    simple_process_node.ingredient = [complex_ingredient_node]
    simple_process_node.description = new_process_description
    simple_process_node.equipment = [complex_equipment_node]
    simple_process_node.product = [simple_material_node]
    simple_process_node.waste = [simple_material_node]
    simple_process_node.prerequisite_process = [simple_process_node]
    simple_process_node.condition = [complex_condition_node]
    simple_process_node.property += [simple_property_node]
    simple_process_node.keyword = [new_process_keywords]
    simple_process_node.citation = [complex_citation_node]
    simple_process_node.notes = new_process_notes

    # test getters
    assert simple_process_node.type == new_process_type
    assert simple_process_node.ingredient == [complex_ingredient_node]
    assert simple_process_node.description == new_process_description
    assert simple_process_node.equipment[-1] == complex_equipment_node
    assert simple_process_node.product[-1] == simple_material_node
    assert simple_process_node.waste == [simple_material_node]
    assert simple_process_node.prerequisite_process == [simple_process_node]
    assert simple_process_node.condition == [complex_condition_node]
    assert simple_process_node.property[-1] == simple_property_node
    assert simple_process_node.keyword == [new_process_keywords]
    assert simple_process_node.citation[-1] == complex_citation_node
    assert simple_process_node.notes == new_process_notes

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
    simple_process_node.notes = ""

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
    assert simple_process_node.notes == ""


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

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)


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

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].process[0].description = "process description UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_process_node)
