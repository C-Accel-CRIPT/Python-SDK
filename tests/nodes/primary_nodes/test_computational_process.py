import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


def test_create_simple_computational_process(simple_data_node, complex_ingredient_node) -> None:
    """
    create a simple computational_process node with required arguments
    """

    my_computational_process = cript.ComputationProcess(
        name="my computational process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredient=[complex_ingredient_node],
    )

    # assertions
    assert isinstance(my_computational_process, cript.ComputationProcess)
    assert my_computational_process.type == "cross_linking"
    assert my_computational_process.input_data == [simple_data_node]
    assert my_computational_process.ingredient == [complex_ingredient_node]


def test_create_complex_computational_process(
    simple_data_node,
    complex_ingredient_node,
    complex_software_configuration_node,
    complex_condition_node,
    simple_property_node,
    complex_citation_node,
) -> None:
    """
    create a complex computational process with all possible arguments
    """

    computational_process_name = "my computational process name"
    computational_process_notes = "my computational process notes"
    computational_process_type = "cross_linking"

    ingredient = complex_ingredient_node
    data = simple_data_node
    my_computational_process = cript.ComputationProcess(
        name=computational_process_name,
        type=computational_process_type,
        input_data=[data],
        ingredient=[ingredient],
        output_data=[simple_data_node],
        software_configuration=[complex_software_configuration_node],
        condition=[complex_condition_node],
        property=[simple_property_node],
        citation=[complex_citation_node],
        notes=computational_process_notes,
    )

    # assertions
    assert isinstance(my_computational_process, cript.ComputationProcess)
    assert my_computational_process.name == computational_process_name
    assert my_computational_process.type == computational_process_type
    assert my_computational_process.input_data == [data]
    assert my_computational_process.ingredient == [ingredient]
    assert my_computational_process.output_data == [simple_data_node]
    assert my_computational_process.software_configuration == [complex_software_configuration_node]
    assert my_computational_process.condition == [complex_condition_node]
    assert my_computational_process.property == [simple_property_node]
    assert my_computational_process.citation == [complex_citation_node]
    assert my_computational_process.notes == computational_process_notes


def test_computational_process_getters_and_setters(simple_computation_process_node, simple_data_node, simple_ingredient_node, simple_software_configuration, simple_condition_node, simple_property_node, complex_citation_node) -> None:
    """
    tests that all the getters and setters are working fine
    """
    computation_process_type = "hybrid_dynamics"
    computation_process_notes = "my awesome notes"

    # set all computation_process attributes
    simple_computation_process_node.type = computation_process_type
    simple_computation_process_node.input_data = [simple_data_node]
    simple_computation_process_node.output_data = [simple_data_node]
    simple_computation_process_node.ingredient = [simple_ingredient_node]
    simple_computation_process_node.software_configuration = [simple_software_configuration]
    simple_computation_process_node.condition = [simple_condition_node]
    simple_computation_process_node.property = [simple_property_node]
    simple_computation_process_node.citation = [complex_citation_node]
    simple_computation_process_node.notes = computation_process_notes

    # test what was set via setters and what was gotten via getters are the same
    assert simple_computation_process_node.type == computation_process_type
    assert simple_computation_process_node.input_data == [simple_data_node]
    assert simple_computation_process_node.output_data == [simple_data_node]
    assert simple_computation_process_node.ingredient == [simple_ingredient_node]
    assert simple_computation_process_node.software_configuration == [simple_software_configuration]
    assert simple_computation_process_node.condition == [simple_condition_node]
    assert simple_computation_process_node.property == [simple_property_node]
    assert simple_computation_process_node.citation == [complex_citation_node]
    assert simple_computation_process_node.notes == computation_process_notes

    # remove all optional computation_process attributes
    simple_computation_process_node.output_data = []
    simple_computation_process_node.software_configuration = []
    simple_computation_process_node.condition = []
    simple_computation_process_node.property = []
    simple_computation_process_node.citation = []
    simple_computation_process_node.notes = ""

    # test computation process attributes can be removed correctly
    assert simple_computation_process_node.output_data == []
    assert simple_computation_process_node.software_configuration == []
    assert simple_computation_process_node.condition == []
    assert simple_computation_process_node.property == []
    assert simple_computation_process_node.citation == []
    assert simple_computation_process_node.notes == ""


def test_serialize_computational_process_to_json(simple_computational_process_node) -> None:
    """
    tests that a computational process node can be correctly serialized to JSON
    """
    expected_dict: dict = {
        "node": ["ComputationProcess"],
        "name": "my computational process node name",
        "type": "cross_linking",
        "input_data": [
            {
                "node": ["Data"],
                "name": "my data name",
                "type": "afm_amp",
                "file": [{"node": ["File"], "name": "my complex file node fixture", "source": "https://criptapp.org", "type": "calibration", "extension": ".csv", "data_dictionary": "my file's data dictionary"}],
            }
        ],
        "ingredient": [
            {
                "node": ["Ingredient"],
                "material": {},
                "quantity": [{"node": ["Quantity"], "key": "mass", "value": 11.2, "unit": "kg", "uncertainty": 0.2, "uncertainty_type": "stdev"}],
                "keyword": ["catalyst"],
            }
        ],
    }

    ref_dict = json.loads(simple_computational_process_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_dict


def test_integration_computational_process(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simplest_computational_process_node, simple_material_node, simple_data_node) -> None:
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # ========= test create =========
    # renaming to avoid duplicate node errors
    simple_project_node.name = f"test_integration_computation_process_name_{uuid.uuid4().hex}"

    simple_material_node.name = f"{simple_material_node.name}_{uuid.uuid4().hex}"

    simple_project_node.material = [simple_material_node]

    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].experiment = [simple_experiment_node]

    # fixing orphanedDataNodeError
    simple_project_node.collection[0].experiment[0].data = [simple_data_node]

    simple_project_node.collection[0].experiment[0].computation_process = [simplest_computational_process_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change computational_process to trigger update
    simple_project_node.collection[0].experiment[0].computation_process[0].type = "DPD"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simplest_computational_process_node)
