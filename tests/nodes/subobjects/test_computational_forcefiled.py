import copy
import json

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
