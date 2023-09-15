import copy
import json
import uuid

import pytest
from tests.utils.util import strip_uid_from_dict

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
def complex_project_dict(complex_collection_node, simple_material_node, complex_user_node) -> dict:
    project_dict = {"node": ["Project"]}
    project_dict["locked"] = True
    project_dict["model_version"] = "1.0.0"
    project_dict["updated_by"] = json.loads(copy.deepcopy(complex_user_node).get_json(condense_to_uuid={}).json)
    project_dict["created_by"] = json.loads(complex_user_node.get_json(condense_to_uuid={}).json)
    project_dict["public"] = True
    project_dict["name"] = "my project name"
    project_dict["notes"] = "my project notes"
    project_dict["member"] = [json.loads(complex_user_node.get_json(condense_to_uuid={}).json)]
    project_dict["admin"] = [json.loads(complex_user_node.get_json(condense_to_uuid={}).json)]
    project_dict["collection"] = [json.loads(complex_collection_node.get_json(condense_to_uuid={}).json)]
    project_dict["material"] = [json.loads(copy.deepcopy(simple_material_node).get_json(condense_to_uuid={}).json)]
    return project_dict


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

    return my_process


@pytest.fixture(scope="function")
def complex_process_node(complex_ingredient_node, simple_equipment_node, complex_citation_node, simple_property_node, simple_condition_node, simple_material_node, simple_process_node) -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """

    my_process_name = "my complex process node name"
    my_process_type = "affinity_pure"
    my_process_description = "my simple material description"

    process_waste = [
        cript.Material(name="my process waste material 1", identifier=[{"bigsmiles": "process waste bigsmiles"}]),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    my_complex_process = cript.Process(
        name=my_process_name,
        type=my_process_type,
        ingredient=[complex_ingredient_node],
        description=my_process_description,
        equipment=[simple_equipment_node],
        product=[simple_material_node],
        waste=process_waste,
        prerequisite_process=[simple_process_node],
        condition=[simple_condition_node],
        property=[simple_property_node],
        keyword=my_process_keywords,
        citation=[complex_citation_node],
    )

    return my_complex_process


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
    identifier = [{"bigsmiles": "123456"}]
    # Use a unique name
    my_material = cript.Material(name="my test material " + str(uuid.uuid4()), identifier=identifier)

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
def complex_material_dict(simple_property_node, simple_process_node, complex_computational_forcefield_node, simple_material_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_material_keyword = ["acetylene"]

    material_dict = {"node": ["Material"]}
    material_dict["name"] = "my complex material"
    material_dict["property"] = [json.loads(simple_property_node.get_json(condense_to_uuid={}).json)]
    material_dict["process"] = json.loads(simple_process_node.get_json(condense_to_uuid={}).json)
    material_dict["parent_material"] = json.loads(simple_material_node.get_json(condense_to_uuid={}).json)
    material_dict["computational_forcefield"] = json.loads(complex_computational_forcefield_node.get_json(condense_to_uuid={}).json)
    material_dict["bigsmiles"] = "my complex_material_node"
    material_dict["keyword"] = my_material_keyword

    return strip_uid_from_dict(material_dict)


@pytest.fixture(scope="function")
def complex_material_node(simple_property_node, simple_process_node, complex_computational_forcefield_node, simple_material_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_identifier = [{"bigsmiles": "my complex_material_node"}]
    my_material_keyword = ["acetylene"]

    my_complex_material = cript.Material(
        name="my complex material",
        identifier=my_identifier,
        property=[simple_property_node],
        process=copy.deepcopy(simple_process_node),
        parent_material=simple_material_node,
        computational_forcefield=complex_computational_forcefield_node,
        keyword=my_material_keyword,
    )

    return my_complex_material


@pytest.fixture(scope="function")
def simple_inventory_node(simple_material_node) -> None:
    """
    minimal inventory node to use for other tests
    """
    # set up inventory node

    material_2 = cript.Material(name="material 2 " + str(uuid.uuid4()), identifier=[{"bigsmiles": "my big smiles"}])

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


@pytest.fixture(scope="function")
def simplest_computational_process_node(simple_data_node, simple_ingredient_node) -> cript.ComputationProcess:
    """
    minimal computational_process node
    """
    my_simplest_computational_process = cript.ComputationProcess(
        name="my computational process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredient=[simple_ingredient_node],
    )

    return my_simplest_computational_process
