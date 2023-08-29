import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper, delete_integration_node_helper
from util import strip_uid_from_dict

import cript


def test_create_simple_data_node(complex_file_node) -> None:
    """
    create a simple data node with only required arguments
    """
    my_data_type = "afm_amp"

    my_data = cript.Data(name="my data name", type=my_data_type, file=[complex_file_node])

    # assertions
    assert isinstance(my_data, cript.Data)
    assert my_data.type == my_data_type
    assert my_data.file == [complex_file_node]


def test_create_complex_data_node(
    complex_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_material_node,
    complex_citation_node,
) -> None:
    """
    create a complex data node with all possible arguments
    """

    file_node = copy.deepcopy(complex_file_node)
    my_complex_data = cript.Data(
        name="my complex data node name",
        type="afm_amp",
        file=[file_node],
        sample_preparation=simple_process_node,
        computation=[simple_computation_node],
        computation_process=[simple_computational_process_node],
        material=[simple_material_node],
        process=[simple_process_node],
        # citation=[complex_citation_node],
    )

    # assertions
    assert isinstance(my_complex_data, cript.Data)
    assert my_complex_data.type == "afm_amp"
    assert my_complex_data.file == [file_node]
    assert my_complex_data.sample_preparation == simple_process_node
    assert my_complex_data.computation == [simple_computation_node]
    assert my_complex_data.computation_process == [simple_computational_process_node]
    assert my_complex_data.material == [simple_material_node]
    assert my_complex_data.process == [simple_process_node]
    # assert my_complex_data.citation == [complex_citation_node]


def test_data_getters_and_setters(
    simple_data_node,
    complex_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_material_node,
    complex_citation_node,
) -> None:
    """
    tests that all the getters and setters are working fine
    and they can be removed as well

    Notes
    -----
    indirectly tests setting the data type to correct vocabulary

    Returns
    -------
    None
    """
    my_data_type = "afm_height"

    my_new_files = [
        complex_file_node,
        cript.File(
            name="my data file node",
            source="https://bing.com",
            type="computation_config",
            extension=".pdf",
            data_dictionary="my second file data dictionary",
        ),
    ]

    # use setters
    comp_process = simple_computational_process_node
    simple_data_node.type = my_data_type
    simple_data_node.file = my_new_files
    simple_data_node.sample_preparation = simple_process_node
    simple_data_node.computation = [simple_computation_node]
    simple_data_node.computation_process = [comp_process]
    simple_data_node.material = [simple_material_node]
    simple_data_node.process = [simple_process_node]
    simple_data_node.citation = [complex_citation_node]

    # assertions check getters and setters
    assert simple_data_node.type == my_data_type
    assert simple_data_node.file == my_new_files
    assert simple_data_node.sample_preparation == simple_process_node
    assert simple_data_node.computation == [simple_computation_node]
    assert simple_data_node.computation_process == [comp_process]
    assert simple_data_node.material == [simple_material_node]
    assert simple_data_node.process == [simple_process_node]
    assert simple_data_node.citation == [complex_citation_node]

    # remove optional attributes
    simple_data_node.sample_preparation = []
    simple_data_node.computation = []
    simple_data_node.computation_process = []
    simple_data_node.material = []
    simple_data_node.process = []
    simple_data_node.citation = []

    # assert that optional attributes have been removed from data node
    assert simple_data_node.sample_preparation == []
    assert simple_data_node.computation == []
    assert simple_data_node.computation_process == []
    assert simple_data_node.material == []
    assert simple_data_node.process == []
    assert simple_data_node.citation == []


def test_serialize_data_to_json(simple_data_node) -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """

    # TODO should Base attributes should be in here too like notes, public, model version, etc?
    expected_data_dict = {
        "node": ["Data"],
        "type": "afm_amp",
        "name": "my data name",
        "file": [
            {
                "node": ["File"],
                "name": "my complex file node fixture",
                "data_dictionary": "my file's data dictionary",
                "extension": ".csv",
                "source": "https://criptapp.org",
                "type": "calibration",
            }
        ],
    }

    ref_dict = json.loads(simple_data_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_data_dict


def test_integration_data(cript_api, simple_project_node, simple_data_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal

    Notes
    -----
    indirectly tests complex file as well because every data node must have a file node
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_project_name_{uuid.uuid4().hex}"

    simple_project_node.collection[0].experiment[0].data = [simple_data_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update a simple attribute of data to trigger update
    simple_project_node.collection[0].experiment[0].data[0].type = "afm_height"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_data_node)
