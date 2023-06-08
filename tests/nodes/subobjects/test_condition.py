import copy
import json

from util import strip_uid_from_dict

import cript


def test_json(complex_condition_node, complex_condition_dict):
    c = complex_condition_node
    c_dict = json.loads(c.json)
    assert strip_uid_from_dict(c_dict) == strip_uid_from_dict(complex_condition_dict)
    c_deepcopy = copy.deepcopy(c)
    c2 = cript.load_nodes_from_json(c_deepcopy.json)
    assert strip_uid_from_dict(json.loads(c2.json)) == strip_uid_from_dict(json.loads(c.json))


def test_setter_getters(complex_condition_node, simple_material_node, complex_data_node):
    c2 = complex_condition_node
    c2.key = "pressure"
    assert c2.key == "pressure"
    c2.type = "avg"
    assert c2.type == "avg"

    c2.set_value(1, "bar")
    assert c2.value == 1
    assert c2.unit == "bar"

    c2.descriptor = "ambient pressure"
    assert c2.descriptor == "ambient pressure"

    c2.set_uncertainty(0.1, "stdev")
    assert c2.uncertainty == 0.1
    assert c2.uncertainty_type == "stdev"

    c2.set_id = None
    assert c2.set_id is None
    c2.measurement_id = None
    assert c2.measurement_id is None

    c2.data = [complex_data_node]
    assert c2.data[0] is complex_data_node
