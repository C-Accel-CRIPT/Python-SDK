import copy
import json

from util import strip_uid_from_dict


def test_json(complex_equipment_node, complex_equipment_dict):
    e = complex_equipment_node
    e_dict = strip_uid_from_dict(json.loads(e.get_json(condense_to_uuid={}).json))
    assert strip_uid_from_dict(e_dict) == strip_uid_from_dict(complex_equipment_dict)
    e2 = copy.deepcopy(e)
    assert strip_uid_from_dict(json.loads(e.get_json(condense_to_uuid={}).json)) == strip_uid_from_dict(json.loads(e2.get_json(condense_to_uuid={}).json))


def test_setter_getter(complex_equipment_node, complex_condition_node, complex_file_node, complex_citation_node):
    e2 = complex_equipment_node
    e2.key = "glass_beaker"
    assert e2.key == "glass_beaker"
    e2.description = "Fancy glassware"
    assert e2.description == "Fancy glassware"

    assert len(e2.condition) == 1
    c2 = complex_condition_node
    e2.condition += [c2]
    assert e2.condition[1] == c2

    assert len(e2.file) == 0
    e2.file += [complex_file_node]
    assert e2.file[-1] is complex_file_node

    cit2 = copy.deepcopy(complex_citation_node)
    assert len(e2.citation) == 1
    e2.citation += [cit2]
    assert e2.citation[1] == cit2
