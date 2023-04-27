import json

from util import strip_uid_from_dict

import cript


def test_computation_forcefield(complex_computation_forcefield_node, complex_computation_forcefield_dict):
    cf = complex_computation_forcefield_node
    cf_dict = strip_uid_from_dict(json.loads(cf.json))
    assert cf_dict == strip_uid_from_dict(complex_computation_forcefield_dict)
    cf2 = cript.load_nodes_from_json(cf.json)
    assert strip_uid_from_dict(json.loads(cf.json)) == strip_uid_from_dict(json.loads(cf2.json))


def test_setter_getter(complex_computation_forcefield_node, complex_citation_node):
    cf2 = complex_computation_forcefield_node
    cf2.key = "Kremer-Grest"
    assert cf2.key == "Kremer-Grest"

    cf2.building_block = "monomer"
    assert cf2.building_block == "monomer"

    cf2.implicit_solvent = ""
    assert cf2.implicit_solvent == ""

    cf2.source = "Iterative Boltzmann inversion"
    assert cf2.source == "Iterative Boltzmann inversion"

    cf2.description = "generic polymer model"
    assert cf2.description == "generic polymer model"

    cf2.data = False
    assert cf2.data is False

    assert len(cf2.citation) == 1
    citation2 = complex_citation_node
    cf2.citation += [citation2]
    assert cf2.citation[1] == citation2