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
# TODO all complex nodes and getters need notes attributes
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
def complex_project_node(complex_collection_node, complex_material_node) -> cript.Project:
    """
    a complex Project node that includes all possible optional arguments that are themselves complex as well
    """
    project_name = "my project name"

    complex_project = cript.Project(name=project_name, collections=[complex_collection_node], materials=[complex_material_node])

    return complex_project


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
    # TODO should be using simple_data_node fixture
    data_files = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary"
    )

    input_data = cript.Data(name="my data name", type="afm_amp", files=[data_files])

    # ingredients with Material and Quantity node
    my_material = cript.Material(name="my material", identifiers=[{"alternative_names": "my material alternative name"}])

    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    ingredients = cript.Ingredient(
        material=my_material,
        quantities=[my_quantity],
    )

    my_computational_process = cript.ComputationalProcess(
        name="my computational process name",
        type=my_computational_process_type,
        input_data=[input_data],
        ingredients=[ingredients],
    )

    return my_computational_process


@pytest.fixture(scope="function")
def simple_data_node(simple_file_node) -> cript.Data:
    """
    minimal data node
    """
    my_data = cript.Data(name="my data name", type="afm_amp", files=[simple_file_node])

    return my_data


@pytest.fixture(scope="fucntion")
def test_create_complex_data_node(
    simple_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_material_node,
    simple_citation_node,
) -> None:
    """
    create a complex data node with all possible arguments for all tests to use when needed
    """
    my_complex_data = cript.Data(
        name="my complex data node name",
        type="afm_amp",
        files=[simple_file_node],
        sample_preperation=simple_process_node,
        computations=[simple_computation_node],
        computational_process=[simple_computational_process_node],
        materials=[simple_material_node],
        processes=[simple_process_node],
        citations=[simple_citation_node],
    )

    return my_complex_data


@pytest.fixture(scope="function")
def simple_process_node() -> cript.Process:
    """
    simple process node to use in other tests to keep tests clean
    """
    my_process = cript.Process(name="my process name", type="affinity_pure")

    return my_process


@pytest.fixture(scope="function")
def simple_computation_node() -> cript.Computation:
    """
    simple computation node to use between tests
    """
    my_computation = cript.Computation(name="my computation name", type="analysis")

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
def complex_material_node(simple_property_node, simple_process_node, simple_computation_forcefield) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_identifier = [{"alternative_names": "my material alternative name"}]

    my_components = [
        cript.Material(name="my component material 1", identifiers=[{"alternative_names": "component 1 alternative name"}]),
        cript.Material(name="my component material 2", identifiers=[{"alternative_names": "component 2 alternative name"}]),
    ]

    parent_material = cript.Material(name="my parent material", identifiers=[{"alternative_names": "parent material 1"}])

    my_material_keywords = ["acetylene"]

    my_complex_material = cript.Material(
        name="my complex material",
        identifiers=my_identifier,
        components=my_components,
        properties=simple_property_node,
        process=simple_process_node,
        parent_materials=parent_material,
        computation_forcefield=simple_computation_forcefield,
        keywords=my_material_keywords,
    )

    return my_complex_material


@pytest.fixture(scope="function")
def simple_reference_node() -> cript.Reference:
    """
    minimal reference node
    """
    my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")

    return my_reference


@pytest.fixture(scope="function")
def complex_reference_node() -> cript.Reference:
    """
    complex reference node with all possible reference node arguments to use for other tests
    """
    return cript.Reference(
        type="journal_article",
        title="Adding the Effect of Topological Defects to the Flory\u2013Rehner and Bray\u2013Merrill Swelling Theories",
        authors=["Nathan J. Rebello", "Haley K. Beech", "Bradley D. Olsen"],
        journal="ACS Macro Letters",
        publisher="American Chemical Society",
        year=2022,
        volume=10,
        issue=None,
        pages=[531, 537],
        doi="10.1021/acsmacrolett.0c00909",
        issn="",
        arxiv_id="",
        pmid=None,
        website="",
    )


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

    my_inventory = cript.Inventory(name="my inventory name", materials_list=[material_1, material_2])

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


@pytest.fixture(scope="function")
def simple_computation_forcefield() -> cript.ComputationForcefield:
    """
    create a minimal computation_forcefield to use for other tests
    """
    return cript.ComputationForcefield(key="amber", building_block="atom")
