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


def test_quantity():
    q = get_quantity()
    assert q.json == get_quantity_string()
    assert cript.load_nodes_from_json(get_quantity_string()).json == q.json

    q.key = "volume"
    assert q.key == "volume"
    q.value = 0.5
    assert q.value == 0.5
    q.unit = "l"
    assert q.unit == "l"
    q.set_uncertainty(0.1, "var")
    assert q.uncertainty == 0.1
    assert q.uncertainty_type == "var"


def test_reference():
    r = get_reference()
    assert r.json == get_reference_string()

    r2 = cript.load_nodes_from_json(r.json)
    assert r2.json == get_reference_string()

    r2.authors = ["Ludwig Schneider"]
    assert str(r2.authors) == "['Ludwig Schneider']"
    with pytest.raises(AttributeError):
        r2.url = "https://test.url"

    r2.type = "dissertation"
    assert r2.type == "dissertation"
    r2.title = "Rheology and Structure Formation in Complex Polymer Melts"
    assert r2.title == "Rheology and Structure Formation in Complex Polymer Melts"
    r2.journal = ""
    assert r2.journal == ""
    r2.publisher = "eDiss Georg-August Universität Göttingen"
    assert r2.publisher == "eDiss Georg-August Universität Göttingen"
    r2.issue = None
    assert r2.issue is None
    r2.pages = [1, 215]
    assert r2.pages == [1, 215]
    r2.doi = "10.53846/goediss-7403"
    assert r2.doi == "10.53846/goediss-7403"
    r2.issn = ""
    assert r2.issn == ""
    r2.arxiv_id = "no id"
    assert r2.arxiv_id == "no id"
    r2.pmid = 0
    assert r2.pmid == 0
    r2.website = "http://hdl.handle.net/11858/00-1735-0000-002e-e60c-c"
    assert r2.website == "http://hdl.handle.net/11858/00-1735-0000-002e-e60c-c"


def test_citation():
    c = get_citation()
    print(c.json)
    print(get_citation_string())
    assert c.json == get_citation_string()
    c.type = "replicated"
    assert c.type == "replicated"
    new_ref = get_reference()
    new_ref.title = "foo bar"
    c.reference = new_ref
    assert c.reference == new_ref


def test_software():
    s = get_software()
    assert s.json == get_software_string()
    s2 = cript.load_nodes_from_json(s.json)
    assert s2.json == s.json

    s2.name = "PySAGES"
    assert s2.name == "PySAGES"
    s2.version = "v0.3.0"
    assert s2.version == "v0.3.0"
    s2.source = "https://github.com/SSAGESLabs/PySAGES"
    assert s2.source == "https://github.com/SSAGESLabs/PySAGES"


def test_json_error():
    faulty_json = "{'node': 'Parameter', 'foo': 'bar'}".replace("'", '"')
    with pytest.raises(CRIPTJsonDeserializationError):
        cript.load_nodes_from_json(faulty_json)

    parameter = get_parameter()
    # Let's break the node by violating the data model
    parameter._json_attrs = replace(parameter._json_attrs, value=None)
    with pytest.raises(CRIPTJsonSerializationError):
        parameter.json
    # Let's break it completely
    parameter._json_attrs = None
    with pytest.raises(CRIPTJsonSerializationError):
        parameter.json


def test_property():
    p = get_property()
    print(p.json)
    print(get_property_string())
    assert p.json == get_property_string()
    p2 = cript.load_nodes_from_json(p.json)
    assert p2.json == p.json

    p2.key = "modulus_loss"
    assert p2.key == "modulus_loss"
    p2.type = "min"
    assert p2.type == "min"
    p2.set_value(600.1, "MPa")
    assert p2.value == 600.1
    assert p2.unit == "MPa"

    p2.set_uncertainty(10.5, "var")
    assert p2.uncertainty == 10.5
    assert p2.uncertainty_type == "var"

    # TODO compoments
    p2.compoments = [False]
    assert p2.compoments[0] is False
    # TODO compoments_relative
    p2.compoments_relative = [True]
    assert p2.compoments_relative[0] is True
    p2.structure = "structure2"
    assert p2.structure == "structure2"

    p2.method = "method2"
    assert p2.method == "method2"

    # TODO sample_preparation
    p2.sample_preparation = False
    assert p2.sample_preparation is False
    assert len(p2.conditions) == 1
    p2.conditions += [get_condition()]
    assert len(p2.conditions) == 2
    # TODO Data
    p2.data = True
    assert p2.data is True
    # TODO Computations
    p2.computations = [None, True, False]
    assert p2.computations[0] is None
    assert p2.computations[1] is True
    assert p2.computations[2] is False

    assert len(p2.citations) == 1
    p2.citations += [get_citation()]
    assert len(p2.citations) == 2
    p2.notes = "notes2"
    assert p2.notes == "notes2"


def test_condition():
    c = get_condition()
    assert c.json == get_condition_string()
    c2 = cript.load_nodes_from_json(c.json)
    assert c2.json == c.json

    c2.key = "pressure"
    assert c2.key == "pressure"
    c2.type = "avg"
    assert c2.type == "avg"

    c2.set_value(1, "bar")
    assert c2.value == 1
    assert c2.unit == "bar"

    c2.descriptor = "ambient pressure"
    assert c2.descriptor == "ambient pressure"

    c2.set_uncertainty(0.1, "std")
    assert c2.uncertainty == 0.1
    assert c2.uncertainty_type == "std"

    # TODO Material
    c2.material += [True]
    assert c2.material[0] is True
    c2.set_id = None
    assert c2.set_id is None
    c2.measurement_id = None
    assert c2.measurement_id is None

    # TODO data
    c2.data = False
    assert c2.data is False


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
