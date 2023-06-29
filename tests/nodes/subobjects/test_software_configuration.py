import copy
import json
import uuid

from util import strip_uid_from_dict

import cript
from tests.test_integration import integrate_nodes_helper


def test_json(complex_software_configuration_node, complex_software_configuration_dict):
    sc = complex_software_configuration_node
    sc_dict = strip_uid_from_dict(json.loads(sc.json))
    assert sc_dict == complex_software_configuration_dict
    sc2 = cript.load_nodes_from_json(sc.json)
    assert strip_uid_from_dict(json.loads(sc2.json)) == strip_uid_from_dict(json.loads(sc.json))


def test_setter_getter(complex_software_configuration_node, complex_algorithm_node, complex_citation_node):
    sc2 = complex_software_configuration_node
    software2 = copy.deepcopy(sc2.software)
    sc2.software = software2
    assert sc2.software is software2

    # assert len(sc2.algorithm) == 1
    # al2 = complex_algorithm_node
    # print(sc2.get_json(indent=2,sortkeys=False).json)
    # print(al2.get_json(indent=2,sortkeys=False).json)
    # sc2.algorithm += [al2]
    # assert sc2.algorithm[1] is al2

    sc2.notes = "my new fancy notes"
    assert sc2.notes == "my new fancy notes"

    # cit2 = complex_citation_node
    # assert len(sc2.citation) == 1
    # sc2.citation += [cit2]
    # assert sc2.citation[1] == cit2


def test_integration_software_configuration(cript_api, simple_project_node, simple_collection_node, simple_experiment_node, simple_computation_node, simple_software_configuration):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert JSON sent and JSON received are the same
    """
    simple_project_node.name = f"test_integration_software_configuration_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]

    simple_project_node.collection[0].experiment = [simple_experiment_node]

    simple_project_node.collection[0].experiment[0].computation = [simple_computation_node]

    simple_project_node.collection[0].experiment[0].computation[0].software_configuration = [simple_software_configuration]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

