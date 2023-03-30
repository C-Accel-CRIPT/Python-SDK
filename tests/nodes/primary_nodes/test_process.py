import cript
import pytest


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


def test_complex_process_node() -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """
    # TODO add ingredient as that is missing from testing the complete node

    my_process_type = "affinity_pure"

    my_process_description = "my simple material description"

    my_equipments = [
        cript.Equipment(key="burner"),
        cript.Equipment(key="canula"),
    ]

    process_product = [
        cript.Material(name="my process product material 1",
                       identifiers=[{"alternative_names": "my alternative process product material 1"}]),

        cript.Material(name="my process product material 1",
                       identifiers=[{"alternative_names": "my alternative process product material 1"}]),
    ]

    process_waste = [
        cript.Material(name="my process waste material 1",
                       identifiers=[{"alternative_names": "my alternative process waste material 1"}]),

        cript.Material(name="my process waste material 1",
                       identifiers=[{"alternative_names": "my alternative process waste material 1"}]),
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

    my_citations = [
        cript.Citation(type="derived_from", reference=my_reference)
    ]

    # create complex process
    my_complex_process = cript.Process(
        type=my_process_type,
        ingredients=None,
        description=my_process_description,
        equipments=my_equipments,
        products=process_product,
        waste=process_waste,
        conditions=my_conditions,
        properties=my_properties,
        keywords=my_process_keywords,
        citations=my_citations
    )

    # assertions
    assert my_complex_process.type == my_process_type
    # assert my_complex_process.ingredients == None
    assert my_complex_process.description == my_process_description
    assert my_complex_process.equipments == my_equipments
    assert my_complex_process.products == process_product
    assert my_complex_process.waste == process_waste
    assert my_complex_process.conditions == my_conditions
    assert my_complex_process.properties == my_properties
    assert my_complex_process.keywords == my_process_keywords
    assert my_complex_process.citations == my_citations
