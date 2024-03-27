import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict
import cript
import requests
import os
import time


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


def test_update_project_add_material_and_collection(simple_collection_node, cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_update_project_add_material_and_collection
    test that a project can be updated an reset

    need to creat ethe node to the api 
    just a simple function that makes the post 
    api.create_on

    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data

    """
    # create a new project to be in api and save
    # save it to database via api 

    # cript_api = cript.API
    my_project_name = "test-project-name"
    create_payload = {"node":["Project"], "name":my_project_name}
    create_response = cript_api.create_node("project" ,create_payload)


    if create_response.json()["code"] in [409,400]:
        raise ValueError(create_response)
        # load_nodes_from_json is what i awan tnext 
        
    elif create_response.json()["code"] in [201,200]:


        # the proper deserialization from the get request 

        uuid = create_response.json()['data']['result'][0]['uuid']
        print('uuid')
        print(uuid)

        # 1) from get request for deserialization 1
        get_url = f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}"
        headers = {"Authorization": f"Bearer {os.environ["CRIPT_TOKEN"]}", "Content-Type": "application/json"}
        # headers = cript_api._http_headers
        result = requests.get(url=get_url, headers=headers)
        print("result")
        result_json_dict = result.json()
        my_project_from_api_dict = result_json_dict["data"]
        print("my_project_from_api_dict")
        print(my_project_from_api_dict)
        # Now your instinct was right to give it a string version, but I want to fix that
        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))
        project_loaded = project_list[0]
        print("\nproject")
        print(project_loaded)

        material_001 = cript.Material(name="M001", identifier=[])
        material_002 = cript.Material(name="M002", identifier=[])
        collection = cript.Collection(name="222-Initial-screening")

        # TOTALLY RESET
        project_loaded.material = [material_001, material_002]
        project_loaded.collection = [collection]
        cript_api.save_node(project_loaded)
        print("\n\n---project after saved")
        print(project_loaded.get_json().json)


        # 2) from get request for deserialization 2 - (then assert)
        get_url = f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}"
        headers = {"Authorization": f"Bearer {os.environ["CRIPT_TOKEN"]}", "Content-Type": "application/json"}
        # headers = cript_api._http_headers
        result = requests.get(url=get_url, headers=headers)
        print("result")
        result_json_dict = result.json()
        my_project_from_api_dict = result_json_dict["data"]
        print("my_project_from_api_dict")
        print(my_project_from_api_dict)
        # Now your instinct was right to give it a string version, but I want to fix that
        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))
        project_loaded = project_list[0]
        print("\nproject2")
        print(project_loaded)

        # DO SOME ASSERTS HERE 
        assert project_loaded.material == [material_001, material_002]
        assert project_loaded.collection == [collection]
 
        # at the end delete the data
        del_res = requests.delete(f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}", headers=headers)
        assert del_res.json()["code"] == 200
        #------------------------------------------------

        


def test_update_project_change_or_reset_material(simple_collection_node, cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_project.py::test_update_project_add_material_and_collection
    test that a project can be updated and completley reset

    strategy:
    create something with a post/patch
    with a name (we will delete at  the end)
    then try to obtain it with load data

    """

    epoch_time = int(time.time())
    name_1 = f"myproj_ali_{epoch_time}"
    mat_3 = f"my_mat__{epoch_time}"
    col_name = "031o0col"

    create_payload = {"node":["Project"], "name":name_1,
                      "material":
                      [
                            {"uuid": "1809330c-31d2-4a80-af72-77b84070ee1d"},
                            {"uuid": "ea8f957c-b6e5-4668-b306-e0d6b0d05d9a"},
                            {"uuid": "3bd734c3-9c4a-47e3-ad25-f6cbd9309683"}
                      ]}
    try:
        create_response = cript_api.create_node("project" ,create_payload)
    except Exception as e:
        print(e)


    cr_res_list = create_response.json()["data"]["result"]

    
    if create_response.json()["code"] in [409,400]:
        print("---create_response")
        print(create_response)
        raise ValueError(create_response)

        
    elif create_response.json()["code"] in [201,200]:
        # print(" got here ")
        uuid = None
        for item in cr_res_list:
            if item['node'] == ['Project']:
            # if item['node'] == ['Project']:
                uuid = item['uuid']
        if uuid == None:
            raise ValueError("no project node")
        

        get_url = f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}"
        headers = {"Authorization": f"Bearer {os.environ["CRIPT_TOKEN"]}", "Content-Type": "application/json"}
        # headers = cript_api._http_headers
        result = requests.get(url=get_url, headers=headers)
        print("~~~~result")
        result_json_dict = result.json()
        my_project_from_res_data_dict = result_json_dict["data"][0]
        print("~~~~my_project_from_api_dict")

        # my_project_from_res_data_dict.pop('admin')
        print(type(my_project_from_res_data_dict))
        print(my_project_from_res_data_dict)
        
        # Now your instinct was right to give it a string version, but I want to fix that
        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list
        print("\n~~~~project_loaded")
        print(project_loaded)

        material_003 = cript.Material(name=mat_3, identifier=[])
        toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"} ])  #, {"pubchem_id": 1140}])
        # styrene = cript.Material(name="styrene", identifier=[{"smiles": "c1ccccc1C=C"}, {"inchi": "InChI=1S/C8H8/c1-2-8-6-4-3-5-7-8/h2-7H,1H2"}])

        collection = cript.Collection(name=col_name)

        # TOTALLY RESET to toluene or my material material_003

        # project_loaded.material = [material_003]
        project_loaded.material = [toluene]
        project_loaded.collection = [collection] 
   
        print("\n~~~~TOTALLY RESET~~~~project_loaded")
        print("\n~~~~~~~~~~~~ SAVING NOW ~~~~~~~~~~~")
        cript_api.save_node(project_loaded)
        
        print("\n-- probably need to fix save --\n---project after saved")


        # 2) manual get request for deserialization 2 - (then assert)
        get_url = f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}" # change the way headers are used
        headers = {"Authorization": f"Bearer {os.environ["CRIPT_TOKEN"]}", "Content-Type": "application/json"}
        result = requests.get(url=get_url, headers=headers) #cript_api._http_headers

        print("\n~~~~~~ saved reflected result")
        result_json_dict = result.json()
        my_project_from_res_data_dict = result_json_dict["data"]
        print("my_project_from_api_dict")
        print(my_project_from_res_data_dict)

        project_list = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_res_data_dict))
        project_loaded = project_list[0]
        print("\nproject2")
        print(project_loaded)
        
       
         # DO SOME ASSERTS HERE 
        print(project_loaded.material[0].get_json().json)

        assert json.loads(project_loaded.material[0].get_json().json)["name"]== json.loads(toluene.get_json().json)["name"]# or material_003toluene.get_json().json)["name"]
        assert len(project_loaded.material) == 1
        assert  json.loads(project_loaded.collection[0].get_json().json)["name"] == json.loads(collection.get_json().json)["name"]
 
        # at the end delete the data
        print("now deleting proj and eventually 2 mats")
        print("only issue with this test is the toluene")

        del_res = requests.delete(f"https://lb-stage.mycriptapp.org/api/v1/project/{uuid}", headers=headers)

        assert del_res.json()["code"] == 200

        # quit()



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


# =====================================================================================
def test_save_node_project(cript_api, simple_project_node):
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
