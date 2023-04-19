def test_creation(simple_algorithm_node):
    a = simple_algorithm_node


def test_setter_getter(simple_algorithm_node):
    a = simple_algorithm_node
    a.key = "berendsen"
    assert a.key == "berendsen"
    a.type = "integration"
    assert a.type == "integration"
    a.citation += [get_citation()]

    assert a.citation[0].json == get_citation().json
    a_str = a.json
    assert a_str == get_algorithm_string()
    a.parameter += [get_parameter()]
    a_str = get_algorithm_string()
    a_str2 = json.dumps(json.loads(a_str.replace("}", f', "parameter": [{get_parameter_string()}]' + "}")), sort_keys=True)
    assert a_str2 == a.json

    a2 = cript.load_nodes_from_json(a_str2)
    assert a_str2 == a2.json
