import copy
import json
import uuid

import pytest
from util import strip_uid_from_dict

import cript


@pytest.fixture(scope="function")
def complex_parameter_node() -> cript.Parameter:
    """
    maximal parameter sub-object that has all possible node attributes
    """
    parameter = cript.Parameter(key="update_frequency", value=1000.0, unit="1/second")

    return parameter


@pytest.fixture(scope="function")
def complex_parameter_dict() -> dict:
    ret_dict = {"node": ["Parameter"], "key": "update_frequency", "value": 1000.0, "unit": "1/second"}
    return ret_dict


# TODO this fixture should be renamed because it is simple_algorithm_subobject not complex
@pytest.fixture(scope="function")
def complex_algorithm_node() -> cript.Algorithm:
    """
    minimal algorithm sub-object
    """
    algorithm = cript.Algorithm(key="mc_barostat", type="barostat")

    return algorithm


@pytest.fixture(scope="function")
def complex_algorithm_dict() -> dict:
    ret_dict = {"node": ["Algorithm"], "key": "mc_barostat", "type": "barostat"}
    return ret_dict


@pytest.fixture(scope="function")
def complex_reference_node() -> cript.Reference:
    title = "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
    title += "SOft coarse grained Monte-Carlo Acceleration (SOMA)"

    reference = cript.Reference(
        type="journal_article",
        title=title,
        author=["Ludwig Schneider", "Marcus Müller"],
        journal="Computer Physics Communications",
        publisher="Elsevier",
        year=2019,
        pages=[463, 476],
        doi="10.1016/j.cpc.2018.08.011",
        issn="0010-4655",
        website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
    )
    return reference


@pytest.fixture(scope="function")
def complex_reference_dict() -> dict:
    ret_dict = {
        "node": ["Reference"],
        "type": "journal_article",
        "title": "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: SOft coarse grained Monte-Carlo Acceleration (SOMA)",
        "author": ["Ludwig Schneider", "Marcus Müller"],
        "journal": "Computer Physics Communications",
        "publisher": "Elsevier",
        "year": 2019,
        "pages": [463, 476],
        "doi": "10.1016/j.cpc.2018.08.011",
        "issn": "0010-4655",
        "website": "https://www.sciencedirect.com/science/article/pii/S0010465518303072",
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_citation_node(complex_reference_node) -> cript.Citation:
    """
    maximal citation sub-object with all possible node attributes
    """
    citation = cript.Citation(type="reference", reference=complex_reference_node)
    return citation


@pytest.fixture(scope="function")
def complex_citation_dict(complex_reference_dict) -> dict:
    ret_dict = {"node": ["Citation"], "reference": complex_reference_dict, "type": "reference"}
    return ret_dict


@pytest.fixture(scope="function")
def complex_quantity_node() -> cript.Quantity:
    quantity = cript.Quantity(key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev")
    return quantity


@pytest.fixture(scope="function")
def complex_quantity_dict() -> dict:
    return {"node": ["Quantity"], "key": "mass", "value": 11.2, "unit": "kg", "uncertainty": 0.2, "uncertainty_type": "stdev"}


@pytest.fixture(scope="function")
def complex_software_node() -> cript.Software:
    software = cript.Software("SOMA", "0.7.0", "https://gitlab.com/InnocentBug/SOMA")
    return software


@pytest.fixture(scope="function")
def complex_software_dict() -> dict:
    ret_dict = {"node": ["Software"], "name": "SOMA", "version": "0.7.0", "source": "https://gitlab.com/InnocentBug/SOMA"}
    return ret_dict


@pytest.fixture(scope="function")
def complex_property_node(complex_material_node, complex_condition_node, complex_citation_node, complex_data_node, simple_process_node, simple_computation_node):
    """
    a maximal property sub-object with all possible fields filled
    """
    my_complex_property = cript.Property(
        key="modulus_shear",
        type="value",
        value=5.0,
        unit="GPa",
        uncertainty=0.1,
        uncertainty_type="stdev",
        structure="structure",
        method="comp",
        sample_preparation=copy.deepcopy(simple_process_node),
        condition=[complex_condition_node],
        computation=[copy.deepcopy(simple_computation_node)],
        data=[copy.deepcopy(complex_data_node)],
        citation=[complex_citation_node],
        notes="my complex_property_node notes",
    )
    return my_complex_property


@pytest.fixture(scope="function")
def complex_property_dict(complex_material_node, complex_condition_dict, complex_citation_dict, complex_data_node, simple_process_node, simple_computation_node) -> dict:
    ret_dict = {
        "node": ["Property"],
        "key": "modulus_shear",
        "type": "value",
        "value": 5.0,
        "unit": "GPa",
        "uncertainty": 0.1,
        "uncertainty_type": "stdev",
        "structure": "structure",
        "sample_preparation": json.loads(simple_process_node.get_json(condense_to_uuid={}).json),
        "method": "comp",
        "condition": [complex_condition_dict],
        "data": [json.loads(complex_data_node.get_json(condense_to_uuid={}).json)],
        "citation": [complex_citation_dict],
        "computation": [json.loads(simple_computation_node.get_json(condense_to_uuid={}).json)],
        "notes": "my complex_property_node notes",
    }
    return strip_uid_from_dict(ret_dict)


@pytest.fixture(scope="function")
def simple_property_node() -> cript.Property:
    p = cript.Property(
        "modulus_shear",
        "value",
        5.0,
        "GPa",
    )
    return p


@pytest.fixture(scope="function")
def simple_property_dict() -> dict:
    ret_dict = {
        "node": ["Property"],
        "key": "modulus_shear",
        "type": "value",
        "value": 5.0,
        "unit": "GPa",
    }
    return strip_uid_from_dict(ret_dict)


@pytest.fixture(scope="function")
def complex_condition_node(complex_data_node) -> cript.Condition:
    my_complex_condition = cript.Condition(
        key="temperature",
        type="value",
        value=22,
        unit="C",
        descriptor="room temperature of lab",
        uncertainty=5,
        uncertainty_type="stdev",
        set_id=0,
        measurement_id=2,
        data=[copy.deepcopy(complex_data_node)],
    )
    return my_complex_condition


@pytest.fixture(scope="function")
def complex_condition_dict(complex_data_node) -> dict:
    ret_dict = {
        "node": ["Condition"],
        "key": "temperature",
        "type": "value",
        "descriptor": "room temperature of lab",
        "value": 22,
        "unit": "C",
        "uncertainty": 5,
        "uncertainty_type": "stdev",
        "set_id": 0,
        "measurement_id": 2,
        "data": [json.loads(complex_data_node.get_json(condense_to_uuid={}).json)],
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_ingredient_node(complex_material_node, complex_quantity_node) -> cript.Ingredient:
    """
    complex ingredient node with all possible parameters filled
    """
    complex_ingredient_node = cript.Ingredient(material=complex_material_node, quantity=[complex_quantity_node], keyword=["catalyst"])

    return complex_ingredient_node


@pytest.fixture(scope="function")
def complex_ingredient_dict(complex_material_node, complex_quantity_dict) -> dict:
    ret_dict = {"node": ["Ingredient"], "material": json.loads(complex_material_node.json), "quantity": [complex_quantity_dict], "keyword": ["catalyst"]}
    return ret_dict


@pytest.fixture(scope="function")
def simple_ingredient_node(simple_material_node, complex_quantity_node) -> cript.Ingredient:
    """
    minimal ingredient sub-object used for testing

    Notes
    ----
    The main difference is that this uses a simple material with less chance of getting any errors
    """

    simple_material_node.name = f"{simple_material_node.name}_{uuid.uuid4().hex}"

    my_simple_ingredient = cript.Ingredient(material=simple_material_node, quantity=[complex_quantity_node], keyword=["catalyst"])

    return my_simple_ingredient


@pytest.fixture(scope="function")
def complex_equipment_node(complex_condition_node, complex_citation_node) -> cript.Equipment:
    """
    maximal equipment node with all possible attributes
    """
    my_complex_equipment = cript.Equipment(
        key="hot_plate",
        description="fancy hot plate for complex_equipment_node",
        condition=[complex_condition_node],
        citation=[complex_citation_node],
    )
    return my_complex_equipment


@pytest.fixture(scope="function")
def simple_equipment_node() -> cript.Equipment:
    """
    simple and minimal equipment
    """
    my_equipment = cript.Equipment(key="burner", description="my simple equipment fixture description")
    return my_equipment


@pytest.fixture(scope="function")
def complex_equipment_dict(complex_condition_dict, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["Equipment"],
        "key": "hot_plate",
        "description": "fancy hot plate for complex_equipment_node",
        "condition": [complex_condition_dict],
        "citation": [complex_citation_dict],
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_computational_forcefield_node(simple_data_node, complex_citation_node) -> cript.ComputationalForcefield:
    """
    maximal computational_forcefield sub-object with all possible arguments included in it
    """
    my_complex_computational_forcefield_node = cript.ComputationalForcefield(
        key="opls_aa",
        building_block="atom",
        coarse_grained_mapping="atom -> atom",
        implicit_solvent="no implicit solvent",
        source="local LigParGen installation",
        description="this is a test forcefield for complex_computational_forcefield_node",
        data=[simple_data_node],
        citation=[complex_citation_node],
    )
    return my_complex_computational_forcefield_node


@pytest.fixture(scope="function")
def complex_computational_forcefield_dict(simple_data_node, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["ComputationalForcefield"],
        "key": "opls_aa",
        "building_block": "atom",
        "coarse_grained_mapping": "atom -> atom",
        "implicit_solvent": "no implicit solvent",
        "source": "local LigParGen installation",
        "description": "this is a test forcefield for complex_computational_forcefield_node",
        "citation": [complex_citation_dict],
        "data": [json.loads(simple_data_node.json)],
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_software_configuration_node(complex_software_node, complex_algorithm_node, complex_citation_node) -> cript.SoftwareConfiguration:
    """
    maximal software_configuration sub-object with all possible attributes
    """
    my_complex_software_configuration_node = cript.SoftwareConfiguration(software=complex_software_node, algorithm=[complex_algorithm_node], notes="my_complex_software_configuration_node notes", citation=[complex_citation_node])
    return my_complex_software_configuration_node


@pytest.fixture(scope="function")
def complex_software_configuration_dict(complex_software_dict, complex_algorithm_dict, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["SoftwareConfiguration"],
        "software": complex_software_dict,
        "algorithm": [complex_algorithm_dict],
        "notes": "my_complex_software_configuration_node notes",
        "citation": [complex_citation_dict],
    }
    return ret_dict


@pytest.fixture(scope="function")
def simple_software_configuration(complex_software_node) -> cript.SoftwareConfiguration:
    """
    minimal software configuration node with only required arguments
    """
    my_software_configuration = cript.SoftwareConfiguration(software=complex_software_node)

    return my_software_configuration


@pytest.fixture(scope="function")
def simple_computational_forcefield_node():
    """
    simple minimal computational forcefield node
    """

    return cript.ComputationalForcefield(key="amber", building_block="atom")


@pytest.fixture(scope="function")
def simple_condition_node() -> cript.Condition:
    """
    simple and minimal condition node
    """
    return cript.Condition(key="atm", type="max", value=1)
