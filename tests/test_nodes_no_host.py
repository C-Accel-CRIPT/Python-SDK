import pytest

import cript
from cript.nodes.exceptions import CRIPTNodeSchemaError


def get_parameter():
    parameter = cript.Parameter("update_frequency", 1000.0, "1/ns")
    return parameter


def get_parameter_string():
    ret_str = "{'node': 'Parameter', 'key': 'update_frequency',"
    ret_str += " 'value': 1000.0, 'unit': '1/ns'}"
    return ret_str.replace("'", '"')


def get_algorithm_string():
    ret_str = "{'node': 'Algorithm', 'key': 'mc_barostat', 'type': 'barostat',"
    ret_str += " 'parameter': [], 'citation': []}"
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

    # Add citation test, once we have citation implemted
def test_removing_nodes():
    a = get_algorithm()
    p = get_parameter()
    a.parameter += [p]
    a.remove_child(p)
    assert a.json == get_algorithm_string()
