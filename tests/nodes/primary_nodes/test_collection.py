import copy
import json
import uuid

from integration_test_helper import integrate_nodes_helper, delete_integration_node_helper
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
    5. test that the attributes can also be removed as well from the node (either None, empty list, or empty str)
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

    # remove Collection attributes
    my_collection.experiment = []
    my_collection.inventory = []
    my_collection.doi = ""
    my_collection.citation = []

    # assert users can remove optional attributes
    assert my_collection.name == new_collection_name
    assert my_collection.experiment == []
    assert my_collection.inventory == []
    assert my_collection.doi == ""
    assert my_collection.citation == []


def test_serialize_collection_to_json(complex_user_node) -> None:
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
        "member": [json.loads(copy.deepcopy(complex_user_node).json)],
        "admin": [json.loads(complex_user_node.json)],
    }

    collection_node = cript.load_nodes_from_json(json.dumps(expected_collection_dict))
    print(collection_node.get_json(indent=2).json)
    # assert
    ref_dict = json.loads(collection_node.get_json(condense_to_uuid={}).json)
    ref_dict = strip_uid_from_dict(ref_dict)

    assert ref_dict == strip_uid_from_dict(expected_collection_dict)


def test_uuid(complex_collection_node):
    collection_node = complex_collection_node

    # Deep copies should not share uuid (or uids) or urls
    collection_node2 = copy.deepcopy(complex_collection_node)
    assert collection_node.uuid != collection_node2.uuid
    assert collection_node.uid != collection_node2.uid
    assert collection_node.url != collection_node2.url

    # Loads from json have the same uuid and url
    collection_node3 = cript.load_nodes_from_json(collection_node.get_json(condense_to_uuid={}).json)
    assert collection_node3.uuid == collection_node.uuid
    assert collection_node3.url == collection_node.url


def test_integration_collection(cript_api, simple_project_node, simple_collection_node):
    """
    integration test between Python SDK and API Client

    ## Create
    1. Serialize SDK Nodes to JSON
    1. POST to API
    1. GET from API
    1. Deserialize API JSON to SDK Nodes
    1. assert they're both equal

    ## Update
    1. Change JSON
    1. POST/PATCH to API
    1. GET from API
    1. Deserialize API JSON to SDK Nodes
    1. assert they're both equal

    Notes
    -----
    - [x] Create
    - [x] Read
    - [x] Update
    """

    # rename project and collection to not bump into duplicate issues
    simple_project_node.name = f"test_integration_collection_project_name_{uuid.uuid4().hex}"
    simple_collection_node.name = f"test_integration_collection_name_{uuid.uuid4().hex}"

    simple_project_node.collection = [simple_collection_node]

    # ========= test create =========
    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    simple_project_node.collection[0].doi = "my doi UPDATED"
    # TODO enable later
    # simple_project_node.collection[0].notes = "my collection notes UPDATED"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_collection_node)
