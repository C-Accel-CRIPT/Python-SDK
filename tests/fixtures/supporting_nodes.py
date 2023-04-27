import pytest

import cript


@pytest.fixture(scope="function")
def complex_file_node() -> cript.File:
    """
    complex file node with only required arguments
    """
    my_file = cript.File(source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary")

    return my_file
