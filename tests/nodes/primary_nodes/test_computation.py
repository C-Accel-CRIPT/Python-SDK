import copy
import json

from util import strip_uid_from_dict

import cript


def test_create_simple_computation_node() -> None:
    """
    test that a simple computation node with all possible arguments can be created successfully
    """
    my_computation_type = "analysis"
    my_computation_name = "this is my computation name"

    my_computation_node = cript.Computation(name=my_computation_name, type=my_computation_type)

    # assertions
    assert isinstance(my_computation_node, cript.Computation)
    assert my_computation_node.name == my_computation_name
    assert my_computation_node.type == my_computation_type


def test_create_complex_computation_node(simple_data_node, complex_software_configuration_node, complex_condition_node, simple_computation_node, complex_citation_node) -> None:
    """
    test that a complex computation node with all possible arguments can be created
    """
    my_computation_type = "analysis"

    citation = copy.deepcopy(complex_citation_node)
    condition = copy.deepcopy(complex_condition_node)
    my_computation_node = cript.Computation(
        name="my complex computation node name",
        type="analysis",
        input_data=[simple_data_node],
        output_data=[simple_data_node],
        software_configuration=[complex_software_configuration_node],
        condition=[condition],
        prerequisite_computation=simple_computation_node,
        citation=[citation],
    )

    # assertions
    assert isinstance(my_computation_node, cript.Computation)
    assert my_computation_node.type == my_computation_type
    assert my_computation_node.input_data == [simple_data_node]
    assert my_computation_node.output_data == [simple_data_node]
    assert my_computation_node.software_configuration == [complex_software_configuration_node]
    assert my_computation_node.condition == [condition]
    assert my_computation_node.prerequisite_computation == simple_computation_node
    assert my_computation_node.citation == [citation]


def test_computation_type_invalid_vocabulary() -> None:
    """
    tests that setting the Computation type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_computation_getters_and_setters(simple_computation_node, simple_data_node, complex_software_configuration_node, complex_condition_node, complex_citation_node) -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the data type to correct vocabulary
    """
    new_type: str = "data_fit"
    new_notes: str = "my computation node note"

    # since the simple_computation_node only has type, the rest of them I can just set and test
    simple_computation_node.type = new_type
    simple_computation_node.input_data = [simple_data_node]
    simple_computation_node.output_data = [simple_data_node]
    simple_computation_node.software_configuration = [complex_software_configuration_node]
    condition = copy.deepcopy(complex_condition_node)
    simple_computation_node.condition = [condition]
    citation = copy.deepcopy(complex_citation_node)
    simple_computation_node.citation = [citation]
    simple_computation_node.notes = new_notes

    # assert getter and setter are same
    assert simple_computation_node.type == new_type
    assert simple_computation_node.input_data == [simple_data_node]
    assert simple_computation_node.output_data == [simple_data_node]
    assert simple_computation_node.software_configuration == [complex_software_configuration_node]
    assert simple_computation_node.condition == [condition]
    assert simple_computation_node.citation == [citation]
    assert simple_computation_node.notes == new_notes


def test_serialize_computation_to_json(simple_computation_node) -> None:
    """
    tests that it can correctly turn the computation node into its equivalent JSON
    """
    # TODO test this more vigorously
    expected_dict = {"node": ["Computation"], "name": "my computation name", "type": "analysis", "citation": []}

    # comparing dicts for better test
    ref_dict = json.loads(simple_computation_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_dict


# ---------- Integration tests ----------
def test_save_computation_to_api() -> None:
    """
    tests if the computation node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_computation_from_api() -> None:
    """
    integration test: gets the computation node from the api that was saved prior
    """
    pass


def test_serialize_json_to_computation() -> None:
    """
    tests that a JSON of a computation node can be correctly converted to python object
    """
    pass


def test_update_computation_in_api() -> None:
    """
    tests that the computation node can be correctly updated within the API
    """
    pass


def test_delete_computation_from_api() -> None:
    """
    integration test: tests that the computation node can be deleted correctly from the API
    tries to get the computation from API, and it is expected for the API to give an error response
    """
    pass
