import copy
import json

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


def test_data_type_invalid_vocabulary() -> None:
    """
    tests that setting the data type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


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
            source="https://bing.com",
            type="computation_config",
            extension=".pdf",
            data_dictionary="my second file data dictionary",
        ),
    ]

    # use setters
    comp_process = copy.deepcopy(simple_computational_process_node)
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
                "data_dictionary": "my file's data dictionary",
                "extension": ".csv",
                "node": ["File"],
                "source": "https://criptapp.org",
                "type": "calibration",
            }
        ],
    }

    ref_dict = json.loads(simple_data_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_data_dict


# ---------- Integration tests ----------
def test_save_data_to_api() -> None:
    """
    tests if the data node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_data_from_api() -> None:
    """
    integration test: gets the data node from the api that was saved prior
    """
    pass


def test_serialize_json_to_data() -> None:
    """
    tests that a JSON of a data node can be correctly converted to python object
    """
    pass


def test_update_data_in_api() -> None:
    """
    tests that the data node can be correctly updated within the API
    """
    pass


def test_delete_data_from_api() -> None:
    """
    integration test: tests that the data node can be deleted correctly from the API
    tries to get the data from API, and it is expected for the API to give an error response
    """
    pass
