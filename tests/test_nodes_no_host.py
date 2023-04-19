import copy
import json
from dataclasses import replace

import pytest

import cript
from cript.nodes.exceptions import (
    CRIPTJsonDeserializationError,
    CRIPTJsonSerializationError,
    CRIPTNodeSchemaError,
)


def test_ingredient():
    i = get_ingredient()
    assert i.json == get_ingredient_string()
    print(i.json)
    i2 = cript.load_nodes_from_json(i.json)
    assert i.json == i2.json

    q2 = get_quantity()
    i2.set_material(False, [q2])
    assert i2.material is False
    assert i2.quantities[0] is q2

    i2.keyword = "monomer"
    assert i2.keyword == "monomer"


def test_equipment():
    e = get_equipment()
    assert e.json == get_equipment_string()
    e2 = cript.load_nodes_from_json(e.json)
    assert e.json == e2.json

    e2.key = "glassware"
    assert e2.key == "glassware"
    e2.description = "Fancy glassware"
    assert e2.description == "Fancy glassware"

    assert len(e2.conditions) == 1
    c2 = get_condition()
    e2.conditions += [c2]
    assert e2.conditions[1] == c2

    assert len(e2.files) == 0
    e2.files += [False]
    assert e2.files[0] is False

    cit2 = get_citation()
    assert len(e2.citations) == 1
    e2.citations += [cit2]
    assert e2.citations[1] == cit2


def test_computation_forcefield():
    cf = get_computation_forcefield()
    assert cf.json == get_computation_forcefield_string()
    cf2 = cript.load_nodes_from_json(cf.json)
    assert cf.json == cf2.json

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
    citation2 = get_citation()
    cf2.citation += [citation2]
    assert cf2.citation[1] == citation2


def test_software_configuration():
    sc = get_software_configuration()
    assert sc.json == get_software_configuration_string()
    sc2 = cript.load_nodes_from_json(sc.json)
    assert sc2.json == sc.json

    software2 = copy.deepcopy(sc.software)
    sc2.software = software2
    assert sc2.software is not sc.software
    assert sc2.software is software2

    assert len(sc2.algorithms) == 1
    al2 = get_algorithm()
    sc2.algorithms += [al2]
    assert sc2.algorithms[1] is al2

    sc2.notes = "my new fancy notes"
    assert sc2.notes == "my new fancy notes"

    cit2 = get_citation()
    assert len(sc2.citation) == 1
    sc2.citation += [cit2]
    assert sc2.citation[1] == cit2
