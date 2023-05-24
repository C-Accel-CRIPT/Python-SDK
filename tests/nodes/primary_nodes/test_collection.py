import copy
import json

from util import strip_uid_from_dict

import cript


def test_create_simple_collection(simple_experiment_node) -> None:
    """
    test to see a simple collection node can be created with only required arguments

    Notes
    -----
    * [Collection](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=8)
    has no required attributes.
    * The Python SDK only requires Collections to have `name`
        * Since it doesn't make sense to have an empty Collection I added an Experiment to the Collection as well
    """
    my_collection_name = "my collection name"

    my_collection = cript.Collection(name=my_collection_name, experiment=[simple_experiment_node])

    # assertions
    assert isinstance(my_collection, cript.Collection)
    assert my_collection.name == my_collection_name
    assert my_collection.experiment == [simple_experiment_node]


def test_create_complex_collection(simple_experiment_node, simple_inventory_node, complex_citation_node) -> None:
    """
    test to see if Collection can be made with all the possible optional arguments
    """
    my_collection_name = "my complex collection name"
    my_cript_doi = "10.1038/1781168a0"

    my_collection = cript.Collection(
        name=my_collection_name,
        experiment=[simple_experiment_node],
        inventory=[simple_inventory_node],
        doi=my_cript_doi,
        citation=[complex_citation_node],
    )

    # assertions
    assert isinstance(my_collection, cript.Collection)
    assert my_collection.name == my_collection_name
    assert my_collection.experiment == [simple_experiment_node]
    assert my_collection.inventory == [simple_inventory_node]
    assert my_collection.doi == my_cript_doi
    assert my_collection.citation == [complex_citation_node]


def test_collection_getters_and_setters(simple_experiment_node, simple_inventory_node, complex_citation_node) -> None:
    """
    test that Collection getters and setters are working properly

    1. create a simple Collection node
    2. use the setter to set the Collection node's attributes
    3. use the getter to get the Collection's attributes
    4. assert that what was set and what was gotten are the same
    """
    my_collection = cript.Collection(name="my collection name")

    new_collection_name = "my new collection name"
    new_cript_doi = "my new cript doi"

    # set Collection attributes
    my_collection.name = new_collection_name
    my_collection.experiment = [simple_experiment_node]
    my_collection.inventory = [simple_inventory_node]
    my_collection.doi = new_cript_doi
    my_collection.citation = [complex_citation_node]

    # assert getters and setters are the same
    assert isinstance(my_collection, cript.Collection)
    assert my_collection.name == new_collection_name
    assert my_collection.experiment == [simple_experiment_node]
    assert my_collection.inventory == [simple_inventory_node]
    assert my_collection.doi == new_cript_doi
    assert my_collection.citation == [complex_citation_node]


def test_serialize_collection_to_json(simple_collection_node) -> None:
    """
    test that Collection node can be correctly serialized to JSON

    1. create a simple Collection node with all required arguments
    1. convert Collection to JSON and back to dict
    1. compare expected_collection dict and Collection dict, and they should be the same

    Notes
    -----
    * Compare dicts instead of JSON string because dict comparison is more accurate
    """

    expected_collection_dict = {
        "node": ["Collection"],
        "name": "my collection name",
        "experiment": [{"node": ["Experiment"], "name": "my experiment name"}],
        "inventory": [],
        "citation": [],
    }

    # assert
    ref_dict = json.loads(simple_collection_node.json)
    ref_dict = strip_uid_from_dict(ref_dict)
    assert ref_dict == expected_collection_dict


def test_uuid(complex_collection_node):
    collection_node = complex_collection_node

    # Deep copies should not share uuid (or uids) or urls
    collection_node2 = copy.deepcopy(complex_collection_node)
    assert collection_node.uuid != collection_node2.uuid
    assert collection_node.uid != collection_node2.uid
    assert collection_node.url != collection_node2.url

    # Loads from json have the same uuid and url
    collection_node3 = cript.load_nodes_from_json(collection_node.json)
    assert collection_node3.uuid == collection_node.uuid
    assert collection_node3.url == collection_node.url


# ---------- Integration tests ----------
def test_save_collection_to_api() -> None:
    """
    tests if the Collection node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_collection_from_api() -> None:
    """
    gets the Collection node from the api that was saved prior
    """
    pass


def test_serialize_json_to_collection() -> None:
    """
    tests that a JSON of a Collection node can from API can be correctly converted to Collection python object
    """
    pass


def test_update_data_in_api() -> None:
    """
    tests that the Collection node can be correctly updated within the API
    """
    pass


def test_delete_data_from_api() -> None:
    """
    tests that the Collection node can be deleted correctly from the API
    tries to get the Collection from API, and it is expected for the API to give an error response
    """
    pass
