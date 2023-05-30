import copy
import json

from util import strip_uid_from_dict

import cript


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
    citation = copy.deepcopy(complex_citation_node)
    simple_experiment_node.citation = [citation]

    # assert getters and setters are equal
    assert isinstance(simple_experiment_node, cript.Experiment)
    assert simple_experiment_node.name == experiment_name
    assert simple_experiment_node.process == [simple_process_node]
    assert simple_experiment_node.computation == [simple_computation_node]
    assert simple_experiment_node.computation_process == [simple_computational_process_node]
    assert simple_experiment_node.data == [simple_data_node]
    assert simple_experiment_node.funding == experiment_funders
    assert simple_experiment_node.citation[-1] == citation


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
        "process": [{"node": ["Process"], "name": "my process name", "type": "affinity_pure", "keyword": []}],
        "computation": [{"node": ["Computation"], "name": "my computation name", "type": "analysis", "citation": []}],
        "computation_process": [
            {
                "node": ["ComputationProcess"],
                "name": "my computational process node name",
                "type": "cross_linking",
                "input_data": [{"node": ["Data"], "name": "my data name", "type": "afm_amp", "file": [{"node": ["File"], "source": "https://criptapp.org", "type": "calibration", "extension": ".csv", "data_dictionary": "my file's data dictionary"}]}],
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
        "data": [{"node": ["Data"]}],
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
def test_save_experiment() -> None:
    """
    integration test

    test that an experiment node can be saved correctly in the API
    indirectly tests that the experiment can be correctly converted from JSON to the node
    indirectly tests that an experiment node can be gotten correctly from the API

    1. create an experiment node with all possible attributes
    2. save the experiment to the API
    3. get the node from the API
    4. convert the node to the experiment class
    5. assert that the experiment node from API and local are equal to each other
    """
    pass


def test_get_experiment_from_api() -> None:
    """
    tests that experiments can be gotten correctly from the API

    Notes
    -----
    indirectly tests that the experiment was saved correctly to the API from the previous test
    """
    pass


def test_convert_api_experiment_json_to_node() -> None:
    """
    tests that it can correctly convert an experiment node from the API to a python Experiment node
    """
    pass


def test_update_experiment() -> None:
    """
    integration test: test that an experiment can be correctly updated in the API
    """
    pass


def test_delete_experiment() -> None:
    """
    integration test: test to see an experiment can be correctly deleted from the API
    """
    pass
