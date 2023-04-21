import json

from util import strip_uid_from_dict

import cript


def test_json(complex_software_node, complex_software_dict):
    s = complex_software_node
    s_dict = strip_uid_from_dict(json.loads(s.json))
    assert s_dict == complex_software_dict
    s2 = cript.load_nodes_from_json(s.json)
    assert s2.json == s.json


def test_setter_getter(complex_software_node):
    s2 = complex_software_node
    s2.name = "PySAGES"
    assert s2.name == "PySAGES"
    s2.version = "v0.3.0"
    assert s2.version == "v0.3.0"
    s2.source = "https://github.com/SSAGESLabs/PySAGES"
    assert s2.source == "https://github.com/SSAGESLabs/PySAGES"
