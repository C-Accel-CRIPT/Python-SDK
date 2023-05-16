import copy
import json
from dataclasses import replace

import pytest
from util import strip_uid_from_dict

import cript
from cript.nodes.core import get_new_uid
from cript.nodes.exceptions import (
    CRIPTJsonNodeError,
    CRIPTJsonSerializationError,
    CRIPTNodeSchemaError,
    CRIPTOrphanedComputationalProcessError,
    CRIPTOrphanedComputationError,
    CRIPTOrphanedDataError,
    CRIPTOrphanedMaterialError,
    CRIPTOrphanedProcessError,
)


def test_removing_nodes(complex_algorithm_node, complex_parameter_node, complex_algorithm_dict):
    a = complex_algorithm_node
    p = complex_parameter_node
    a.parameter += [p]
    assert strip_uid_from_dict(json.loads(a.json)) != complex_algorithm_dict
    a.remove_child(p)
    assert strip_uid_from_dict(json.loads(a.json)) == complex_algorithm_dict


def test_json_error(complex_parameter_node):
    parameter = complex_parameter_node
    # Let's break the node by violating the data model
    parameter._json_attrs = replace(parameter._json_attrs, value="abc")
    with pytest.raises(CRIPTNodeSchemaError):
        parameter.validate()
    # Let's break it completely
    parameter._json_attrs = None
    with pytest.raises(CRIPTJsonSerializationError):
        parameter.json


def test_local_search(complex_algorithm_node, complex_parameter_node):
    a = complex_algorithm_node
    # Check if we can use search to find the algoritm node, but specifying node and key
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc_barostat"})
    assert find_algorithms == [a]
    # Check if it corretcly exclude the algorithm if key is specified to non-existent value
    find_algorithms = a.find_children({"node": "Algorithm", "key": "mc"})
    assert find_algorithms == []

    # Adding 2 separate parameters to test deeper search
    p1 = complex_parameter_node
    p2 = copy.deepcopy(complex_parameter_node)
    p2.key = "damping_time"
    p2.value = 15.0
    p2.unit = "m"
    a.parameter += [p1, p2]

    # Test if we can find a specific one of the parameters
    find_parameter = a.find_children({"key": "damping_time"})
    assert find_parameter == [p2]

    # Test to find the other parameter
    find_parameter = a.find_children({"key": "update_frequency"})
    assert find_parameter == [p1]

    # Test if correctly find no paramter if we are searching for a non-existent parameter
    find_parameter = a.find_children({"key": "update"})
    assert find_parameter == []

    # Test nested search. Here we are looking for any node that has a child node parameter as specified.
    find_algorithms = a.find_children({"parameter": {"key": "damping_time"}})
    assert find_algorithms == [a]
    # Same as before, but specifiying two children that have to be present (AND condition)
    find_algorithms = a.find_children({"parameter": [{"key": "damping_time"}, {"key": "update_frequency"}]})
    assert find_algorithms == [a]

    # Test that the main node is correctly excluded if we specify an additionally non-existent paramter
    find_algorithms = a.find_children({"parameter": [{"key": "damping_time"}, {"key": "update_frequency"}, {"foo": "bar"}]})
    assert find_algorithms == []


def test_cycles(complex_data_node, simple_computation_node):
    # We create a wrong cycle with parameters here.
    # TODO replace this with nodes that actually can form a cycle
    d = copy.deepcopy(complex_data_node)
    c = copy.deepcopy(simple_computation_node)
    d.computation += [c]
    # Using input and output data guarantees a cycle here.
    c.output_data += [d]
    c.input_data += [d]

    # Generate json with an implicit cycle
    c.get_json()
    d.get_json()


def test_uid_serial(simple_inventory_node):
    simple_inventory_node.material += simple_inventory_node.material
    json_dict = json.loads(simple_inventory_node.get_json(condense_to_uuid={}).json)
    assert len(json_dict["material"]) == 4
    assert isinstance(json_dict["material"][2]["uid"], str)
    assert json_dict["material"][2]["uid"].startswith("_:")
    assert len(json_dict["material"][2]["uid"]) == len(get_new_uid())
    assert isinstance(json_dict["material"][3]["uid"], str)
    assert json_dict["material"][3]["uid"].startswith("_:")
    assert len(json_dict["material"][3]["uid"]) == len(get_new_uid())
    assert json_dict["material"][3]["uid"] != json_dict["material"][2]["uid"]


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


def test_invalid_project_graphs(simple_project_node, simple_material_node, simple_process_node, simple_property_node, simple_data_node, simple_computation_node, simple_computation_process_node):
    project = copy.deepcopy(simple_project_node)
    process = copy.deepcopy(simple_process_node)
    material = copy.deepcopy(simple_material_node)

    ingredient = cript.Ingredient(material=material, quantity=[cript.Quantity(key="mass", value=1.23, unit="kg")])
    process.ingredient += [ingredient]

    # Add the process to the experiment, but not in inventory or materials
    # Invalid graph
    project.collection[0].experiment[0].process += [process]
    with pytest.raises(CRIPTOrphanedMaterialError):
        project.validate()

    # First fix add material to inventory
    project.collection[0].inventory += [cript.Inventory("test_inventory", material=[material])]
    project.validate()
    # Reverse this fix
    project.collection[0].inventory = []
    with pytest.raises(CRIPTOrphanedMaterialError):
        project.validate()

    # Fix by add to the materials list instead.
    # Using the util helper function for this.
    cript.add_orphaned_nodes_to_project(project, active_experiment=None, max_iteration=10)
    project.validate()

    # Now add an orphan process to the graph
    process2 = copy.deepcopy(simple_process_node)
    process.prerequisite_process += [process2]
    with pytest.raises(CRIPTOrphanedProcessError):
        project.validate()

    # Wrong fix it helper node
    dummy_experiment = copy.deepcopy(project.collection[0].experiment[0])
    with pytest.raises(RuntimeError):
        cript.add_orphaned_nodes_to_project(project, dummy_experiment)
    # Problem still presists
    with pytest.raises(CRIPTOrphanedProcessError):
        project.validate()
    # Fix by using the helper function correctly
    cript.add_orphaned_nodes_to_project(project, project.collection[0].experiment[0], 10)
    project.validate()

    # We add property to the material, because that adds the opportunity for orphaned data and computation
    property = copy.deepcopy(simple_property_node)
    material.property += [property]
    project.validate()
    # Now add an orphan data
    data = copy.deepcopy(simple_data_node)
    property.data = [data]
    with pytest.raises(CRIPTOrphanedDataError):
        project.validate()
    # Fix with the helper function
    cript.add_orphaned_nodes_to_project(project, project.collection[0].experiment[0], 10)
    project.validate()

    # Add an orphan Computation
    computation = copy.deepcopy(simple_computation_node)
    property.computation += [computation]
    with pytest.raises(CRIPTOrphanedComputationError):
        project.validate()
    # Fix with the helper function
    cript.add_orphaned_nodes_to_project(project, project.collection[0].experiment[0], 10)
    project.validate()

    # Add orphan computational process
    comp_proc = copy.deepcopy(simple_computation_process_node)
    data.computation_process += [comp_proc]
    with pytest.raises(CRIPTOrphanedComputationalProcessError):
        while True:
            try:  # Do trigger not orphan materials
                project.validate()
            except CRIPTOrphanedMaterialError as exc:
                project._json_attrs.material.append(exc.orphaned_node)
            else:
                break

    cript.add_orphaned_nodes_to_project(project, project.collection[0].experiment[0], 10)
    project.validate()
