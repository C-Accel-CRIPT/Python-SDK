import cript


def test_create_simple_computational_process(simple_data_node, simple_ingredient_node) -> None:
    """
    create a simple computational_process node with required arguments
    """

    my_computational_process = cript.ComputationalProcess(
        type="cross_linking", input_data=[simple_data_node], ingredients=[simple_ingredient_node]
    )

    # assertions
    assert isinstance(my_computational_process, cript.ComputationalProcess)
    assert my_computational_process.type == "cross_linking"
    assert my_computational_process.input_data == [simple_data_node]
    assert my_computational_process.ingredients == [simple_ingredient_node]


def test_create_complex_computational_process(
    simple_data_node,
    simple_material_node,
    simple_ingredient_node,
    simple_software_configuration,
    simple_condition_node,
    simple_property_node,
    simple_citation_node,
) -> None:
    """
    create a complex computational process with all possible arguments
    """

    computational_process_type = "cross_linking"

    my_computational_process = cript.ComputationalProcess(
        type=computational_process_type,
        input_data=[simple_data_node],
        ingredients=[simple_ingredient_node],
        output_data=[simple_data_node],
        software_configurations=[simple_software_configuration],
        conditions=[simple_condition_node],
        properties=[simple_property_node],
        citations=[simple_citation_node],
    )

    # assertions
    assert isinstance(my_computational_process, cript.ComputationalProcess)
    assert my_computational_process.type == computational_process_type
    assert my_computational_process.input_data == [simple_data_node]
    assert my_computational_process.ingredients == [simple_ingredient_node]
    assert my_computational_process.output_data == [simple_data_node]
    assert my_computational_process.software_configurations == [simple_software_configuration]
    assert my_computational_process.conditions == [simple_condition_node]
    assert my_computational_process.properties == [simple_property_node]
    assert my_computational_process.citations == [simple_citation_node]


# ---------- Integration tests ----------
def test_save_computational_process_to_api() -> None:
    """
    tests if the computational_process node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_computational_process_from_api() -> None:
    """
    integration test: gets the computational_process node from the api that was saved prior
    """
    pass


def test_serialize_json_to_computational_process() -> None:
    """
    tests that a JSON of a computational_process node can be correctly converted to python object
    """
    pass


def test_update_computational_process_in_api() -> None:
    """
    tests that the computational_process node can be correctly updated within the API
    """
    pass


def test_delete_computational_process_from_api() -> None:
    """
    integration test: tests that the computational_process node can be deleted correctly from the API
    tries to get the computational_process from API, and it is expected for the API to give an error response
    """
    pass
