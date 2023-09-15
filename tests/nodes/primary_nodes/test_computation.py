import copy
import json
import uuid

from integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
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
    simple_computation_node.condition = [complex_condition_node]
    simple_computation_node.citation = [complex_citation_node]
    simple_computation_node.notes = new_notes

    # assert getter and setter are same
    assert simple_computation_node.type == new_type
    assert simple_computation_node.input_data == [simple_data_node]
    assert simple_computation_node.output_data == [simple_data_node]
    assert simple_computation_node.software_configuration == [complex_software_configuration_node]
    assert simple_computation_node.condition == [complex_condition_node]
    assert simple_computation_node.citation == [complex_citation_node]
    assert simple_computation_node.notes == new_notes

    # remove node attributes
    simple_computation_node.type = ""
    simple_computation_node.input_data = []
    simple_computation_node.output_data = []
    simple_computation_node.software_configuration = []
    simple_computation_node.condition = []
    simple_computation_node.citation = []
    simple_computation_node.notes = ""

    # assert users can remove optional attributes
    assert simple_computation_node.input_data == []
    assert simple_computation_node.output_data == []
    assert simple_computation_node.software_configuration == []
    assert simple_computation_node.condition == []
    assert simple_computation_node.citation == []
    assert simple_computation_node.notes == ""


def test_serialize_computation_to_json(simple_computation_node) -> None:
    """
    tests that it can correctly turn the computation node into its equivalent JSON
    """
    # TODO test this more vigorously
    expected_dict = {"node": ["Computation"], "name": "my computation name", "type": "analysis"}

    # comparing dicts for better test
    ref_dict = json.loads(simple_computation_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_dict


def test_integration_computation(cript_api, simple_project_node, simple_computation_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # --------- test create ---------
    simple_project_node.name = f"test_integration_computation_name_{uuid.uuid4().hex}"
    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # --------- test update ---------
    # change simple computation attribute to trigger update
    simple_project_node.collection[0].experiment[0].computation[0].type = "data_fit"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_computation_node)
