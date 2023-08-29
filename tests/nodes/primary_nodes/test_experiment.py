import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

import cript
from tests.integration_test_helper import delete_integration_node_helper


def test_create_simple_experiment() -> None:
    """
    test just to see if a minimal experiment can be made without any issues
    """
    experiment_name = "my experiment name"

    my_experiment = cript.Experiment(name=experiment_name)

    # assertions
    assert isinstance(my_experiment, cript.Experiment)


def test_create_complex_experiment(simple_process_node, simple_computation_node, simple_computational_process_node, simple_data_node, complex_citation_node) -> None:
    """
    test to see if Collection can be made with all the possible options filled
    """
    experiment_name = "my experiment name"
    experiment_funders = ["National Science Foundation", "IRIS", "NIST"]

    citation = copy.deepcopy(complex_citation_node)
    my_experiment = cript.Experiment(
        name=experiment_name,
        process=[simple_process_node],
        computation=[simple_computation_node],
        computation_process=[simple_computational_process_node],
        data=[simple_data_node],
        funding=experiment_funders,
        citation=[citation],
    )

    # assertions
    assert isinstance(my_experiment, cript.Experiment)
    assert my_experiment.name == experiment_name
    assert my_experiment.process == [simple_process_node]
    assert my_experiment.computation == [simple_computation_node]
    assert my_experiment.computation_process == [simple_computational_process_node]
    assert my_experiment.data == [simple_data_node]
    assert my_experiment.funding == experiment_funders
    assert my_experiment.citation[-1] == citation


def test_all_getters_and_setters_for_experiment(
    simple_experiment_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_data_node,
    complex_citation_node,
) -> None:
    """
    tests all the getters and setters for the experiment

    1. create a node with only the required arguments
    2. set all the properties for the experiment
    3. get all the properties for the experiment
    4. assert that what you set in the setter and the getter are equal to each other
    """
    experiment_name = "my new experiment name"
    experiment_funders = ["MIT", "European Research Council (ERC)", "Japan Society for the Promotion of Science (JSPS)"]

    # set experiment properties
    simple_experiment_node.name = experiment_name
    simple_experiment_node.process = [simple_process_node]
    simple_experiment_node.computation = [simple_computation_node]
    simple_experiment_node.computation_process = [simple_computational_process_node]
    simple_experiment_node.data = [simple_data_node]
    simple_experiment_node.funding = experiment_funders
    simple_experiment_node.citation = [complex_citation_node]

    # assert getters and setters are equal
    assert isinstance(simple_experiment_node, cript.Experiment)
    assert simple_experiment_node.name == experiment_name
    assert simple_experiment_node.process == [simple_process_node]
    assert simple_experiment_node.computation == [simple_computation_node]
    assert simple_experiment_node.computation_process == [simple_computational_process_node]
    assert simple_experiment_node.data == [simple_data_node]
    assert simple_experiment_node.funding == experiment_funders
    assert simple_experiment_node.citation[-1] == complex_citation_node

    # test experiment attributes can be removed
    simple_experiment_node.process = []
    simple_experiment_node.computation = []
    simple_experiment_node.computation_process = []
    simple_experiment_node.data = []
    simple_experiment_node.funding = []
    simple_experiment_node.citation = []

    # assert that optional attributes can be removed
    assert simple_experiment_node.process == []
    assert simple_experiment_node.computation == []
    assert simple_experiment_node.computation_process == []
    assert simple_experiment_node.data == []
    assert simple_experiment_node.funding == []
    assert simple_experiment_node.citation == []


def test_experiment_json(simple_process_node, simple_computation_node, simple_computational_process_node, simple_data_node, complex_citation_node, complex_citation_dict) -> None:
    """
    tests that the experiment JSON is functioning correctly

    1. create an experiment with all possible attributes
    2. convert the experiment into a JSON
    3. assert that the JSON is that it produces is equal to what you expected

    Notes
    -----
    indirectly tests that the notes attribute also works within the experiment node.
    All nodes inherit from the base node, so if the base node attribute is working in this test
    there is a good chance that it will work correctly for all other nodes that inherit from it as well
    """
    experiment_name = "my experiment name"
    experiment_funders = ["National Science Foundation", "IRIS", "NIST"]

    citation = copy.deepcopy(complex_citation_node)
    my_experiment = cript.Experiment(
        name=experiment_name,
        process=[simple_process_node],
        computation=[simple_computation_node],
        computation_process=[simple_computational_process_node],
        data=[simple_data_node],
        funding=experiment_funders,
        citation=[citation],
    )

    # adding notes to test base node attributes
    my_experiment.notes = "these are all of my notes for this experiment"

    # TODO this is unmaintainable and we should figure out a strategy for a better way
    expected_experiment_dict = {
        "node": ["Experiment"],
        "name": "my experiment name",
        "notes": "these are all of my notes for this experiment",
        "process": [{"node": ["Process"], "name": "my process name", "type": "affinity_pure"}],
        "computation": [{"node": ["Computation"], "name": "my computation name", "type": "analysis"}],
        "computation_process": [
            {
                "node": ["ComputationProcess"],
                "name": "my computational process node name",
                "type": "cross_linking",
                "input_data": [
                    {
                        "node": ["Data"],
                        "name": "my data name",
                        "type": "afm_amp",
                        "file": [{"node": ["File"], "name": "my complex file node fixture", "source": "https://criptapp.org", "type": "calibration", "extension": ".csv", "data_dictionary": "my file's data dictionary"}],
                    }
                ],
                "ingredient": [
                    {
                        "node": ["Ingredient"],
                        "material": {},
                        "quantity": [{"node": ["Quantity"], "key": "mass", "value": 11.2, "unit": "kg", "uncertainty": 0.2, "uncertainty_type": "stdev"}],
                        "keyword": ["catalyst"],
                    }
                ],
            }
        ],
        "data": [{}],
        "funding": ["National Science Foundation", "IRIS", "NIST"],
        "citation": [
            {
                "node": ["Citation"],
                "type": "reference",
                "reference": {
                    "node": ["Reference"],
                    "type": "journal_article",
                    "title": "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: SOft coarse grained Monte-Carlo Acceleration (SOMA)",
                    "author": ["Ludwig Schneider", "Marcus M\u00fcller"],
                    "journal": "Computer Physics Communications",
                    "publisher": "Elsevier",
                    "year": 2019,
                    "pages": [463, 476],
                    "doi": "10.1016/j.cpc.2018.08.011",
                    "issn": "0010-4655",
                    "website": "https://www.sciencedirect.com/science/article/pii/S0010465518303072",
                },
            }
        ],
    }

    ref_dict = json.loads(my_experiment.json)
    ref_dict = strip_uid_from_dict(ref_dict)

    assert len(ref_dict) == len(expected_experiment_dict)
    assert ref_dict == expected_experiment_dict


# -------- Integration Tests --------
def test_integration_experiment(cript_api, simple_project_node, simple_collection_node, simple_experiment_node):
    """
    integration test between Python SDK and API Client

    tests both POST and GET

    1. create a project
    1. create a collection
    1. add collection to project
    1. save the project
    1. get the project
    1. deserialize the project to node
    1. convert the new node to JSON
    1. compare the project node JSON that was sent to API and the node the API gave, have the same JSON

    Notes
    -----
    comparing JSON because it is easier to compare than an object
    """
    # ========= test create =========
    # rename project and collection to not bump into duplicate issues
    simple_project_node.name = f"test_integration_experiment_project_name_{uuid.uuid4().hex}"
    simple_project_node.collection = [simple_collection_node]
    simple_project_node.collection[0].experiment = [simple_experiment_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update simple attribute to trigger update
    simple_project_node.collection[0].experiment[0].funding = ["update1", "update2", "update3"]
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_experiment_node)
