import json

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
    my_process = cript.Process(name="my process name", type=my_process_type, description=my_process_description, keywords=my_process_keywords)

    # assertions
    assert isinstance(my_process, cript.Process)
    assert my_process.type == my_process_type
    assert my_process.description == my_process_description
    assert my_process.keywords == my_process_keywords


def test_complex_process_node(complex_ingredient_node, complex_equipment_node, complex_citation_node, simple_property_node, complex_condition_node) -> None:
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

    process_product = [
        cript.Material(
            name="my process product material 1",
            identifiers=[{"alternative_names": "my alternative process product material 1"}],
        ),
        cript.Material(
            name="my process product material 1",
            identifiers=[{"alternative_names": "my alternative process product material 1"}],
        ),
    ]

    process_waste = [
        cript.Material(name="my process waste material 1", identifiers=[{"alternative_names": "my alternative process waste material 1"}]),
        cript.Material(name="my process waste material 1", identifiers=[{"alternative_names": "my alternative process waste material 1"}]),
    ]

    prerequisite_processes = [
        cript.Process(name="prerequisite processes 1", type="blow_molding"),
        cript.Process(name="prerequisite processes 2", type="centrifugation"),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    # create complex process
    my_complex_process = cript.Process(
        name=my_process_name,
        type=my_process_type,
        ingredients=[complex_ingredient_node],
        description=my_process_description,
        equipments=[complex_equipment_node],
        products=process_product,
        waste=process_waste,
        prerequisite_processes=[prerequisite_processes],
        conditions=[complex_condition_node],
        properties=[simple_property_node],
        keywords=my_process_keywords,
        citations=[complex_citation_node],
    )

    # assertions
    assert my_complex_process.type == my_process_type
    assert my_complex_process.ingredients == [complex_ingredient_node]
    assert my_complex_process.description == my_process_description
    assert my_complex_process.equipments == [complex_equipment_node]
    assert my_complex_process.products == process_product
    assert my_complex_process.waste == process_waste
    assert my_complex_process.prerequisite_processes == [prerequisite_processes]
    assert my_complex_process.conditions == [complex_condition_node]
    assert my_complex_process.properties == [simple_property_node]
    assert my_complex_process.keywords == my_process_keywords
    assert my_complex_process.citations == [complex_citation_node]


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
    simple_process_node.ingredients = [complex_ingredient_node]
    simple_process_node.description = new_process_description
    simple_process_node.equipments = [complex_equipment_node]
    simple_process_node.products = [simple_process_node]
    simple_process_node.waste = [simple_material_node]
    simple_process_node.prerequisite_processes = [simple_process_node]
    simple_process_node.conditions = [complex_condition_node]
    simple_process_node.properties = [simple_property_node]
    simple_process_node.keywords = [new_process_keywords]
    simple_process_node.citations = [complex_citation_node]

    # test getters
    assert simple_process_node.type == new_process_type
    assert simple_process_node.ingredients == [complex_ingredient_node]
    assert simple_process_node.description == new_process_description
    assert simple_process_node.equipments == [complex_equipment_node]
    assert simple_process_node.products == [simple_process_node]
    assert simple_process_node.waste == [simple_material_node]
    assert simple_process_node.prerequisite_processes == [simple_process_node]
    assert simple_process_node.conditions == [complex_condition_node]
    assert simple_process_node.properties == [simple_property_node]
    assert simple_process_node.keywords == [new_process_keywords]
    assert simple_process_node.citations == [complex_citation_node]


def test_serialize_process_to_json(simple_process_node) -> None:
    """
    test serializing process node to JSON
    """
    expected_process_dict = {"node": ["Process"], "name": "my process name", "keywords": [], "type": "affinity_pure"}

    # comparing dicts because they are more accurate
    ref_dict = json.loads(simple_process_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_process_dict


# TODO add integration tests
