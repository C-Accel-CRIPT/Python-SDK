import json

from util import strip_uid_from_dict

import cript


def test_create_simple_computation_process(simple_data_node, complex_ingredient_node) -> None:
    """
    create a simple computation_process node with required arguments
    """

    my_computation_process = cript.ComputationalProcess(
        name="my computation process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredients=[complex_ingredient_node],
    )

    # assertions
    assert isinstance(my_computation_process, cript.ComputationalProcess)
    assert my_computation_process.type == "cross_linking"
    assert my_computation_process.input_data == [simple_data_node]
    assert my_computation_process.ingredients == [complex_ingredient_node]


def test_create_complex_computation_process(
    simple_data_node,
    simple_material_node,
    complex_ingredient_node,
    complex_software_configuration_node,
    complex_condition_node,
    simple_property_node,
    complex_citation_node,
) -> None:
    """
    create a complex computation process with all possible arguments
    """

    computation_process_name = "my computation process name"
    computation_process_type = "cross_linking"

    my_computation_process = cript.ComputationalProcess(
        name=computation_process_name,
        type=computation_process_type,
        input_data=[simple_data_node],
        ingredients=[complex_ingredient_node],
        output_data=[simple_data_node],
        software_configurations=[complex_software_configuration_node],
        conditions=[complex_condition_node],
        properties=[simple_property_node],
        citations=[complex_citation_node],
    )

    # assertions
    assert isinstance(my_computation_process, cript.ComputationalProcess)
    assert my_computation_process.name == computation_process_name
    assert my_computation_process.type == computation_process_type
    assert my_computation_process.input_data == [simple_data_node]
    assert my_computation_process.ingredients == [complex_ingredient_node]
    assert my_computation_process.output_data == [simple_data_node]
    assert my_computation_process.software_configurations == [complex_software_configuration_node]
    assert my_computation_process.conditions == [complex_condition_node]
    assert my_computation_process.properties == [simple_property_node]
    assert my_computation_process.citations == [complex_citation_node]


def test_serialize_computation_process_to_json(simple_computation_process_node) -> None:
    """
    tests that a computation process node can be correctly serialized to JSON
    """
    expected_dict: dict = {
        "node": ["ComputationalProcess"],
        "name": "my computation process name",
        "type": "cross_linking",
        "input_data": [
            {
                "node": ["Data"],
                "name": "my data name",
                "type": "afm_amp",
                "files": [
                    {
                        "node": ["File"],
                        "source": "https://criptapp.org",
                        "type": "calibration",
                        "extension": ".csv",
                        "data_dictionary": "my file's data dictionary",
                    }
                ],
            }
        ],
        "ingredients": [
            {
                "node": ["Ingredient"],
                "material": {
                    "node": ["Material"],
                    "name": "my material",
                    "identifiers": [{"alternative_names": "my material alternative name"}],
                },
                "quantities": [{"node": ["Quantity"], "key": "mass", "value": 1.23, "unit": "gram"}],
            }
        ],
    }

    ref_dict = json.loads(simple_computation_process_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_dict


# ---------- Integration tests ----------
def test_save_computation_process_to_api() -> None:
    """
    tests if the computation_process node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_computation_process_from_api() -> None:
    """
    integration test: gets the computation_process node from the api that was saved prior
    """
    pass


def test_serialize_json_to_computation_process() -> None:
    """
    tests that a JSON of a computation_process node can be correctly converted to python object
    """
    pass


def test_update_computation_process_in_api() -> None:
    """
    tests that the computation_process node can be correctly updated within the API
    """
    pass


def test_delete_computation_process_from_api() -> None:
    """
    integration test: tests that the computation_process node can be deleted correctly from the API
    tries to get the computation_process from API, and it is expected for the API to give an error response
    """
    pass
