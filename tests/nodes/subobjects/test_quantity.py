import json

from util import strip_uid_from_dict

import cript


def test_json(complex_quantity_node, complex_quantity_dict):
    q = complex_quantity_node
    q_dict = json.loads(q.json)
    assert strip_uid_from_dict(q_dict) == complex_quantity_dict
    q2 = cript.load_nodes_from_json(q.json)
    assert q2.json == q.json


def test_getter_setter(complex_quantity_node):
    q = complex_quantity_node
    q.value = 0.5
    assert q.value == 0.5
    q.set_uncertainty(0.1, "stderr")
    assert q.uncertainty == 0.1
    assert q.uncertainty_type == "stderr"

    q.set_key_unit("volume", "m**3")
    assert q.key == "volume"
    assert q.unit == "m**3"
