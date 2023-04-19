import json

import cript


def test_create_parameter(simple_parameter_node):
    p = simple_parameter_node


def test_parameter_setter_getter(simple_parameter_node):
    p = simple_parameter_node
    p.key = "advanced_sampling"
    assert p.key == "advanced_sampling"
    p.value = 15.0
    assert p.value == 15.0
    p.unit = "m"
    assert p.unit == "m"


def test_paraemter_json_serialization(simple_parameter_node, simple_parameter_dict):
    p = simple_parameter_node
    p_str = p.json
    p2 = cript.load_nodes_from_json(p_str)
    p_dict = json.loads(p2.json)
    assert p_dict == simple_parameter_dict
