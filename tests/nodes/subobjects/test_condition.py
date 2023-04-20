import json

from util import strip_uid_from_dict

import cript


def test_json(simple_condition_node, simple_condition_dict):
    c = simple_condition_node
    c_dict = json.loads(c.json)
    assert strip_uid_from_dict(c_dict) == strip_uid_from_dict(simple_condition_dict)
    c2 = cript.load_nodes_from_json(c.json)
    assert c2.json == c.json


def test_setter_getters(simple_condition_node, simple_material_node, simple_data_node):
    c2 = simple_condition_node
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

    c2.material += [simple_material_node]
    assert c2.material[-1] is simple_material_node
    c2.set_id = None
    assert c2.set_id is None
    c2.measurement_id = None
    assert c2.measurement_id is None

    c2.data = simple_data_node
    assert c2.data is simple_data_node
