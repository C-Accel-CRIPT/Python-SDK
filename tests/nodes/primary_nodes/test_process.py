import json

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
    my_process = cript.Process(type=my_process_type, description=my_process_description, keywords=my_process_keywords)

    # assertions
    assert isinstance(my_process, cript.Process)
    assert my_process.type == my_process_type
    assert my_process.description == my_process_description
    assert my_process.keywords == my_process_keywords


def complex_process_node(simple_ingredient_node) -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """
    # TODO clean up this test and use fixtures from conftest.py

    my_process_type = "affinity_pure"

    my_process_description = "my simple material description"

    my_equipments = [
        cript.Equipment(key="burner"),
        cript.Equipment(key="canula"),
    ]

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
        cript.Material(
            name="my process waste material 1",
            identifiers=[{"alternative_names": "my alternative process waste material 1"}]
        ),
        cript.Material(
            name="my process waste material 1",
            identifiers=[{"alternative_names": "my alternative process waste material 1"}]
        ),
    ]

    prerequisite_processes = [
        cript.Process(type="blow_molding"),
        cript.Process(type="centrifugation"),
    ]

    my_conditions = [
        cript.Condition(key="atm", type="min", value=1),
        cript.Condition(key="boundary_type", type="max", value=2),
    ]

    my_properties = [
        cript.Property(key="arrhenius_activation", type="min", value=3, unit="gram"),
        cript.Property(key="arrhenius_activation", type="max", value=4, unit="gram"),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    my_reference = cript.Reference(type="journal_article", title="my title")

    my_citations = [cript.Citation(type="derived_from", reference=my_reference)]

    # create complex process
    my_complex_process = cript.Process(
        type=my_process_type,
        ingredients=simple_ingredient_node,
        description=my_process_description,
        equipments=my_equipments,
        products=process_product,
        waste=process_waste,
        conditions=my_conditions,
        properties=my_properties,
        keywords=my_process_keywords,
        citations=my_citations,
    )

    # assertions
    assert my_complex_process.type == my_process_type
    assert my_complex_process.ingredients == [simple_ingredient_node]
    assert my_complex_process.description == my_process_description
    assert my_complex_process.equipments == my_equipments
    assert my_complex_process.products == process_product
    assert my_complex_process.waste == process_waste
    assert my_complex_process.conditions == my_conditions
    assert my_complex_process.properties == my_properties
    assert my_complex_process.keywords == my_process_keywords
    assert my_complex_process.citations == my_citations


def test_process_getters_and_setters(
        simple_process_node,
        simple_ingredient_node,
        simple_equipment_node,
        simple_material_node,
        simple_condition_node,
        simple_property_node,
        simple_citation_node,
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
    simple_process_node.ingredients = [simple_ingredient_node]
    simple_process_node.description = new_process_description
    simple_process_node.equipments = [simple_equipment_node]
    simple_process_node.products = [simple_process_node]
    simple_process_node.waste = [simple_material_node]
    simple_process_node.prerequisite_processes = [simple_process_node]
    simple_process_node.conditions = [simple_condition_node]
    simple_process_node.properties = [simple_property_node]
    simple_process_node.keywords = [new_process_keywords]
    simple_process_node.citations = [simple_citation_node]

    # test getters
    assert simple_process_node.type == new_process_type
    assert simple_process_node.ingredients == [simple_ingredient_node]
    assert simple_process_node.description == new_process_description
    assert simple_process_node.equipments == [simple_equipment_node]
    assert simple_process_node.products == [simple_process_node]
    assert simple_process_node.waste == [simple_material_node]
    assert simple_process_node.prerequisite_processes == [simple_process_node]
    assert simple_process_node.conditions == [simple_condition_node]
    assert simple_process_node.properties == [simple_property_node]
    assert simple_process_node.keywords == [new_process_keywords]
    assert simple_process_node.citations == [simple_citation_node]


def test_serialize_process_to_json(simple_process_node) -> None:
    """
    test serializing process node to JSON
    """
    expected_process_dict = {"keywords": [], "node": "Process", "type": "affinity_pure"}

    # comparing dicts because they are more accurate
    assert json.loads(simple_process_node.json) == expected_process_dict

# TODO add integration tests
