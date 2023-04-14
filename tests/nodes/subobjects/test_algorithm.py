def test_create_simple_algorithm_subobject() -> None:
    """
    create a simple algorithm subobject required arguments
    """
    pass


def test_create_complex_algorithm_subobject() -> None:
    """
    create a complex algorithm subobject with all possible arguments
    """
    pass


def test_algorithm_key_invalid_vocabulary() -> None:
    """
    tests that setting the algorithm key to an invalid vocabulary word gives the expected error
    """
    pass


def test_algorithm_getters_and_setters() -> None:
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


def test_serialize_algorithm_to_json() -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """
    pass


# ---------- Integration tests ----------
def test_save_algorithm_to_api() -> None:
    """
    tests if the algorithm subobject can be saved to the API without errors and status code of 200
    """
    pass


def test_get_a_node_with_algorithm_from_api() -> None:
    """
    integration test: gets the algorithm subobject from the api that was saved prior
    """
    pass


def test_deserialize_node_with_algorithm() -> None:
    """
    tests that a JSON of a algorithm subobject can be correctly converted to python object
    """
    pass


def test_update_algorithm_in_api() -> None:
    """
    tests that the algorithm subobject can be correctly updated within the API
    """
    pass


def test_delete_algorithm_from_api() -> None:
    """
    integration test: tests that the algorithm subobject can be deleted correctly from the API
    tries to get the algorithm from API, and it is expected for the API to give an error response
    """
    pass
