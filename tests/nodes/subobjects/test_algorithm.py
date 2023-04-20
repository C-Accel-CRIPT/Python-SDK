import json

from util import strip_uid_from_dict

import cript


def test_setter_getter(simple_algorithm_node, simple_citation_node):
    a = simple_algorithm_node
    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"
    a.citation += [simple_citation_node]
    assert a.citation[0].json == simple_citation_node.json


def test_json(simple_algorithm_node, simple_algorithm_dict, simple_citation_node):
    a = simple_algorithm_node
    a_dict = json.loads(a.json)
    assert strip_uid_from_dict(a_dict) == simple_algorithm_dict
    a2 = cript.load_nodes_from_json(a.json)
    assert strip_uid_from_dict(json.loads(a2.json)) == strip_uid_from_dict(a_dict)
