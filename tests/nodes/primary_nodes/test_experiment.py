import cript
import pytest


def test_create_experiment_slim() -> None:
    """
    test just to see if a collection can be made without any issues
    with just a collection name and nothing else

    Returns
    -------
    None
    """
    pass


def test_create_experiment_full() -> None:
    """
    test to see if Collection can be made with all the possible options filled

    Returns
    -------
    None
    """
    pass


def test_all_getters_and_setters_for_experiment() -> None:
    """
    tests all the getters and setters for the experiment

    1. create a node with only the required arguments
    2. set all the properties for the experiment
    3. get all the properties for the experiment
    4. assert that what you set in the setter and the getter are equal to each other

    Returns
    -------
    None
    """


def test_experiment_json() -> None:
    """
    tests that the experiment JSON is functioning correctly

    1. create an experiment with all possible attributes
    2. convert the experiment into a JSON
    3. assert that the JSON is that it produces is equal to what you expected

    Returns
    -------
    None
    """
    pass


def convert_json_to_experiment() -> None:
    """
    test that a JSON can be successfully converted to an experiment

    1. create an experiment json with all possible attributes
    2. convert the json into an experiment node
    3. assert that the experiment node that is produced is equal to the experiment node you expected


    Returns
    -------
    None
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

    Returns
    -------
    None
    """
    pass


def test_update_experiment() -> None:
    """
    integration test

    test that an experiment can be correctly updated in the API

    Returns
    -------
    None
    """
    pass


def test_delete_experiment() -> None:
    """
    integration test

    test to see an experiment can be correctly deleted from the API
    Returns
    -------
    None
    """
    pass
