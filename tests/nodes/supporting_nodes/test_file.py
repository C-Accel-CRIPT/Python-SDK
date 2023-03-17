import cript
import pytest


@pytest.fixture(scope="session")
def cript_api():
    """
    creates an CRIPT API object, used for
    * saving
    * getting
    * updating
    * deleting

    Returns
    -------
    cript.API
        api object used to interact with CRIPT
    """
    host: str = "https://cript.org"
    token: str = "123465"

    return cript.API(host=host, token=token)


def test_file_to_json():
    """
    test that file can correctly be serialized from Node to JSON
    """
    pass


def test_file_from_json():
    """
    test that file can correctly be serialized from JSON to Node
    """
    pass


def test_create_save_file(cript_api):
    """
    * tests that it can create a file with only required attributes
    * tests that it can save a file
    * indirectly tests file with a link source
    """
    my_file = cript.File(source="https://example.com", type="calibration")
    cript_api.save(my_file)


def test_create_file_with_all_attributes():
    """
    tests that it can create a file with all optional attributes
    """
    my_file = cript.File(
        source="https://example.com",
        type="calibration",
        extension="csv",
        data_dictionary="this is my data dictionary",
    )


def test_get_file_from_cript():
    """
    tests that it can get a file correctly from CRIPT
    """


def test_file_source_path():
    """
    tests file with source of absolute path pointing to a path on local storage
    """
    pass


def test_file_invalid_source_path():
    """
    tests file with source of absolute path pointing to a path on local storage
    """
    pass


def get_all_file_attributes():
    """
    tests that it can correctly get all the file attributes
    """
    # TODO consider adding individual test for individual attributes instead of one test for all attributes
    pass


def set_all_file_attributes():
    """
    tests that it can correctly set all file attributes
    """
    # TODO consider adding individual test for individual attributes instead of one test for all attributes
    pass
