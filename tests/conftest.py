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


# ---------- Primary Nodes ----------
# TODO alphabetize later to make looking through it easier
@pytest.fixture(scope="session")
def simple_computational_process_node() -> cript.ComputationalProcess:
    """
    simple Computational Process node with only required arguments to use in other tests
    """
    my_computational_process_type = "cross_linking"

    # input data
    data_files = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
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
def simple_data_node(simple_file_node) -> cript.Data:
    """
    minimal data node
    """
    my_data = cript.Data(type="afm_amp", files=[simple_file_node])

    yield my_data


@pytest.fixture(scope="session")
def simple_process_node() -> cript.Process:
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
def simple_computation_node() -> cript.Computation:
    """
    simple computation node to use between tests
    """
    my_computation = cript.Computation(type="analysis")

    yield my_computation


@pytest.fixture(scope="session")
def simple_material_node() -> cript.Material:
    """
    simple material node to use between tests
    """
    identifiers = [{"alternative_names": "my material alternative name"}]
    my_material = cript.Material(name="my material", identifiers=identifiers)

    yield my_material


@pytest.fixture(scope="session")
def simple_reference_node() -> cript.Reference:
    """
    minimal reference node
    """
    my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

    yield my_reference


@pytest.fixture(scope="session")
def simple_software_node() -> cript.Software:
    """
    minimal software node with only required arguments
    """
    my_software = cript.Software("my software name", version="1.2.3")

    yield my_software


@pytest.fixture(scope="session")
def simple_software_configuration(simple_software_node) -> cript.SoftwareConfiguration:
    """
    minimal software configuration node with only required arguments
    """
    my_software_configuration = cript.SoftwareConfiguration(software=simple_software_node)

    yield my_software_configuration


# ---------- Subobjects Nodes ----------
@pytest.fixture(scope="session")
def simple_condition_node() -> cript.Condition:
    """
    minimal condition node
    """
    my_condition = cript.Condition(key="atm", type="min", value=1)

    yield my_condition


@pytest.fixture(scope="session")
def simple_equipment_node() -> cript.Equipment:
    """
    minimal condition node to reuse for tests
    """
    my_equipment = cript.Equipment(key="burner")

    yield my_equipment


@pytest.fixture(scope="session")
def simple_property_node() -> cript.Property:
    """
    minimal Property node to reuse for tests
    """
    # TODO key and type might not be correct, check later
    my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

    yield my_property


# ---------- Supporting Nodes ----------
@pytest.fixture(scope="session")
def simple_file_node() -> cript.File:
    """
    simple file node with only required arguments
    """
    my_file = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
    )

    # use copy of file node to keep original state between tests
    my_file_copy = copy.deepcopy(my_file)

    # use simple file node in other tests
    yield my_file_copy

    # reset file node to original state
    my_file_copy = copy.deepcopy(my_file)


@pytest.fixture(scope="session")
def simple_citation_node(simple_reference_node) -> cript.Citation:
    """
    minimal citation node
    """
    my_citation = cript.Citation(type="derived_from", reference=simple_reference_node)

    yield my_citation


@pytest.fixture(scope="session")
def simple_quantity_node() -> cript.Quantity:
    """
    minimal quantity node
    """
    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    yield my_quantity


@pytest.fixture(scope="session")
def simple_ingredient_node(simple_material_node, simple_quantity_node) -> cript.Ingredient:
    """
    minimal ingredient node
    """
    ingredients = cript.Ingredient(
        material=simple_material_node,
        quantities=[simple_quantity_node],
    )

    yield ingredients
