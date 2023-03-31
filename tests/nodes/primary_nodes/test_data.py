import pytest

import cript


def test_create_simple_data_node() -> None:
    """
    create a simple data node with only required arguments
    """
    my_data_type = "afm_amp"

    my_files = [
        cript.File(
            source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
        )
    ]

    my_data = cript.Data(type=my_data_type, files=my_files)

    # assertions
    assert isinstance(my_data, cript.Data)
    assert my_data.type == my_data_type
    assert my_data.files == my_files


def test_create_complex_data_node() -> None:
    """
    create a complex data node with all possible arguments
    """
    my_data_type = "afm_amp"

    my_files = [
        cript.File(
            source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
        )
    ]

    sample_preperation = cript.Process(type="affinity_pure", description="my simple material description", keywords=["anionic"])

    my_computations = [cript.Computation(type="analysis")]

    my_computational_process = [cript.ComputationalProcess()]


@pytest.fixture(scope="session")
def data_object() -> cript.Data:
    """
    create simple data object with only required attributes

    Returns
    -------
    Data
    """
    # create data
    # my_files = [cript.File()]
    #
    # data_type = "afm_amp"
    # my_data = cript.Data(type=data_type, files=my_files)

    # assertions
    # assert isinstance(my_data, cript.Data)
    # assert my_data.files == my_files

    # use data node

    # reset data node to original state
    pass


def test_data_type_invalid_vocabulary() -> None:
    """
    tests that setting the data type to an invalid vocabulary word gives the expected error

    Returns
    -------
    None
    """
    pass


def test_data_getters_and_setters() -> None:
    """
    tests that all the getters and setters are working fine

    Notes
    -----
    indirectly tests setting the data type to correct vocabulary

    Returns
    -------
    None
    """
    pass


def test_serialize_data_to_json() -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """
    pass


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
