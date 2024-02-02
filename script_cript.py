import cript
from cript.api.api_config import _API_TIMEOUT
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


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
    object_name = "proj 20249933333339"
    object_name_change = "proj 202933333399500"
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
            print(e)  # Will print "No schema found for node type Project" if schema is not found
            # ... handle the error, maybe abort the operation or log it

    else:
        print(f"Class {class_name} not found in the cript module")

    print("\n------   NOW FETCHING MATERIAL AND PATCHING IT TO PROJECT ------- ")

    host = Config.host
    class_name = "Material"
    node_type = class_name.lower()
    object_name = "Test Material B"

    # object_name_change = "Material name 5050"

    class_params = {"node_type": node_type, "object_name": object_name}  # , "host": host, "token": api_token}  # Parameters needed to instantiate the class

    if hasattr(cript, class_name):
        # Instantiate the class

        # Dynamically instantiate the Project class if it exists in the cript module

        # project = getattr(cript, class_name).get_or_create(**class_params)

        # material_node_instance = PrimaryBaseNode.get_or_create(**class_params)

        polystyrene = cript.Material(name="polystyrene", identifier=[])
        project.material = [polystyrene]

        print("\n did we instantiate material ")
        print(f"{class_name} instance created or fetched successfully: {project.uuid}  ")

        print(project.get_json())
        quit()
        # no need for deep diff

        # Assuming host and api_token are defined as per your provided code
        # response = primary_node_instance.patch(changes=changes)  # , host, api_token)
        try:
            print(dir(material_node_instance))
            quit()

            response = project.patch(changes=changes)
            if response.status_code == 200:
                print(f"{class_name} updated successfully.")
            elif response.status_code == 409:
                print(f"duplicate Name/Data for {class_name}")

            else:
                print(f"Failed to update {class_name}. Status code: {response.status_code}")

            # ... handle successful patch
        except ValueError as e:
            print(e)  # Will print "No schema found for node type Project" if schema is not found
            # ... handle the error, maybe abort the operation or log it

    else:
        print(f"Class {class_name} not found in the cript module")
