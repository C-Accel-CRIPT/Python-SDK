import cript
import pytest
from cript.nodes.exceptions import CRIPTNodeSchemaError


def get_parameter():
    parameter = cript.Parameter("update_frequency", 1000., "1/ns")
    return parameter

def get_parameter_string():
    return "{'node': 'Parameter', 'key': 'update_frequency', 'value': 1000.0, 'unit': '1/ns'}".replace("'", "\"")

def get_algorithm():
    algorithm = cript.Algorithm("mc_barostat", "barostat")
    return algorithm

def get_algorithm_string():
    return "{'node': 'Algorithm', 'key': 'mc_barostat', 'type': 'barostat', 'parameter': [], 'citation': []}".replace("'", "\"")

def get_identifier():
    identifier = cript.Identifier("names", ["styrene", "vinylbenzene"])
    return identifier
def get_identifier_string():
    return "{'node': 'Identifier', 'key': 'names', 'value': ['styrene', 'vinylbenzene']}".replace("'", "\"")
def test_parameter():
    p = get_parameter()
    p_str = p.json
    assert p_str == get_parameter_string()
    p = cript.load_nodes_from_json(p_str)
    assert p_str == get_parameter_string()

    p.key = "advanced_sampling"
    assert p.key == "advanced_sampling"
    p.value = 15.
    assert p.value == 15.
    with pytest.raises(CRIPTNodeSchemaError):
        p.value = None
    assert p.value == 15.
    p.unit = "m"
    assert p.unit == "m"

def test_algorithm():
    a = get_algorithm()
    a_str= a.json
    assert a_str == get_algorithm_string()
    a.parameter += [get_parameter()]
    a_str= get_algorithm_string()
    a_str2 = a_str.replace("parameter\": []", f"parameter\": [{get_parameter_string()}]")
    assert a_str2 == a.json

    a2 = cript.load_nodes_from_json(a_str2)
    assert a_str2 == a2.json

    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"

    #Add citation test, once we have citation implemted

def test_identifier():
    idx = get_identifier()
    assert idx.json == get_identifier_string()
    idx2 = cript.load_nodes_from_json(idx.json)
    assert idx2.json == idx.json

    idx2.key = "smiles"
    assert idx2.key == "smiles"
    idx2.value = "c1ccccc1C=C"
    assert idx2.value == "c1ccccc1C=C"
