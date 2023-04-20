import copy
import json

from util import strip_uid_from_dict

import cript


def test_json(simple_software_configuration_node, simple_software_configuration_dict):
    sc = simple_software_configuration_node
    sc_dict = strip_uid_from_dict(json.loads(sc.json))
    assert sc_dict == simple_software_configuration_dict
    sc2 = cript.load_nodes_from_json(sc.json)
    assert strip_uid_from_dict(json.loads(sc2.json)) == strip_uid_from_dict(json.loads(sc.json))


def test_setter_getter(simple_software_configuration_node, simple_algorithm_node, simple_citation_node):
    sc2 = simple_software_configuration_node
    software2 = copy.deepcopy(sc2.software)
    sc2.software = software2
    assert sc2.software is software2

    assert len(sc2.algorithms) == 1
    al2 = simple_algorithm_node
    sc2.algorithms += [al2]
    assert sc2.algorithms[1] is al2

    sc2.notes = "my new fancy notes"
    assert sc2.notes == "my new fancy notes"

    cit2 = simple_citation_node
    assert len(sc2.citation) == 1
    sc2.citation += [cit2]
    assert sc2.citation[1] == cit2
