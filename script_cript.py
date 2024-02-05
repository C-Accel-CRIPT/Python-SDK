import cript
from cript.api.api_config import _API_TIMEOUT
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
import json

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


# WIP : will load this from a config file
class Config:
    host = "https://lb-stage.mycriptapp.org"
    token = ""
    storage_token = ""


with cript.API(host="https://lb-stage.mycriptapp.org/", api_token=Config.token, storage_token=Config.storage_token) as api:  # "https://stage.mycriptapp.org/",
    print("\n------    PROJECT    ------- ")

    host = Config.host
    class_name = "Project"
    node_type = class_name.lower()
    object_name = "proj sing wojj880f7f099923"
    object_name_change = "proj wokf788fk0999023"
    class_params = {"node_type": node_type, "object_name": object_name}  # , "host": host, "token": api_token}  # Parameters needed to instantiate the class

    if hasattr(cript, class_name):
        # Instantiate the class
        # Dynamically instantiate the Project class if it exists in the cript module
        # project = getattr(cript, class_name).get_or_create(**class_params)

        print("\ndid we get here 1")

        project = PrimaryBaseNode.get_or_create(**class_params)  # (node_type="project", object_name=object_name)  # , host=host, token=api_token)

        print("\ndid we get here 2")
        print(f"{class_name} instance created or fetched successfully: {project.uuid}  ")

        # deep diff goes here
        changes = {"node": [class_name], "name": object_name_change}

        # Assuming host and api_token are defined as per your provided code
        # response = primary_node_instance.patch(changes=changes)  # , host, api_token)
        try:
            response = project.patch(changes=changes)
            if response.status_code == 200:
                print(f"{class_name} updated successfully.")
            elif response.status_code == 409:
                print(f"duplicate Name/Data for {class_name}")

            else:
                print(f"Failed to update {class_name}. Status code: {response.status_code}")

            # ... handle successful patch
        except ValueError as e:
            print(e)  # will print "No schema found for node type Project" if schema is not found
            # ... handle the error, maybe abort the operation or log it

    else:
        print(f"Class {class_name} not found in the cript module")

    print("\n------   NOW FETCHING MATERIAL AND PATCHING IT TO PROJECT ------- ")

    # host = Config.host
    # class_name = "Material"
    # node_type = class_name.lower()
    # object_name = "Test Material B"

    if hasattr(cript, class_name):
        # Instantiate the class
        # Dynamically instantiate the Project class if it exists in the cript module
        # project = getattr(cript, class_name).get_or_create(**class_params)

        # material_node_instance = PrimaryBaseNode.get_or_create(**class_params)

        polystyrene = cript.Material(name="polystyrene", identifier=[])
        # toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}, {"pubchem_id": 1140}])
        styrene = cript.Material(name="styrene", identifier=[{"smiles": "c1ccccc1C=C"}, {"inchi": "InChI=1S/C8H8/c1-2-8-6-4-3-5-7-8/h2-7H,1H2"}])
        # butanol = cript.Material(name="1-butanol", identifier=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])

        methanol = cript.Material(name="methanol", identifier=[{"smiles": "CO"}, {"names": ["Butan-1-ol", "Butyric alcohol", "Methylolpropane", "n-Butan-1-ol", "methanol"]}])

        butanol = cript.Material(name="1-butanol", identifier=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])

        # project.material += [butanol]  # would use a += operator in theory
        project.material.append(polystyrene)
        project.material.append(butanol)

        print("\n did we instantiate material ")
        print(f"{class_name} instance created or fetched successfully: {project.uuid}  ")

        print("project.get_json()")
        result = project.get_json()
        # Assuming result is your ReturnTuple object
        json_data_string = result.json
        # Convert the JSON string to a Python dictionary
        json_data_dict = json.loads(json_data_string)
        print("json_data_dict")
        print(json_data_dict)
        print("\n\n    now here")

        res = project.save()
        print(project)
        print("\n--project.material items")
        for item in project.material:
            print(item.get_json().json)

        collection = cript.Collection(name="Initial screening")
        # We add this collection to the project as a list.
        project.collection.append(collection)

        res2 = project.save()
        print("\n -- now print project with collection")
        print(project)

    else:
        print(f"Class {class_name} not found in the cript module")
