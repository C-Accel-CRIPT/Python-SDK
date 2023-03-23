from dataclasses import replace

import pytest

import cript
from cript.nodes.exceptions import (
    CRIPTJsonDeserializationError,
    CRIPTJsonSerializationError,
    CRIPTNodeSchemaError,
)


def get_parameter():
    parameter = cript.Parameter("update_frequency", 1000.0, "1/ns")
    return parameter


def get_parameter_string():
    ret_str = "{'node': 'Parameter', 'key': 'update_frequency',"
    ret_str += " 'value': 1000.0, 'unit': '1/ns'}"
    return ret_str.replace("'", '"')


def get_algorithm():
    algorithm = cript.Algorithm("mc_barostat", "barostat")
    return algorithm


def get_algorithm_string():
    ret_str = "{'node': 'Algorithm', 'key': 'mc_barostat', 'type': 'barostat',"
    ret_str += " 'parameter': [], 'citation': []}"
    return ret_str.replace("'", '"')


def get_quantity():
    quantity = cript.Quantity("mass", 11.2, "kg", 0.2, "std")
    return quantity


def get_quantity_string():
    ret_str = "{'node': 'Quantity', 'key': 'mass', 'value': 11.2, "
    ret_str += "'unit': 'kg', 'uncertainty': 0.2, 'uncertainty_type': 'std'}"
    return ret_str.replace("'", '"')


def get_reference():
    reference = cript.Reference(
        "journal_article",
        authors=["Ludwig Schneider", "Marcus Müller"],
        journal="Computer Physics Communications",
        publisher="Elsevier",
        year=2019,
        pages=[463, 476],
        doi="10.1016/j.cpc.2018.08.011",
        issn="0010-4655",
        website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
    )
    return reference


def get_reference_string():
    ret_str = "{'node': 'Reference', 'url': '', 'type': 'journal_article', 'title': '', 'authors':"
    ret_str += " ['Ludwig Schneider', 'Marcus M\\u00fcller'], 'journal': 'Computer Physics Communications', "
    ret_str += "'publisher': 'Elsevier', 'year': 2019, 'issue': null, 'pages': [463, 476], "
    ret_str += "'doi': '10.1016/j.cpc.2018.08.011', 'issn': '0010-4655', 'arxiv_id': '', "
    ret_str += "'pmid': null, 'website': 'https://www.sciencedirect.com/science/article/pii/S0010465518303072'}"
    return ret_str.replace("'", '"')


def get_citation():
    citation = cript.Citation("reference", get_reference())
    return citation


def get_citation_string():
    return "{'node': 'Citation', 'type': 'reference', 'reference':}".replace(
        "'reference':", f"'reference': {get_reference_string()}"
    ).replace("'", '"')


def get_software():
    software = cript.Software("SOMA", "0.7.0", "https://gitlab.com/InnocentBug/SOMA")
    return software


def get_software_string():
    ret_str = "{'node': 'Software', 'url': '', 'name': 'SOMA',"
    ret_str += " 'version': '0.7.0', 'source': 'https://gitlab.com/InnocentBug/SOMA'}"
    return ret_str.replace("'", '"')


def test_parameter():
    p = get_parameter()
    p_str = p.json
    assert p_str == get_parameter_string()
    p = cript.load_nodes_from_json(p_str)
    assert p_str == get_parameter_string()

    p.key = "advanced_sampling"
    assert p.key == "advanced_sampling"
    p.value = 15.0
    assert p.value == 15.0
    with pytest.raises(CRIPTNodeSchemaError):
        p.value = None
    assert p.value == 15.0
    p.unit = "m"
    assert p.unit == "m"


def test_algorithm():
    a = get_algorithm()
    a_str = a.json
    assert a_str == get_algorithm_string()
    a.parameter += [get_parameter()]
    a_str = get_algorithm_string()
    a_str2 = a_str.replace('parameter": []', f'parameter": [{get_parameter_string()}]')
    assert a_str2 == a.json

    a2 = cript.load_nodes_from_json(a_str2)
    assert a_str2 == a2.json

    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"
    a.citation += [get_citation()]
    assert a.citation[0].json == get_citation().json


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


def test_removing_nodes():
    a = get_algorithm()
    p = get_parameter()
    a.parameter += [p]
    a.remove_child(p)
    assert a.json == get_algorithm_string()


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

    faulty_json = "{'node': 'Parameter', 'key': 'update_frequency', 'value': 1000.0, 'unit': '1/ns', 'foo': 'bar'}".replace(
        "'", '"'
    )
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


def get_property():
    p = cript.Property(
        "modulus_shear",
        "value",
        5.0,
        "GPa",
        0.1,
        "std",
        # TODO components
        [None],
        # TODO components_relative
        [None],
        structure="structure",
        method="method",
        # TODO sample_preparation
        sample_preparation=None,
        conditions=[get_condition()],
        # TODO data
        data=None,
        # TODO computations
        computations=[None],
        citations=[get_citation()],
        notes="notes",
    )
    return p


def get_property_string():
    ret_str = "{'node': 'Property', 'key': 'modulus_shear', 'type': 'value', 'value': 5.0,"
    ret_str += " 'unit': 'GPa', 'uncertainty': 0.1, 'uncertainty_type': 'std', "
    ret_str += "'components': [null], 'components_relative': [null], 'structure': 'structure', "
    ret_str += f"'method': 'method', 'sample_preparation': null, 'conditions': [{get_condition_string()}], 'data': null,"
    ret_str += f" 'computations': [null], 'citations': [{get_citation_string()}], 'notes': 'notes'" + "}"
    return ret_str.replace("'", '"')


def test_property():
    p = get_property()
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


def get_condition():
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
    )  # TODO data, material
    return c


def get_condition_string():
    ret_str = "{'node': 'Condition', 'key': 'temp', 'type': 'value', "
    ret_str += "'descriptor': 'room temperature of lab', 'value': 22, 'unit': 'C',"
    ret_str += " 'uncertainty': 5, 'uncertainty_type': 'var', 'material': [], "
    ret_str += "'set_id': 0, 'measurement_id': 2, 'data': null}"
    return ret_str.replace("'", '"')


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

    c2.set_id = None
    assert c2.set_id is None
    c2.measurement_id = None
    assert c2.measurement_id is None

    # TODO data


def get_ingredient():
    # TODO replace material
    i = cript.Ingredient(None, [get_quantity()], "catalyst")
    return i


def get_ingredient_string():
    ret_str = "{'node': 'Ingredient', 'material': null, "
    ret_str += f"'quantities': [{get_quantity_string()}],"
    ret_str += " 'keyword': 'catalyst'}"
    return ret_str.replace("'", '"')


def test_ingredient():
    i = get_ingredient()
    assert i.json == get_ingredient_string()
    i2 = cript.load_nodes_from_json(i.json)
    assert i.json == i2.json

    q2 = get_quantity()
    i2.set_material(False, [q2])
    assert i2.material is False
    assert i2.quantities[0] is q2

    i2.keyword = "monomer"
    assert i2.keyword == "monomer"
