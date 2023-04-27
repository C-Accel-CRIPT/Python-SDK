import json

from util import strip_uid_from_dict

import cript


def test_json(complex_equipment_node, complex_equipment_dict):
    e = complex_equipment_node
    e_dict = strip_uid_from_dict(json.loads(e.json))
    assert strip_uid_from_dict(e_dict) == strip_uid_from_dict(complex_equipment_dict)
    e2 = cript.load_nodes_from_json(e.json)
    assert strip_uid_from_dict(json.loads(e.json)) == strip_uid_from_dict(json.loads(e2.json))


def test_settter_getter(complex_equipment_node, complex_condition_node, complex_file_node, complex_citation_node):
    e2 = complex_equipment_node
    e2.key = "glassware"
    assert e2.key == "glassware"
    e2.description = "Fancy glassware"
    assert e2.description == "Fancy glassware"

    assert len(e2.conditions) == 1
    c2 = complex_condition_node
    e2.conditions += [c2]
    assert e2.conditions[1] == c2

    assert len(e2.files) == 0
    e2.files += [complex_file_node]
    assert e2.files[-1] is complex_file_node

    cit2 = complex_citation_node
    assert len(e2.citations) == 1
    e2.citations += [cit2]
    assert e2.citations[1] == cit2
