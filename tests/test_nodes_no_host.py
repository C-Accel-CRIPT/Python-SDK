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


def test_local_search():
    a = get_algorithm()

    # Check if we can use search to find the algoritm node, but specifying node and key
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc_barostat"})
    assert find_algorithms == [a]
    # Check if it corretcly exclude the algorithm if key is specified to non-existent value
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc"})
    assert find_algorithms == []

    # Adding 2 separate parameters to test deeper search
    p1 = get_parameter()
    p2 = get_parameter()
    p2.key = "advanced_sampling"
    p2.value = 15.0
    p2.unit = "m"
    a.parameter += [p1, p2]

    # Test if we can find a specific one of the parameters
    find_parameter = a.find_children({"key": "advanced_sampling"})
    assert find_parameter == [p2]

    # Test to find the other parameter
    find_parameter = a.find_children({"key": "update_frequency"})
    assert find_parameter == [p1]

    # Test if correctly find no paramter if we are searching for a non-existent parameter
    find_parameter = a.find_children({"key": "update"})
    assert find_parameter == []

    # Test nested search. Here we are looking for any node that has a child node parameter as specified.
    find_algorithms = a.find_children({"parameter": {"key": "advanced_sampling"}})
    assert find_algorithms == [a]
    # Same as before, but specifiying two children that have to be present (AND condition)
    find_algorithms = a.find_children({"parameter": [{"key": "advanced_sampling"}, {"key": "update_frequency"}]})
    assert find_algorithms == [a]

    # Test that the main node is correctly excluded if we specify an additionally non-existent paramter
    find_algorithms = a.find_children(
        {"parameter": [{"key": "advanced_sampling"}, {"key": "update_frequency"}, {"foo": "bar"}]}
    )
    assert find_algorithms == []


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
