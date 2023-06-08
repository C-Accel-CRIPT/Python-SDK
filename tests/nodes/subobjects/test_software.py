import copy
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


def test_uuid(complex_software_node):
    s = complex_software_node

    # Deep copies should not share uuid (or uids) or urls
    s2 = copy.deepcopy(complex_software_node)
    assert s.uuid != s2.uuid
    assert s.uid != s2.uid
    assert s.url != s2.url

    # Loads from json have the same uuid and url
    s3 = cript.load_nodes_from_json(s.json)
    assert s3.uuid == s.uuid
    assert s3.url == s.url
