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
        "inventory": [],
        "citation": [],
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


# ---------- Integration tests ----------
def test_integration_collection(cript_api, simple_project_node, simple_collection_node):
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

    # rename project and collection to not bump into duplicate issues
    simple_project_node.name = "test_integration_collection_project_name"
    simple_collection_node.name = "test_integration_collection_collection_name"

    simple_project_node.collection = [simple_collection_node]

    # exception handling in case the project node already exists in DB and there is no docker container
    try:
        cript_api.save(project=simple_project_node)
    except Exception as error:
        # handling duplicate project name errors
        if "http:409 duplicate item" in str(error):
            pass
        else:
            raise Exception(error)

    my_paginator = cript_api.search(node_type=cript.Project, search_mode=cript.SearchModes.EXACT_NAME, value_to_search=simple_project_node.name)

    my_project_from_api_dict = my_paginator.current_page_results[0]

    print("\n\n------------------------------------------------------")
    print(json.dumps(my_project_from_api_dict))
    print("------------------------------------------------------")

    print("\n\n------------------------------------------------------")
    print(simple_project_node.json)
    print("------------------------------------------------------")

    # my_project_from_api_node = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))

    # check equivalent JSON dicts
    # assert json.dumps(my_paginator.current_page_results[0]) == simple_project_node.json
