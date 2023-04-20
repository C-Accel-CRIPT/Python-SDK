import json

from util import strip_uid_from_dict

import cript


def test_computation_forcefield(simple_computation_forcefield_node, simple_computation_forcefield_dict):
    cf = simple_computation_forcefield_node
    cf_dict = strip_uid_from_dict(json.loads(cf.json))
    assert cf_dict == strip_uid_from_dict(simple_computation_forcefield_dict)
    cf2 = cript.load_nodes_from_json(cf.json)
    assert cf.json == cf2.json


def test_setter_getter(simple_computation_forcefield_node, simple_citation_node):
    cf2 = simple_computation_forcefield_node
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
    citation2 = simple_citation_node
    cf2.citation += [citation2]
    assert cf2.citation[1] == citation2
