import copy
import json
from dataclasses import replace

import pytest
from util import strip_uid_from_dict

from cript.nodes.core import get_new_uid
from cript.nodes.exceptions import CRIPTJsonSerializationError, CRIPTJsonNodeError


def test_removing_nodes(simple_algorithm_node, simple_parameter_node, simple_algorithm_dict):
    a = simple_algorithm_node
    p = simple_parameter_node
    a.parameter += [p]
    assert strip_uid_from_dict(json.loads(a.json)) != simple_algorithm_dict
    a.remove_child(p)
    assert strip_uid_from_dict(json.loads(a.json)) == simple_algorithm_dict


def test_json_error(simple_parameter_node):
    parameter = simple_parameter_node
    # Let's break the node by violating the data model
    parameter._json_attrs = replace(parameter._json_attrs, value=None)
    with pytest.raises(CRIPTJsonSerializationError):
        parameter.json
    # Let's break it completely
    parameter._json_attrs = None
    with pytest.raises(CRIPTJsonSerializationError):
        parameter.json


def test_local_search(simple_algorithm_node, simple_parameter_node):
    a = simple_algorithm_node
    # Check if we can use search to find the algoritm node, but specifying node and key
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc_barostat"})
    assert find_algorithms == [a]
    # Check if it corretcly exclude the algorithm if key is specified to non-existent value
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc"})
    assert find_algorithms == []

    # Adding 2 separate parameters to test deeper search
    p1 = simple_parameter_node
    p2 = copy.deepcopy(simple_parameter_node)
    p2.key = "advanced_sampling"
    p2.value = 15.0
    p2.unit = "m"
    a.parameter += [p1, p2]

    # Test if we can find a specific one of the parameters
    find_parameter = a.find_children({"key": "advanced_sampling"})
    assert find_parameter == [p2]

    # Test to find the other parameter
    find_parameter = a.find_children({"key": "update_frequency"})
    assert find_parameter == [p1]

    # Test if correctly find no paramter if we are searching for a non-existent parameter
    find_parameter = a.find_children({"key": "update"})
    assert find_parameter == []

    # Test nested search. Here we are looking for any node that has a child node parameter as specified.
    find_algorithms = a.find_children({"parameter": {"key": "advanced_sampling"}})
    assert find_algorithms == [a]
    # Same as before, but specifiying two children that have to be present (AND condition)
    find_algorithms = a.find_children({"parameter": [{"key": "advanced_sampling"}, {"key": "update_frequency"}]})
    assert find_algorithms == [a]

    # Test that the main node is correctly excluded if we specify an additionally non-existent paramter
    find_algorithms = a.find_children({"parameter": [{"key": "advanced_sampling"}, {"key": "update_frequency"}, {"foo": "bar"}]})
    assert find_algorithms == []


def test_cycles(simple_parameter_node):
    # We create a wrong cycle with parameters here.
    # TODO replace this with nodes that actually can form a cycle
    p1 = copy.deepcopy(simple_parameter_node)
    p1.unit = "1"
    p2 = copy.deepcopy(simple_parameter_node)
    p2.unit = "2"
    p3 = copy.deepcopy(simple_parameter_node)
    p3.unit = "3"

    p1.key = p2
    p2.key = p3
    p3.key = p1

    p1.get_json()


def test_uid_serial(simple_inventory_node):
    simple_inventory_node.materials += simple_inventory_node.materials
    json_dict = json.loads(simple_inventory_node.get_json().json)
    assert len(json_dict["materials"]) == 4
    assert isinstance(json_dict["materials"][2]["uid"], str)
    assert json_dict["materials"][2]["uid"].startswith("_:")
    assert len(json_dict["materials"][2]["uid"]) == len(get_new_uid())
    assert isinstance(json_dict["materials"][3]["uid"], str)
    assert json_dict["materials"][3]["uid"].startswith("_:")
    assert len(json_dict["materials"][3]["uid"]) == len(get_new_uid())
    assert json_dict["materials"][3]["uid"] != json_dict["materials"][2]["uid"]


def test_invalid_json_load():
    def raise_node_dict(node_dict):
        node_str = json.dumps(node_dict)
        with pytest.raises(CRIPTJsonNodeError):
            cript.load_nodes_from_json(node_str)

    node_dict = {"node": "Computation"}
    raise_node_dict(node_dict)
    node_dict = {"node": []}
    raise_node_dict(node_dict)
    node_dict = {"node": ["asdf", "asdf"]}
    raise_node_dict(node_dict)
    node_dict = {"node": [None]}
    raise_node_dict(node_dict)
