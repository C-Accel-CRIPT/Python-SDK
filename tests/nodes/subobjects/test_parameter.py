import json

from util import strip_uid_from_dict

import cript


def test_parameter_setter_getter(complex_parameter_node):
    p = complex_parameter_node
    p.key = "damping_time"
    assert p.key == "damping_time"
    p.value = 15.0
    assert p.value == 15.0
    p.unit = "m"
    assert p.unit == "m"


def test_paraemter_json_serialization(complex_parameter_node, complex_parameter_dict):
    p = complex_parameter_node
    p_str = p.json
    p2 = cript.load_nodes_from_json(p_str)
    p_dict = json.loads(p2.json)
    assert strip_uid_from_dict(p_dict) == complex_parameter_dict
    assert p2.json == p.json
