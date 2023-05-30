import copy
import json

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
def complex_project_dict(complex_collection_node, complex_material_node, complex_user_node) -> dict:
    project_dict = {"node": ["Project"]}
    project_dict["locked"] = True
    project_dict["model_version"] = 1.0
    project_dict["updated_by"] = complex_user_node
    project_dict["create_by"] = complex_user_node
    project_dict["public"] = True
    project_dict["name"] = "my project name"
    project_dict["notes"] = "my project notes"
    project_dict["member"] = [complex_user_node]
    project_dict["admin"] = complex_user_node
    project_dict["collection"] = [complex_collection_node]
    project_dict["material"] = [complex_material_node]


@pytest.fixture(scope="function")
def complex_project_node(complex_project_dict) -> cript.Project:
    """
    a complex Project node that includes all possible optional arguments that are themselves complex as well
    """

    complex_project = cript.load_nodes_from_json(json.dumps(complex_project_dict))

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
        inventory=[simple_inventory_node],
        doi=my_cript_doi,
        citation=[complex_citation_node],
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
def simple_computation_process_node(complex_ingredient_node, simple_data_node) -> cript.ComputationProcess:
    """
    simple Computational Process node with only required arguments to use in other tests
    """
    my_computational_process_type = "cross_linking"

    my_computational_process = cript.ComputationProcess(
        name="my computational process name",
        type=my_computational_process_type,
        input_data=[copy.deepcopy(simple_data_node)],
        ingredient=[complex_ingredient_node],
    )

    return my_computational_process


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
        sample_preparation=copy.deepcopy(simple_process_node),
        computation=[simple_computation_node],
        computation_process=[simple_computation_process_node],
        material=[simple_material_node],
        process=[copy.deepcopy(simple_process_node)],
        citation=[copy.deepcopy(complex_citation_node)],
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
def simple_material_dict() -> dict:
    """
    the dictionary that `simple_material_node` produces
    putting it in one location to make updating it easy
    """
    simple_material_dict: dict = {"node": ["Material"], "name": "my material", "bigsmiles": "123456"}

    return simple_material_dict


@pytest.fixture(scope="function")
def complex_material_node(simple_property_node, simple_process_node, complex_computational_forcefield_node, simple_material_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_identifier = [{"bigsmiles": "my complex_material_node"}]

    [
        cript.Material(name="my component material 1", identifiers=[{"bigsmiles": "component 1 bigsmiles"}]),
        cript.Material(name="my component material 2", identifiers=[{"bigsmiles": "component 2 bigsmiles"}]),
    ]

    my_material_keyword = ["acetylene"]

    my_complex_material = cript.Material(
        name="my complex material",
        identifiers=my_identifier,
        # component=my_component,
        property=[simple_property_node],
        # process=copy.deepcopy(simple_process_node),
        parent_material=simple_material_node,
        computational_forcefield=complex_computational_forcefield_node,
        keyword=my_material_keyword,
    )

    return my_complex_material


@pytest.fixture(scope="function")
def simple_software_configuration(simple_software_node) -> cript.SoftwareConfiguration:
    """
    minimal software configuration node with only required arguments
    """
    my_software_configuration = cript.SoftwareConfiguration(software=simple_software_node)

    return my_software_configuration


@pytest.fixture(scope="function")
def simple_inventory_node(simple_material_node) -> None:
    """
    minimal inventory node to use for other tests
    """
    # set up inventory node

    material_2 = cript.Material(name="material 2", identifiers=[{"bigsmiles": "my big smiles"}])

    my_inventory = cript.Inventory(name="my inventory name", material=[simple_material_node, material_2])

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
