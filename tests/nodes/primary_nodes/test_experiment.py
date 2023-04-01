import pytest

import cript


def test_create_simple_experiment(
    simple_process_node, simple_computation_node, simple_computational_process_node, simple_data_node, simple_citation_node
) -> None:
    """
    test just to see if a minimal experiment can be made without any issues
    """
    experiment_name = "my experiment name"

    my_experiment = cript.Experiment(name=experiment_name)

    # assertions
    assert isinstance(my_experiment, cript.Experiment)


def test_create_complex_experiment(
    simple_process_node, simple_computation_node, simple_computational_process_node, simple_data_node, simple_citation_node
) -> None:
    """
    test to see if Collection can be made with all the possible options filled
    """
    experiment_name = "my experiment name"
    experiment_funders = ["National Science Foundation", "IRIS", "NIST"]

    my_experiment = cript.Experiment(
        name=experiment_name,
        process=[simple_process_node],
        computation=[simple_computation_node],
        computational_process=[simple_computational_process_node],
        data=[simple_data_node],
        funding=experiment_funders,
        citation=[simple_citation_node],
    )

    # assertions
    assert isinstance(my_experiment, cript.Experiment)
    assert my_experiment.name == experiment_name
    assert my_experiment.process == [simple_process_node]
    assert my_experiment.computation == [simple_computation_node]
    assert my_experiment.computational_process == [simple_computational_process_node]
    assert my_experiment.data == [simple_data_node]
    assert my_experiment.funding == experiment_funders
    assert my_experiment.citation == [simple_citation_node]


def test_all_getters_and_setters_for_experiment(
    simple_experiment_node,
    simple_process_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_data_node,
    simple_citation_node,
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
    simple_experiment_node.computational_process = [simple_computational_process_node]
    simple_experiment_node.data = [simple_data_node]
    simple_experiment_node.funding = experiment_funders
    simple_experiment_node.citation = [simple_citation_node]

    # assert getters and setters are equal
    assert isinstance(simple_experiment_node, cript.Experiment)
    assert simple_experiment_node.name == experiment_name
    assert simple_experiment_node.process == [simple_process_node]
    assert simple_experiment_node.computation == [simple_computation_node]
    assert simple_experiment_node.computational_process == [simple_computational_process_node]
    assert simple_experiment_node.data == [simple_data_node]
    assert simple_experiment_node.funding == experiment_funders
    assert simple_experiment_node.citation == [simple_citation_node]


def test_experiment_json() -> None:
    """
    tests that the experiment JSON is functioning correctly

    1. create an experiment with all possible attributes
    2. convert the experiment into a JSON
    3. assert that the JSON is that it produces is equal to what you expected
    """
    pass


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
