import cript
from cript.api.api_config import _API_TIMEOUT
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
import json
import os
import requests, time

# ============== NOTES ==============
# 1) get request - check if project exists
# - if exists will get response of object , original object that we will pass to the update function
# original stored, deep copy
# update
# project.material = [ new_material ]
# when you hit save it will figure out this already existed
# patch that will take the diff and send just the delta
# final object will need to be validated by json schema main node as reference
# if the project doesnt exist you send a post and theres , no diff just create
# project.save()
# ============================


# remember , after some time, will need the set -a, source .env, set +a
class Config:
    host = os.getenv("HOST")
    api_token = os.getenv("API_KEY")
    storage_token = os.getenv("STORAGE_KEY")
    delete_all_projs = False
    material_name = "N9"
    # object_name = "Brili P1"  # "try444"  # "project0110"
    object_name = "H@LL0"
    mat_name1 = "material_90900"
    mat_name2 = "butanol"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}


with cript.API(host=Config.host, api_token=Config.api_token, storage_token=Config.storage_token) as api:  # "https://stage.mycriptapp.org/",
    print("\n------    PROJECT    ------- ")

    class_name = "Project"
    node_type = class_name.lower()
    object_name = Config.object_name
    object_name_change = "boohoo1"
    class_params = {"node": node_type, "name": object_name}  #   , "material": [{"node": ["Material"], "name": Config.material_name}]}  # , "host": host, "token": api_token}  # Parameters needed to instantiate the class

    if Config.delete_all_projs:
        get_url = f"{Config.host}/api/v1/project"
        headers = {"Authorization": f"Bearer {Config.api_token}", "Content-Type": "application/json"}
        try:
            big_proj_list = requests.get(get_url, headers=headers).json()["data"]["result"]
            # print("big_proj_list")
            # print(big_proj_list)
            # print("get_url")
            # print(get_url)
            # print(api_token)
            # quit()
            # big_proj_list = big_proj_list["result"]
            for item in big_proj_list:
                time.sleep(1)
                print(item["uuid"])
                url = f"https://lb-stage.mycriptapp.org/api/v1/project/{item['uuid']}"
                res = requests.delete(url, headers=headers)
                print(url)
                print(res.json())
            print("ended the thing")
        except Exception as e:
            print(e)
        quit()

    if hasattr(cript, class_name):
        # get_url = "https://lb-stage.mycriptapp.org/api/v1/project/e7381525-64b9-4849-a416-57aa1e09044f"
        # result = requests.get(url=get_url, headers=Config.headers)
        # print(result)

        # my_project_from_api_dict = result.json()

        # # project = cript.load_nodes_from_json(json)

        # my_project_node_from_api = cript.load_nodes_from_json(nodes_json=json.dumps(my_project_from_api_dict))

        # print(type(my_project_node_from_api))
        # print("-------")
        # api.save_node(my_project_node_from_api)

        # ====================================
        # Instantiate the class
        # Dynamically instantiate the Project class if it exists in the cript module
        # project = getattr(cript, class_name).get_or_create(**class_params)
        # maybe we need to validate the class params

        # project = PrimaryBaseNode.get_or_create(**class_params)  # also any leftover kwargs will be passed and accepted ? # (node_type="project", object_name=object_name)  # , host=host, token=api_token)
        project = api.get_or_create(**class_params)  # also any leftover kwargs will be passed and accepted ? # (node_type="project", object_name=object_name)  # , host=host, token=api_token)

        # ===========================================================================

        # project = cript.Project(name="My first project.")
        print("\n\n@@@@@ here we go")

        material9000 = cript.Material(name=Config.mat_name1, identifier=[])
        material2000 = cript.Material(name=Config.mat_name2, identifier=[])
        material_000 = cript.Material(name="aa1511", identifier=[])
        material_001 = cript.Material(name="aa2252", identifier=[])
        material_002 = cript.Material(name="aa3533", identifier=[])
        material_003 = cript.Material(name="aa4544", identifier=[])

        collection = cript.Collection(name="Initial-screening")
        collection2 = cript.Collection(name="22-Initial-screening")
        collection3 = cript.Collection(name="44-Initial-screening")
        # We add this collection to the project as a list.
        # project.collection.append(collection)

        project.material += [material9000, material_000, material2000]
        # ------------------------
        project.material += [material_001]
        project.material += [material_002]
        project.material += [material_003]

        project.collection.append(collection)
        project.collection.append(collection2)
        project.collection.append(collection3)

        print("----- project !!!!!\n")
        print(project)

        # project.save()
        # api.save_node(project)
        # quit()

        print("\n\n@@@@@ here we go 2 ")
        material2000 = cript.Material(name=Config.mat_name2, identifier=[])
        project.material = [material2000]
        print(project)
        api.save_node(project)

        # =========================OLD=============================================

        # Alright:
        # say we just send a post request to make a
        # node = "project"
        # url = f"{Config.host}/api/v1/{node}"
        # data = {"node": [node.capitalize()], "name": Config.object_name, "material": [{"node": ["Material"], "name": Config.material_name}]}  # , "public": Config.is_public}
        # # data.update(kwargs)
        # headers = {"Authorization": f"Bearer {Config.api_token}", "Content-Type": "application/json"}

        # # print("NODE TYPE == PROJECT - do post")

        # response = requests.post(url, json=data, headers=headers)
        # # uuid = response.json()["data"]["result"][0].get("uuid")
        # # node_data = cls.fetch_object_data(node, uuid)

        # # print("response.json()")
        # # print(response.json())
        # # quit()
        # obj_data = response.json()["data"]["result"][0]
        # node_class = getattr(cript, "Project")  # node.capitalize())
        # project = node_class(**obj_data)
        # print(":::obj_data")
        # print(obj_data)
        # print("-------------")
        # print(project)
        # quit()

        # ======================================================================
        print(" ----- GOT BACK OUT")
        print("project.get_json().json")
        print("----")
        try:
            print(project.get_json().json)
        except Exception as e:
            print("didnt work get project")
            print(e)

        # deep diff goes here

        changes = {"node": [class_name], "name": object_name_change}

        quit()
        # Assuming host and api_token are defined as per your provided code
        # response = primary_node_instance.patch(changes=changes)  # , host, api_token)
        try:
            response = project.patch(changes=changes)
            if response.status_code == 200:
                print(f"{class_name} updated successfully.")
            elif response.status_code == 409:
                print(f"duplicate Name/Data for {class_name}")

            else:
                print(f"UGH Failed to update  {class_name}. \n response is: {response}")

            # ... handle successful patch
        except ValueError as e:
            print(e)  # will print "No schema found for node type Project" if schema is not found
            # ... handle the error, maybe abort the operation or log it

    else:
        print(f"Class {class_name} not found in the cript module")

    print("\n------   NOW FETCHING NEW MATERIAL AND PATCHING IT TO PROJECT ------- ")

    # host = Config.host
    # class_name = "Material"
    # node_type = class_name.lower()
    # object_name = "Test Material B"

    if hasattr(cript, class_name):
        # Instantiate the class
        # Dynamically instantiate the Project class if it exists in the cript module
        # project = getattr(cript, class_name).get_or_create(**class_params)

        # material_node_instance = PrimaryBaseNode.get_or_create(**class_params)

        # print("\n   GET HERE for material??")
        class_name = "Material"
        node_type = class_name.lower()
        object_name = "material777"
        # object_name_change = "soy cup"
        parent_uuid = project.uuid
        parent_node_type = str(project.node_type).lower()
        # print(parent_node_type)
        # quit()
        class_params = {"identifier": [], "node_type": node_type, "object_name": object_name, "parent_uuid": parent_uuid, "parent_node_type": parent_node_type}

        # material2000 = PrimaryBaseNode.get_or_create(**class_params)

        # ------

        # polystyrene = cript.Material(name="polystyrene", identifier=[])
        # # toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}, {"pubchem_id": 1140}])
        # styrene = cript.Material(name="styrene", identifier=[{"smiles": "c1ccccc1C=C"}, {"inchi": "InChI=1S/C8H8/c1-2-8-6-4-3-5-7-8/h2-7H,1H2"}])
        # # butanol = cript.Material(name="1-butanol", identifier=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])
        # methanol = cript.Material(name="methanol", identifier=[{"smiles": "CO"}, {"names": ["Butan-1-ol", "Butyric alcohol", "Methylolpropane", "n-Butan-1-ol", "methanol"]}])
        butanol = cript.Material(name="1-butanol", identifier=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])

        print("--------- PROJ 1ST TIME ----------")
        print(project)

        # -------
        material9000 = cript.Material(name="material_9000", identifier=[])
        # material9000 = PrimaryBaseNode.get_or_create(**class_params)
        # -------

        # project.material += [butanol]  # would use a += operator in theory
        # project.material.append(polystyrene)
        project.material = [material9000]
        project.material.append(butanol)

        # create a phase property
        phase = cript.Property(key="phase", value="solid", type="none", unit=None)
        # create a color property
        color = cript.Property(key="color", value="white", type="none", unit=None)

        # add the properties to the material
        material9000.property += [phase, color]

        print("\n--------- PROJ wait ... ----------")
        print(project)

        # --------------------

        print("\n did we instantiate material ")
        print(type(material9000))
        # print(f"{class_name} instance created or fetched successfully: {material9000.uuid}  ")

        # print("project.get_json()")
        result = project.get_json()
        # Assuming result is your ReturnTuple object
        json_data_string = result.json
        # Convert the JSON string to a Python dictionary
        json_data_dict = json.loads(json_data_string)
        # print("json_data_dict")
        # print(json_data_dict)
        # print("\n\n    now here")

        res = project.save()
        print("\n--------- PROJ 2ND TIME ----------")
        print(project)
        print(material9000)

        # print("\n--project.material items")
        # # loop through material list, could do material.save()

        # for item in project.material:
        #     print(item.get_json().json)

        # collection = cript.Collection(name="Initial screening")
        # # We add this collection to the project as a list.
        # project.collection.append(collection)

        # res2 = project.save()
        # print("\n -- now print project with collection")
        # print(project)

    else:
        print(f"Class {class_name} not found in the cript module")
