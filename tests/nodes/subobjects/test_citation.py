import json

from util import strip_uid_from_dict

import cript


def test_json(simple_citation_node, simple_citation_dict):
    c = simple_citation_node
    c_dict = strip_uid_from_dict(json.loads(c.json))
    assert c_dict == simple_citation_dict
    c2 = cript.load_nodes_from_json(c.json)
    c2_dict = strip_uid_from_dict(json.loads(c2.json))
    assert c_dict == c2_dict


def test_setter_getter(simple_citation_node, simple_reference_node):
    c = simple_citation_node
    c.type = "replicated"
    assert c.type == "replicated"
    new_ref = simple_reference_node
    new_ref.title = "foo bar"
    c.reference = new_ref
    assert c.reference == new_ref
