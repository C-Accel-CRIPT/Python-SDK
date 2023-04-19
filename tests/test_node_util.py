import json
from dataclasses import replace

import pytest
from test_nodes_no_host import get_algorithm, get_algorithm_string, get_parameter

import cript
from cript.nodes.exceptions import (
    CRIPTJsonDeserializationError,
    CRIPTJsonSerializationError,
    CRIPTNodeCycleError,
)
from cript.nodes.util import get_new_uid

# def test_removing_nodes():
#     a = get_algorithm()
#     p = get_parameter()
#     a.parameter += [p]
#     a.remove_child(p)
#     assert a.json == get_algorithm_string()


# def test_json_error():
#     faulty_json = "{'node': 'Parameter', 'foo': 'bar'}".replace("'", '"')
#     with pytest.raises(CRIPTJsonDeserializationError):
#         cript.load_nodes_from_json(faulty_json)

#     parameter = get_parameter()
#     # Let's break the node by violating the data model
#     parameter._json_attrs = replace(parameter._json_attrs, value=None)
#     with pytest.raises(CRIPTJsonSerializationError):
#         parameter.json
#     # Let's break it completely
#     parameter._json_attrs = None
#     with pytest.raises(CRIPTJsonSerializationError):
#         parameter.json


def test_local_search():
    a = get_algorithm()

    # Check if we can use search to find the algoritm node, but specifying node and key
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc_barostat"})
    assert find_algorithms == [a]
    # Check if it corretcly exclude the algorithm if key is specified to non-existent value
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc"})
    assert find_algorithms == []

    # Adding 2 separate parameters to test deeper search
    p1 = get_parameter()
    p2 = get_parameter()
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


def test_cycles():
    # We create a wrong cycle with parameters here.
    # TODO replace this with nodes that actually can form a cycle
    p1 = get_parameter()
    p1.unit = "1"
    p2 = get_parameter()
    p2.unit = "2"
    p3 = get_parameter()
    p3.unit = "3"

    p1.key = p2
    p2.key = p3

    with pytest.raises(CRIPTNodeCycleError):
        p3.key = p1


def test_uid_serial(simple_inventory_node):
    simple_inventory_node.materials += simple_inventory_node.materials
    json_dict = json.loads(simple_inventory_node.get_json())
    assert len(json_dict["materials"]) == 4
    assert isinstance(json_dict["materials"][2], str)
    assert json_dict["materials"][2].startswith("_")
    assert len(json_dict["materials"][2]) == len(get_new_uid())
    assert isinstance(json_dict["materials"][3], str)
    assert json_dict["materials"][3].startswith("_")
    assert len(json_dict["materials"][3]) == len(get_new_uid())
