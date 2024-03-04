import json
import uuid

import time

import cript

from tests.utils.integration_test_helper import delete_integration_node_helper, save_integration_node_helper  # , _create_node
from tests.utils.util import strip_uid_from_dict

# try this or else put it in tests.utils.util
# from cript.api.utils.helper_functions import _create_node


def test_create_simple_project(simple_collection_node) -> None:
    """
    test that a project node with only required arguments can be created
    """
    my_project_name = "my Project name"

    my_project = cript.Project(name=my_project_name, collection=[simple_collection_node])

    # assertions
    assert isinstance(my_project, cript.Project)
    assert my_project.name == my_project_name
    assert my_project.collection == [simple_collection_node]


def test_project_getters_and_setters(simple_project_node, simple_collection_node, complex_collection_node, simple_material_node) -> None:
    """
    tests that a Project node getters and setters are working as expected

    1. use a simple project node
    2. set all of its attributes to something new
    3. get all of its attributes
    4. what was set and what was gotten should be equivalent
    """
    new_project_name = "my new project name"
    new_project_notes = "my new project notes"

    # set attributes
    simple_project_node.name = new_project_name
    simple_project_node.collection = [complex_collection_node]
    simple_project_node.material = [simple_material_node]
    simple_project_node.notes = new_project_notes

    # get attributes and assert that they are the same
    assert simple_project_node.name == new_project_name
    assert simple_project_node.collection == [complex_collection_node]
    assert simple_project_node.material == [simple_material_node]
    assert simple_project_node.notes == new_project_notes

    # remove optional attributes
    simple_project_node.collection = []
    simple_project_node.material = []
    simple_project_node.notes = ""

    # assert optional attributes have been removed
    assert simple_project_node.collection == []
    assert simple_project_node.material == []
    assert simple_project_node.notes == ""


def test_serialize_project_to_json(complex_project_node, complex_project_dict) -> None:
    """
    tests that a Project node can be correctly converted to a JSON
    """
    expected_dict = complex_project_dict

    # Since we condense those to UUID we remove them from the expected dict.
    expected_dict["admin"] = [{}]
    expected_dict["member"] = [{}]

    # comparing dicts instead of JSON strings because dict comparison is more accurate
    serialized_project: dict = json.loads(complex_project_node.get_json(condense_to_uuid={}).json)
    serialized_project = strip_uid_from_dict(serialized_project)

    assert serialized_project == strip_uid_from_dict(expected_dict)


def test_integration_project(cript_api, simple_project_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_project_name_{uuid.uuid4().hex}"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    simple_project_node.notes = "project notes UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_project_node)


"""
main changes here - 
we need to get rid of env stuff 
we need to replace requests with capsule

we need to replace anything here that has create node 
    - put that into util func or capsule?

- object_exists - next generator
- find_uuid_by_name_and_type - next generator
"""


def test_update_project_change_or_reset_materials_newly_made(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_update_project_change_or_reset_materials_newly_made
    test that a project can be updated and completley reset
    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data
    """

    epoch_time = int(time.time())
    name_1 = f"myproj_ali_{epoch_time}"
    mat_1 = f"my_mat__{epoch_time}"
    col_name = "031o0col"

    # print("hello")

    # url_path = f"/{node.node_type_snake_case}/"
    url_path = f"/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"uuid": "1809330c-31d2-4a80-af72-77b84070ee1d"}, {"uuid": "ea8f957c-b6e5-4668-b306-e0d6b0d05d9a"}]}

    # print(cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload)).json())

    # quit()
    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        print(create_response)
    except Exception as e:
        print(e)

    cr_res_list = create_response.json()["data"]["result"]

    if create_response.json()["code"] in [409, 400, 401]:
        print("---create_response")
        print(create_response)
        raise ValueError(create_response)

    elif create_response.json()["code"] in [201, 200]:

        uuid = None
        for item in cr_res_list:
            if item["node"] == ["Project"]:

                uuid = item["uuid"]
        if uuid == None:
            raise ValueError("no project node")

        get_url = f"/project/{uuid}"

        result = cript_api._capsule_request(url_path=get_url, method="GET")

        result_json_dict = result.json()

        my_project_from_res_data_dict = result_json_dict["data"][0]

        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list

        material_001 = cript.Material(name=mat_1, identifier=[])

        collection = cript.Collection(name=col_name)

        project_loaded.material = [material_001]  # [material_001]

        project_loaded.collection = [collection]

        # print("\n~~~~~~~~~~~~ SAVING NOW ~~~~~~~~~~~")
        cript_api.save_node(project_loaded)
        # print("BASICALLY now WE NEED TO ASSERT ON THE RESPONSE, NOT RELOAD IT INTO A NODE")

        # print("\n-- probably need to fix save --\n---project after saved")

        get_url = f"/project/{uuid}"
        edited_result = cript_api._capsule_request(url_path=get_url, method="GET")

        # print("\n~~~~~~ saved reflected result")
        # print(edited_result.json())

        assert len(edited_result.json()["data"]) == 1

        final = edited_result.json()["data"][0]

        assert len(final["material"]) == 1

        assert final["material"][0]["name"] == json.loads(material_001.get_json().json)["name"]  # or material_003toluene.get_json().json)["name"]
        assert final["collection"][0]["name"] == json.loads(collection.get_json().json)["name"]

        # print("now deleting proj and eventually 2 mats")
        # print("only issue with this test is the toluene")

        del_res = cript_api._capsule_request(url_path=f"/project/{uuid}", method="DELETE")

        assert del_res.json()["code"] == 200


def test_update_project_change_or_reset_material_to_existing_materials(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_update_project_change_or_reset_material_to_existing_materials
    test that a project can be updated and completley reset
    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data
    """

    epoch_time = int(time.time())
    name_1 = f"myproj_ali_{epoch_time}"
    mat_1 = f"my_mat__{epoch_time}"
    col_name = f"031o0col__{epoch_time}"

    url_path = f"/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"uuid": "1809330c-31d2-4a80-af72-77b84070ee1d"}, {"uuid": "ea8f957c-b6e5-4668-b306-e0d6b0d05d9a"}]}

    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        # print(create_response)
    except Exception as e:
        print(e)
        raise ValueError(e)

    cr_res_list = create_response.json()["data"]["result"]

    if create_response.json()["code"] in [409, 400, 401]:
        # print("---create_response")
        # print(create_response)
        raise ValueError(create_response)

    elif create_response.json()["code"] in [201, 200]:

        uuid = None
        for item in cr_res_list:
            if item["node"] == ["Project"]:

                uuid = item["uuid"]
        if uuid == None:
            raise ValueError("no project node")

        get_url = f"/project/{uuid}"

        result = cript_api._capsule_request(url_path=get_url, method="GET")

        result_json_dict = result.json()

        my_project_from_res_data_dict = result_json_dict["data"][0]

        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list

        material_001 = cript.Material(name=mat_1, identifier=[])
        toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}])  # , {"pubchem_id": 1140}])
        styrene = cript.Material(name="styrene", identifier=[{"smiles": "Cc1ccccc1"}])

        collection = cript.Collection(name=col_name)

        project_loaded.material = [toluene, styrene]
        project_loaded.collection = [collection]

        cript_api.save_node(project_loaded)

        get_url = f"/project/{uuid}"
        edited_result = cript_api._capsule_request(url_path=get_url, method="GET")

        assert len(edited_result.json()["data"]) == 1

        final = edited_result.json()["data"][0]

        assert len(final["material"]) == 2  # styrene and toluene

        set1 = set([final["material"][0]["name"].lower(), final["material"][1]["name"].lower()])

        set2 = set([json.loads(toluene.get_json().json)["name"].lower(), json.loads(styrene.get_json().json)["name"].lower()])

        assert set1 == set2  # or material_003toluene.get_json().json)["name"]

        assert final["collection"][0]["name"] == json.loads(collection.get_json().json)["name"]

        del_res = cript_api._capsule_request(url_path=f"/project/{uuid}", method="DELETE")

        assert del_res.json()["code"] == 200


def test_add_existing_materials_by_name_to_project(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_add_existing_materials_by_name_to_project
    test that a project can be updated and completley reset
    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data
    """

    epoch_time = int(time.time())
    name_1 = f"myproj_ali_{epoch_time}"

    url_path = f"/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"uuid": "1809330c-31d2-4a80-af72-77b84070ee1d"}, {"uuid": "ea8f957c-b6e5-4668-b306-e0d6b0d05d9a"}]}

    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        # print(create_response)
    except Exception as e:

        print(e)

    cr_res_list = create_response.json()["data"]["result"]

    if create_response.json()["code"] in [409, 400]:

        # print(create_response)
        raise ValueError(create_response)

    elif create_response.json()["code"] in [201, 200]:

        uuid = None
        for item in cr_res_list:
            if item["node"] == ["Project"]:
                uuid = item["uuid"]
        if uuid == None:
            raise ValueError("no project node")

        get_url = f"/project/{uuid}"

        result = cript_api._capsule_request(url_path=get_url, method="GET")

        result_json_dict = result.json()

        my_project_from_res_data_dict = result_json_dict["data"][0]

        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list

        # toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}])  # , {"pubchem_id": 1140}])
        # styrene = cript.Material(name="styrene", identifier=[{"smiles": "Cc1ccccc1"}])

        # print("\n~~~~~~~~~~~~ ADDING NOW ~~~~~~~~~~~")

        # cript_api.add_existing_node_by_name(parent_node=project_loaded, child_node=toluene)
        add_res = cript_api.add_existing_nodes_by_name(parent_node=project_loaded, child_class_type="material", existing_child_node_names=["toluene", "styrene"])
        assert add_res.json()["code"] == 200


def test_remove_existing_materials_by_name_from_project(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_remove_existing_materials_by_name_from_project
    test that a project can be updated and completley reset
    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data
    """

    epoch_time = int(time.time())
    name_1 = f"myproj_ali_{epoch_time}"

    url_path = f"/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"uuid": "1809330c-31d2-4a80-af72-77b84070ee1d"}, {"uuid": "ea8f957c-b6e5-4668-b306-e0d6b0d05d9a"}]}

    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        # print(create_response)
    except Exception as e:

        print(e)

    cr_res_list = create_response.json()["data"]["result"]

    if create_response.json()["code"] in [409, 400]:

        # print(create_response)
        raise ValueError(create_response)

    elif create_response.json()["code"] in [201, 200]:

        uuid = None
        for item in cr_res_list:
            if item["node"] == ["Project"]:
                uuid = item["uuid"]
        if uuid == None:
            raise ValueError("no project node")

        get_url = f"/project/{uuid}"

        result = cript_api._capsule_request(url_path=get_url, method="GET")
        result_json_dict = result.json()
        my_project_from_res_data_dict = result_json_dict["data"][0]

        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list

        # toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}])  # , {"pubchem_id": 1140}])
        # styrene = cript.Material(name="styrene", identifier=[{"smiles": "Cc1ccccc1"}])

        # print("\n~~~~~~~~~~~~ ADDING NOW ~~~~~~~~~~~")

        # cript_api.add_existing_node_by_name(parent_node=project_loaded, child_node=toluene)
        add_res = cript_api.add_existing_nodes_by_name(parent_node=project_loaded, child_class_type="material", existing_child_node_names=["toluene", "styrene"])

        # print("\n~~~~~~~~~~~~ now deleteing ~~~~~~~~~~~")

        delete_res = cript_api.remove_nodes_by_name(parent_node=project_loaded, child_class_type="material", existing_child_node_names=["toluene", "styrene"])

        assert delete_res.json()["code"] == 200
