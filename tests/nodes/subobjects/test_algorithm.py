import json

from util import strip_uid_from_dict

import cript


def test_setter_getter(complex_algorithm_node, complex_citation_node):
    a = complex_algorithm_node
    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"
    a.citation += [complex_citation_node]
    assert strip_uid_from_dict(json.loads(a.citation[0].json)) == strip_uid_from_dict(json.loads(complex_citation_node.json))


def test_json(complex_algorithm_node, complex_algorithm_dict, complex_citation_node):
    a = complex_algorithm_node
    a_dict = json.loads(a.json)
    assert strip_uid_from_dict(a_dict) == complex_algorithm_dict
    print(a.get_json(indent=2).json)
    a2 = cript.load_nodes_from_json(a.json)
    assert strip_uid_from_dict(json.loads(a2.json)) == strip_uid_from_dict(a_dict)
