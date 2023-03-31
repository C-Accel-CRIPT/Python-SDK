import json

import cript


def test_create_simple_data_node(simple_file_node) -> None:
    """
    create a simple data node with only required arguments
    """
    my_data_type = "afm_amp"

    my_data = cript.Data(type=my_data_type, files=[simple_file_node])

    # assertions
    assert isinstance(my_data, cript.Data)
    assert my_data.type == my_data_type
    assert my_data.files == [simple_file_node]


def test_create_complex_data_node(
    simple_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_material_node,
    simple_citation_node,
) -> None:
    """
    create a complex data node with all possible arguments
    """
    my_complex_data = cript.Data(
        type="afm_amp",
        files=[simple_file_node],
        sample_preperation=simple_process_node,
        computations=[simple_computation_node],
        computational_process=[simple_computational_process_node],
        materials=[simple_material_node],
        processes=[simple_process_node],
        citations=[simple_citation_node],
    )

    # assertions
    assert isinstance(my_complex_data, cript.Data)
    assert my_complex_data.type == "afm_amp"
    assert my_complex_data.files == [simple_file_node]
    assert my_complex_data.sample_preperation == simple_process_node
    assert my_complex_data.computations == [simple_computation_node]
    assert my_complex_data.computational_process == [simple_computational_process_node]
    assert my_complex_data.materials == [simple_material_node]
    assert my_complex_data.processes == [simple_process_node]
    assert my_complex_data.citations == [simple_citation_node]


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
    simple_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_material_node,
    simple_citation_node,
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
        simple_file_node,
        cript.File(
            source="https://bing.com",
            type="computation_config",
            extension=".pdf",
            data_dictionary="my second file data dictionary",
        ),
    ]

    # use setters
    simple_data_node.type = my_data_type
    simple_data_node.files = my_new_files
    simple_data_node.sample_preperation = simple_process_node
    simple_data_node.computations = [simple_computation_node]
    simple_data_node.computational_process = simple_computational_process_node
    simple_data_node.materials = [simple_material_node]
    simple_data_node.processes = [simple_process_node]
    simple_data_node.citations = [simple_citation_node]

    # assertions check getters and setters
    assert simple_data_node.type == my_data_type
    assert simple_data_node.files == my_new_files
    assert simple_data_node.sample_preperation == simple_process_node
    assert simple_data_node.computations == [simple_computation_node]
    assert simple_data_node.computational_process == simple_computational_process_node
    assert simple_data_node.materials == [simple_material_node]
    assert simple_data_node.processes == [simple_process_node]
    assert simple_data_node.citations == [simple_citation_node]


def test_serialize_data_to_json(simple_data_node) -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """

    # TODO Base attributes should be in here too like notes, public, model version, etc.
    expected_data_dict = {
        "node": "Data",
        "type": "afm_amp",
        "files": [
            {
                "node": "File",
                "source": "https://criptapp.org",
                "type": "calibration",
                "extension": ".csv",
                "data_dictionary": "my file's data dictionary",
            }
        ],
        "sample_preperation": None,
        "computations": None,
        "computational_process": None,
        "materials": None,
        "processes": None,
        "citations": None,
    }

    print("\n \n")
    print(simple_data_node.json)

    assert json.loads(simple_data_node.json) == expected_data_dict


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
