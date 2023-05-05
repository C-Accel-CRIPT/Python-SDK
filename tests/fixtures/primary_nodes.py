import copy

import pytest

import cript


@pytest.fixture(scope="function")
def simple_project_node(simple_collection_node) -> cript.Project:
    """
    create a minimal Project node with only required arguments for other tests to use

    Returns
    -------
    cript.Project
    """

    return cript.Project(name="my Project name", collection=[simple_collection_node])


@pytest.fixture(scope="function")
def complex_project_node(complex_collection_node, complex_material_node) -> cript.Project:
    """
    a complex Project node that includes all possible optional arguments that are themselves complex as well
    """
    project_name = "my project name"

    complex_project = cript.Project(name=project_name, collection=[complex_collection_node], material=[complex_material_node])

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

    my_collection = cript.Collection(name=my_collection_name, experiment=[simple_experiment_node])

    return my_collection


@pytest.fixture(scope="function")
def complex_collection_node(simple_experiment_node, simple_inventory_node, complex_citation_node) -> cript.Collection:
    """
    Collection node with all optional arguments
    """
    my_collection_name = "my complex collection name"
    my_cript_doi = "10.1038/1781168a0"

    my_collection = cript.Collection(
        name=my_collection_name,
        experiment=[simple_experiment_node],
        inventories=[simple_inventory_node],
        cript_doi=my_cript_doi,
        citations=[complex_citation_node],
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
def simple_computation_process_node() -> cript.ComputationProcess:
    """
    simple Computational Process node with only required arguments to use in other tests
    """
    my_computational_process_type = "cross_linking"

    # input data

    # TODO should be using simple_data_node fixture
    data_files = cript.File(source="https://criptapp.org", type="calibration", extension=".csv", data_dictionary="my file's data dictionary")

    input_data = cript.Data(name="my data name", type="afm_amp", file=[data_files])

    # ingredients with Material and Quantity node
    my_material = cript.Material(name="my material", identifiers=[{"alternative_names": "my material alternative name"}])

    my_quantity = cript.Quantity(key="mass", value=1.23, unit="kg")

    ingredients = cript.Ingredient(
        material=my_material,
        quantity=[my_quantity],
    )

    my_computational_process = cript.ComputationProcess(
        name="my computational process name",
        type=my_computational_process_type,
        input_data=[input_data],
        ingredient=[ingredients],
    )

    return copy.deepcopy(my_computational_process)


@pytest.fixture(scope="function")
def simple_data_node(complex_file_node) -> cript.Data:
    """
    minimal data node
    """
    my_data = cript.Data(name="my data name", type="afm_amp", file=[complex_file_node])

    return my_data


@pytest.fixture(scope="function")
def complex_data_node(
    complex_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computation_process_node,
    simple_material_node,
    complex_citation_node,
) -> None:
    """
    create a complex data node with all possible arguments for all tests to use when needed
    """
    my_complex_data = cript.Data(
        name="my complex data node name",
        type="afm_amp",
        file=[copy.deepcopy(complex_file_node)],
        sample_preperation=copy.deepcopy(simple_process_node),
        computations=[simple_computation_node],
        computational_process=[simple_computation_process_node],
        materials=[simple_material_node],
        processes=[copy.deepcopy(simple_process_node)],
        citations=[copy.deepcopy(complex_citation_node)],
    )

    return my_complex_data


@pytest.fixture(scope="function")
def simple_process_node() -> cript.Process:
    """
    simple process node to use in other tests to keep tests clean
    """
    my_process = cript.Process(name="my process name", type="affinity_pure")

    return copy.deepcopy(my_process)


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
    identifiers = [{"bigsmiles": "123456"}]
    my_material = cript.Material(name="my material", identifiers=identifiers)

    return my_material


@pytest.fixture(scope="function")
def complex_material_node(simple_property_node, simple_process_node, complex_computational_forcefield_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_identifier = [{"alternative_names": "my material alternative name"}]

    my_component = [
        cript.Material(name="my component material 1", identifiers=[{"alternative_names": "component 1 alternative name"}]),
        cript.Material(name="my component material 2", identifiers=[{"alternative_names": "component 2 alternative name"}]),
    ]

    parent_material = cript.Material(name="my parent material", identifiers=[{"alternative_names": "parent material 1"}])

    my_material_keyword = ["acetylene"]

    my_complex_material = cript.Material(
        name="my complex material",
        identifiers=my_identifier,
        component=my_component,
        property=simple_property_node,
        process=copy.deepcopy(simple_process_node),
        parent_material=parent_material,
        computational_forcefield=complex_computational_forcefield_node,
        keyword=my_material_keyword,
    )

    return copy.deepcopy(my_complex_material)


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

    my_inventory = cript.Inventory(name="my inventory name", material=[material_1, material_2])

    # use my_inventory in another test
    return my_inventory


@pytest.fixture(scope="function")
def simple_computational_process_node(simple_data_node, complex_ingredient_node) -> None:
    """
    simple/minimal computational_process node with only required arguments
    """
    my_computational_process = cript.ComputationProcess(
        name="my computational process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredient=[complex_ingredient_node],
    )

    return my_computational_process
