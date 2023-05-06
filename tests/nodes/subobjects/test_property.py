import json

from util import strip_uid_from_dict

import cript


def test_json(complex_property_node, complex_property_dict):
    p = complex_property_node
    p_dict = strip_uid_from_dict(json.loads(p.json))
    assert p_dict == complex_property_dict
    p2 = cript.load_nodes_from_json(p.json)
    assert strip_uid_from_dict(json.loads(p2.json)) == strip_uid_from_dict(json.loads(p.json))


def test_setter_getter(complex_property_node, simple_material_node, simple_process_node, complex_condition_node, simple_data_node, simple_computation_node, complex_citation_node):
    p2 = complex_property_node
    p2.key = "modulus_loss"
    assert p2.key == "modulus_loss"
    p2.type = "min"
    assert p2.type == "min"
    p2.set_value(600.1, "MPa")
    assert p2.value == 600.1
    assert p2.unit == "MPa"

    p2.set_uncertainty(10.5, "var")
    assert p2.uncertainty == 10.5
    assert p2.uncertainty_type == "var"

    p2.components += [simple_material_node]
    assert p2.components[-1] is simple_material_node
    # TODO compoments_relative
    p2.components_relative += [simple_material_node]
    assert p2.components_relative[-1] is simple_material_node
    p2.structure = "structure2"
    assert p2.structure == "structure2"

    p2.method = "method2"
    assert p2.method == "method2"

    p2.sample_preparation = simple_process_node
    assert p2.sample_preparation is simple_process_node
    assert len(p2.condition) == 1
    p2.condition += [complex_condition_node]
    assert len(p2.condition) == 2
    # TODO Data
    p2.data = simple_data_node
    assert p2.data is simple_data_node
    # TODO Computations
    p2.computations += [simple_computation_node]
    assert p2.computations[-1] is simple_computation_node

    assert len(p2.citation) == 1
    p2.citation += [complex_citation_node]
    assert len(p2.citation) == 2
    p2.notes = "notes2"
    assert p2.notes == "notes2"
