import copy
import json
import time
import uuid

import pytest

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


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
    my_collection_notes = "test_create_complex_collection notes"

    my_collection = cript.Collection(name=my_collection_name, experiment=[simple_experiment_node], inventory=[simple_inventory_node], doi=my_cript_doi, citation=[complex_citation_node], notes=my_collection_notes)

    # assertions
    assert isinstance(my_collection, cript.Collection)
    assert my_collection.name == my_collection_name
    assert my_collection.experiment == [simple_experiment_node]
    assert my_collection.inventory == [simple_inventory_node]
    assert my_collection.doi == my_cript_doi
    assert my_collection.citation == [complex_citation_node]
    assert my_collection.notes == my_collection_notes


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
    new_collection_notes = "my collection getters and setters notes"

    # set Collection attributes
    my_collection.name = new_collection_name
    my_collection.experiment = [simple_experiment_node]
    my_collection.inventory = [simple_inventory_node]
    my_collection.doi = new_cript_doi
    my_collection.citation = [complex_citation_node]
    my_collection.notes = new_collection_notes

    # assert getters and setters are the same
    assert isinstance(my_collection, cript.Collection)
    assert my_collection.name == new_collection_name
    assert my_collection.experiment == [simple_experiment_node]
    assert my_collection.inventory == [simple_inventory_node]
    assert my_collection.doi == new_cript_doi
    assert my_collection.citation == [complex_citation_node]
    assert my_collection.notes == new_collection_notes

    # remove Collection attributes
    my_collection.experiment = []
    my_collection.inventory = []
    my_collection.doi = ""
    my_collection.citation = []
    my_collection.notes = ""

    # assert users can remove optional attributes
    assert my_collection.name == new_collection_name
    assert my_collection.experiment == []
    assert my_collection.inventory == []
    assert my_collection.doi == ""
    assert my_collection.citation == []
    assert my_collection.notes == ""


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
    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    simple_project_node.collection[0].doi = "my doi UPDATED"
    # TODO enable later
    # simple_project_node.collection[0].notes = "my collection notes UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_collection_node)


@pytest.mark.skip(reason="api and WIP")
def test_collection_inventory_node_change(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_material.py::test_material_property_node_change

    WIP
    change the inventory by changing the list of inventory objects
    an  inventory object will have a field "materials" a list of material nodes
    """

    epoch_time = int(time.time())
    name_1 = f"my_proj_ali_{epoch_time}"
    mat_1 = f"my_mat__{epoch_time}"

    url_path = "/project/"
    create_payload = {"node": ["Project"], "name": name_1, "inventory": [{"node": ["Inventory"], "name": "inventory_" + mat_1, "material": [{"node": ["Material"], "name": mat_1 + "mat"}]}]}

    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        print(create_response)
    except Exception as e:
        print(e)

    print(create_response.json())
    cr_res_list = create_response.json()["data"]["result"]

    if create_response.json()["code"] in [409, 400, 401]:
        print("---create_response")
        print(create_response)
        raise ValueError(create_response)

    elif create_response.json()["code"] in [201, 200]:
        print("---create_response")
        print(create_response.json())

        uuid = None
        for item in cr_res_list:
            if item["node"] == ["Material"]:
                uuid = item["uuid"]
            if item["node"] == ["Project"]:
                uuid = item["uuid"]
            if item["node"] == ["Colection"]:
                uuid = item["uuid"]
            # do inventory here
        if uuid is None:
            raise ValueError("no material node")

        get_url1 = f"/material/{uuid}"
        print("---get_url1: ", get_url1)

        result = cript_api._capsule_request(url_path=get_url1, method="GET")

        result_json_dict = result.json()
        print("\nresult_json_dict :", result_json_dict)

        my_mat_from_res_data_dict = result_json_dict["data"][0]

        mat_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_mat_from_res_data_dict))
        mat_loaded = mat_list

        print("mat_loaded")
        print(mat_loaded)

        # create a color property
        # property_001 = cript.Property(name=mat_1, identifier=[])
        color = cript.Property(key="color", value="white", type="none", unit=None)

        print("TOTAL RESET ON THIS")
        mat_loaded.property = [color]

        """
        1 - get existing material node by uuid - paginator
          - or create material node with a property

        2 - make an edit to a child node (property or process or component)
        3 - save the node
        """

        print("\n~~~~~~~~~~~~ SAVING NOW ~~~~~~~~~~~")
        print(mat_loaded)  # material_loaded
        print("--//--")
        # print(dir(mat_loaded))

        url_path = cript_api.save_node(mat_loaded)  # material_loaded
