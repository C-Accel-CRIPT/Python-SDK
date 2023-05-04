import copy
import json

import pytest
from util import strip_uid_from_dict

import cript


@pytest.fixture(scope="function")
def complex_parameter_node() -> cript.Parameter:
    parameter = cript.Parameter("update_frequency", 1000.0, "1/second")
    return parameter


@pytest.fixture(scope="function")
def complex_parameter_dict() -> dict:
    ret_dict = {"node": ["Parameter"], "key": "update_frequency", "value": 1000.0, "unit": "1/ns"}
    return ret_dict


@pytest.fixture(scope="function")
def complex_algorithm_node() -> cript.Algorithm:
    algorithm = cript.Algorithm("mc_barostat", "barostat")
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
        "journal_article",
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
    citation = cript.Citation("reference", complex_reference_node)
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
    ret_dict = {"node": ["Quantity"], "key": "mass", "value": 11.2, "unit": "kg", "uncertainty": 0.2, "uncertainty_type": "std"}
    return ret_dict


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
    p = cript.Property(
        "modulus_shear",
        "value",
        5.0,
        "GPa",
        0.1,
        "std",
        structure="structure",
        method="method",
        sample_preparation=[copy.deepcopy(simple_process_node)],
        conditions=[complex_condition_node],
        computations=[copy.deepcopy(simple_computation_node)],
        citations=[complex_citation_node],
        notes="notes",
    )
    return p


@pytest.fixture(scope="function")
def complex_property_dict(complex_material_node, complex_condition_dict, complex_citation_dict, complex_data_node, simple_process_node, simple_computation_node) -> dict:
    ret_dict = {
        "node": ["Property"],
        "key": "modulus_shear",
        "type": "value",
        "value": 5.0,
        "unit": "GPa",
        "uncertainty": 0.1,
        "uncertainty_type": "std",
        "structure": "structure",
        "sample_preparation": [json.loads(simple_process_node.json)],
        "method": "method",
        "conditions": [complex_condition_dict],
        "citations": [complex_citation_dict],
        "computations": [json.loads(simple_computation_node.json)],
        "notes": "notes",
    }
    return strip_uid_from_dict(ret_dict)


@pytest.fixture(scope="function")
def simple_property_node():
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
def complex_condition_node(complex_material_node, complex_data_node) -> cript.Condition:
    c = cript.Condition(
        "temp",
        "value",
        22,
        "C",
        "room temperature of lab",
        uncertainty=5,
        uncertainty_type="var",
        set_id=0,
        measurement_id=2,
        material=[complex_material_node],
        data=complex_data_node,
    )
    return c


@pytest.fixture(scope="function")
def complex_condition_dict(complex_material_node, complex_data_node) -> dict:
    ret_dict = {
        "node": ["Condition"],
        "key": "temp",
        "type": "value",
        "descriptor": "room temperature of lab",
        "value": 22,
        "unit": "C",
        "uncertainty": 5,
        "uncertainty_type": "var",
        "set_id": 0,
        "measurement_id": 2,
        "material": [json.loads(complex_material_node.json)],
        "data": json.loads(complex_data_node.json),
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_ingredient_node(complex_material_node, complex_quantity_node) -> cript.Ingredient:
    i = cript.Ingredient(complex_material_node, [complex_quantity_node], "catalyst")
    return i


@pytest.fixture(scope="function")
def complex_ingredient_dict(complex_material_node, complex_quantity_dict) -> dict:
    ret_dict = {"node": ["Ingredient"], "material": json.loads(complex_material_node.json), "quantities": [complex_quantity_dict], "keyword": "catalyst"}
    return ret_dict


@pytest.fixture(scope="function")
def complex_equipment_node(complex_condition_node, complex_citation_node) -> cript.Equipment:
    e = cript.Equipment(
        "hot plate",
        "fancy hot plate",
        conditions=[complex_condition_node],
        citations=[complex_citation_node],
    )
    return e


@pytest.fixture(scope="function")
def complex_equipment_dict(complex_condition_dict, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["Equipment"],
        "key": "hot plate",
        "description": "fancy hot plate",
        "conditions": [complex_condition_dict],
        "citations": [complex_citation_dict],
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_computational_forcefield_node(simple_data_node, complex_citation_node) -> cript.ComputationalForcefield:
    cf = cript.ComputationalForcefield(
        "opls_aa",
        "atom",
        "atom -> atom",
        "no implicit solvent",
        "local LigParGen installation",
        "this is a test forcefield",
        [simple_data_node],
        [complex_citation_node],
    )
    return cf


@pytest.fixture(scope="function")
def complex_computational_forcefield_dict(simple_data_node, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["ComputationalForcefield"],
        "key": "opls_aa",
        "building_block": "atom",
        "coarse_grained_mapping": "atom -> atom",
        "implicit_solvent": "no implicit solvent",
        "source": "local LigParGen installation",
        "description": "this is a test forcefield",
        "citation": [complex_citation_dict],
        "data": [json.loads(simple_data_node.json)],
    }
    return ret_dict


@pytest.fixture(scope="function")
def complex_software_configuration_node(complex_software_node, complex_algorithm_node, complex_citation_node) -> cript.SoftwareConfiguration:
    sc = cript.SoftwareConfiguration(complex_software_node, [complex_algorithm_node], "my_notes", [complex_citation_node])
    return sc


@pytest.fixture(scope="function")
def complex_software_configuration_dict(complex_software_dict, complex_algorithm_dict, complex_citation_dict) -> dict:
    ret_dict = {
        "node": ["SoftwareConfiguration"],
        "software": complex_software_dict,
        "algorithms": [complex_algorithm_dict],
        "notes": "my_notes",
        "citation": [complex_citation_dict],
    }
    return ret_dict
