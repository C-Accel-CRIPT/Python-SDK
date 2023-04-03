"""
This conftest file contains simple nodes (nodes with minimal required arguments)
and complex node (nodes that have all possible arguments), to use for testing.

Since nodes often depend on other nodes copying and pasting nodes is not ideal,
and keeping all nodes in one file makes it easier/cleaner to create tests.

The fixtures are all functional fixtures that stay consistent between all tests.
"""


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


@pytest.fixture(scope="function")
def simple_project_node(simple_collection_node) -> cript.Project:
    """
    create a minimal Project node with only required arguments for other tests to use

    Returns
    -------
    cript.Project
    """

    return cript.Project(name="my Project name", collections=[simple_collection_node])


@pytest.fixture(scope="function")
def simple_collection_node(simple_experiment_node) -> cript.Collection:
    """
    create a simple collection node for other tests to be able to easily and cleanly reuse

    Notes
    -----
    * [Collection](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=8)
    has no required attributes.
    * The Python SDK only requires Collections to have `name`
        * Since it doesn't make sense to have an empty Collection I added an Experiment to the Collection as well
    """
    my_collection_name = "my collection name"

    my_collection = cript.Collection(name=my_collection_name, experiments=[simple_experiment_node])

    return my_collection


@pytest.fixture(scope="function")
def complex_collection_node(simple_experiment_node, simple_inventory_node, simple_citation_node) -> cript.Collection:
    """
    Collection node with all optional arguments
    """
    my_collection_name = "my complex collection name"
    my_cript_doi = "10.1038/1781168a0"

    my_collection = cript.Collection(
        name=my_collection_name,
        experiments=[simple_experiment_node],
        inventories=[simple_inventory_node],
        cript_doi=my_cript_doi,
        citations=[simple_citation_node],
    )

    return my_collection


@pytest.fixture(scope="function")
def simple_experiment_node() -> cript.Experiment:
    """
    minimal experiment node to use for other tests

    Returns
    -------
    Experiment
    """

    return cript.Experiment(name="my experiment name")


@pytest.fixture(scope="function")
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
    my_material = cript.Material(name="my material", identifiers=[{"alternative_names": "my material alternative name"}])

    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    ingredients = cript.Ingredient(
        material=my_material,
        quantities=[my_quantity],
    )

    my_computational_process = cript.ComputationalProcess(
        type=my_computational_process_type, input_data=[input_data], ingredients=[ingredients]
    )

    return my_computational_process


@pytest.fixture(scope="function")
def simple_data_node(simple_file_node) -> cript.Data:
    """
    minimal data node
    """
    my_data = cript.Data(type="afm_amp", files=[simple_file_node])

    return my_data


@pytest.fixture(scope="function")
def simple_process_node() -> cript.Process:
    """
    simple process node to use in other tests to keep tests clean
    """
    my_process = cript.Process(type="affinity_pure")

    return my_process


@pytest.fixture(scope="function")
def simple_computation_node() -> cript.Computation:
    """
    simple computation node to use between tests
    """
    my_computation = cript.Computation(type="analysis")

    return my_computation


@pytest.fixture(scope="function")
def simple_material_node() -> cript.Material:
    """
    simple material node to use between tests
    """
    identifiers = [{"alternative_names": "my material alternative name"}]
    my_material = cript.Material(name="my material", identifiers=identifiers)

    return my_material


@pytest.fixture(scope="function")
def simple_reference_node() -> cript.Reference:
    """
    minimal reference node
    """
    my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

    return my_reference


@pytest.fixture(scope="function")
def simple_software_node() -> cript.Software:
    """
    minimal software node with only required arguments
    """
    my_software = cript.Software("my software name", version="1.2.3")

    return my_software


@pytest.fixture(scope="function")
def simple_software_configuration(simple_software_node) -> cript.SoftwareConfiguration:
    """
    minimal software configuration node with only required arguments
    """
    my_software_configuration = cript.SoftwareConfiguration(software=simple_software_node)

    return my_software_configuration


@pytest.fixture(scope="function")
def simple_inventory_node() -> None:
    """
    minimal inventory node to use for other tests
    """
    # set up inventory node
    material_1 = cript.Material(name="material 1", identifiers=[{"alternative_names": "material 1 alternative name"}])

    material_2 = cript.Material(name="material 2", identifiers=[{"alternative_names": "material 2 alternative name"}])

    my_inventory = cript.Inventory(materials_list=[material_1, material_2])

    # use my_inventory in another test
    return my_inventory


# ---------- Subobjects Nodes ----------
@pytest.fixture(scope="function")
def simple_condition_node() -> cript.Condition:
    """
    minimal condition node
    """
    my_condition = cript.Condition(key="atm", type="min", value=1)

    return my_condition


@pytest.fixture(scope="function")
def simple_equipment_node() -> cript.Equipment:
    """
    minimal condition node to reuse for tests
    """
    my_equipment = cript.Equipment(key="burner")

    return my_equipment


@pytest.fixture(scope="function")
def simple_property_node() -> cript.Property:
    """
    minimal Property node to reuse for tests
    """
    # TODO key and type might not be correct, check later
    my_property = cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")

    return my_property


# ---------- Supporting Nodes ----------
@pytest.fixture(scope="function")
def simple_file_node() -> cript.File:
    """
    simple file node with only required arguments
    """
    my_file = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
    )

    return my_file


@pytest.fixture(scope="function")
def simple_citation_node(simple_reference_node) -> cript.Citation:
    """
    minimal citation node
    """
    my_citation = cript.Citation(type="derived_from", reference=simple_reference_node)

    return my_citation


@pytest.fixture(scope="function")
def simple_quantity_node() -> cript.Quantity:
    """
    minimal quantity node
    """
    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    return my_quantity


@pytest.fixture(scope="function")
def simple_ingredient_node(simple_material_node, simple_quantity_node) -> cript.Ingredient:
    """
    minimal ingredient node
    """
    ingredients = cript.Ingredient(
        material=simple_material_node,
        quantities=[simple_quantity_node],
    )

    return ingredients
