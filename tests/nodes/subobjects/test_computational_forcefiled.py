import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript


def test_computational_forcefield(complex_computational_forcefield_node, complex_computational_forcefield_dict):
    cf = complex_computational_forcefield_node
    cf_dict = strip_uid_from_dict(json.loads(cf.json))
    assert cf_dict == strip_uid_from_dict(complex_computational_forcefield_dict)
    cf2 = cript.load_nodes_from_json(cf.json)
    assert strip_uid_from_dict(json.loads(cf.json)) == strip_uid_from_dict(json.loads(cf2.json))


def test_setter_getter(complex_computational_forcefield_node, complex_citation_node, simple_data_node):
    cf2 = complex_computational_forcefield_node
    cf2.key = "opls_ua"
    assert cf2.key == "opls_ua"

    cf2.building_block = "united_atoms"
    assert cf2.building_block == "united_atoms"

    cf2.implicit_solvent = ""
    assert cf2.implicit_solvent == ""

    cf2.source = "Iterative Boltzmann inversion"
    assert cf2.source == "Iterative Boltzmann inversion"

    cf2.description = "generic polymer model"
    assert cf2.description == "generic polymer model"

    data = copy.deepcopy(simple_data_node)
    cf2.data += [data]
    assert cf2.data[-1] is data

    assert len(cf2.citation) == 1
    citation2 = copy.deepcopy(complex_citation_node)
    cf2.citation += [citation2]
    assert cf2.citation[1] == citation2


def test_integration_computational_forcefield(cript_api, simple_project_node, simple_material_node, simple_computational_forcefield_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_computational_forcefield_{uuid.uuid4().hex}"

    # renaming to avoid API duplicate node error
    simple_material_node.name = f"{simple_material_node.name}_{uuid.uuid4().hex}"

    simple_project_node.material = [simple_material_node]
    simple_project_node.material[0].computational_forcefield = simple_computational_forcefield_node

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # change simple attribute to trigger update
    simple_project_node.material[0].computational_forcefield.description = "material computational_forcefield description UPDATED"
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
