import copy

import pytest

import cript


@pytest.fixture(scope="session")
def cript_api():
    """
    creates a CRIPT API object, used for integration tests for all nodes

    * saving
    * getting
    * updating
    * deleting

    Returns
    -------
    cript.API
        api object used to interact with CRIPT
    """
    return cript.API(host="https://cript.org", token="123465")


# ------------------ Simple Nodes ------------------
# minimal nodes with only required arguments to reuse for tests and keep tests clean

# ---------- Primary Nodes ----------
@pytest.fixture(scope="session")
def simple_computational_process_node() -> None:
    """
    simple Computational Process node with only required arguments to use in other tests
    """
    my_computational_process_type = "cross_linking"

    # input data
    data_files = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv",
        data_dictionary="my file's data dictionary"
    )

    input_data = cript.Data(type="afm_amp", files=[data_files])

    # ingredients with Material and Quantity node
    my_material = cript.Material(name="my material",
                                 identifiers=[{"alternative_names": "my material alternative name"}])

    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    ingredients = cript.Ingredient(
        material=my_material,
        quantities=[my_quantity],
    )

    my_computational_process = cript.ComputationalProcess(
        type=my_computational_process_type, input_data=[input_data], ingredients=[ingredients]
    )

    computational_process_copy = copy.deepcopy(my_computational_process)
    yield computational_process_copy

    # reset node state
    computational_process_copy = copy.deepcopy(my_computational_process)


@pytest.fixture(scope="session")
def simple_process_node() -> None:
    """
    simple process node to use in other tests to keep tests clean
    """

    my_process = cript.Process(type="affinity_pure")

    # use copy of process node to keep original state between tests
    my_process_copy = copy.deepcopy(my_process)
    yield my_process_copy

    # reset process node
    my_process_copy = copy.deepcopy(my_process)


@pytest.fixture(scope="session")
def simple_computation_node() -> None:
    """
    simple computation node to use between tests
    """
    my_computation = cript.Computation(type="analysis")

    yield my_computation


@pytest.fixture(scope="session")
def simple_material_node() -> None:
    """
    simple material node to use between tests
    """
    identifiers = [
        {"alternative_names": "my material alternative name"}
    ]
    my_material = cript.Material(name="my material", identifiers=identifiers)

    yield my_material


@pytest.fixture(scope="session")
def simple_reference_node() -> None:
    """
    minimal reference node
    """
    my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

    yield my_reference


@pytest.fixture(scope="session")
def data_object() -> cript.Data:
    """
    create simple data object with only required attributes

    Returns
    -------
    Data
    """


# ---------- Subobjects Nodes ----------
@pytest.fixture(scope="session")
def simple_condition_node() -> None:
    """
    minimal condition node
    """
    my_condition = cript.Condition(key="atm", type="min", value=1)

    yield my_condition


# ---------- Supporting Nodes ----------
@pytest.fixture(scope="session")
def simple_file_node() -> None:
    """
    simple file node with only required arguments
    """
    my_file = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv",
        data_dictionary="my file's data dictionary"
    )

    # use copy of file node to keep original state between tests
    my_file_copy = copy.deepcopy(my_file)

    # use simple file node in other tests
    yield my_file_copy

    # reset file node to original state
    my_file_copy = copy.deepcopy(my_file)


@pytest.fixture(scope="session")
def simple_citation_node(simple_reference_node) -> None:
    """
    minimal citation node
    """
    my_citation = cript.Citation(type="derived_from", reference=simple_reference_node)

    yield my_citation
