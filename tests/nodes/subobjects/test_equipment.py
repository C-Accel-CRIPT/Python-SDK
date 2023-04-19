import json

from util import strip_uid_from_dict

import cript


def test_json(simple_equipment_node, simple_equipment_dict):
    e = simple_equipment_node
    e_dict = strip_uid_from_dict(json.loads(e.json))
    assert e_dict == strip_uid_from_dict(simple_equipment_dict)
    e2 = cript.load_nodes_from_json(e.json)
    assert e.json == e2.json


def test_settter_getter(simple_equipment_node, simple_condition_node, simple_file_node, simple_citation_node):
    e2 = simple_equipment_node
    e2.key = "glassware"
    assert e2.key == "glassware"
    e2.description = "Fancy glassware"
    assert e2.description == "Fancy glassware"

    assert len(e2.conditions) == 1
    c2 = simple_condition_node
    e2.conditions += [c2]
    assert e2.conditions[1] == c2

    assert len(e2.files) == 1
    e2.files += [simple_file_node]
    assert e2.files[-1] is simple_file_node

    cit2 = simple_citation_node
    assert len(e2.citations) == 1
    e2.citations += [cit2]
    assert e2.citations[1] == cit2
