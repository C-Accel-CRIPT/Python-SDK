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
    token = "eyJraWQiOiJsUitMbmh4ZXVaODlHQVwvVThSNHMwbUNMYWR5UE9OekVUSktxOGtKbXVHOD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZmI0ZWVlNS0wMjc4LTQ4ZmUtODEzYS1hOGQ3NWNhNDA2MzYiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfdnlLMU45cDIyX0NSSVBUIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3Z5SzFOOXAyMiIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjRjbjlzNXIyMzA4OTFoMzhlNGVzYzE0NnBzIiwib3JpZ2luX2p0aSI6IjIzN2YwNjNkLTY3ZGEtNDE1ZC04YmE3LTgwYjk4YzkwZGYyYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNzA1NjIxNjkwLCJleHAiOjE3MDcxODkxNTQsImlhdCI6MTcwNzEwMjc1NCwianRpIjoiZTdlMjRkZmMtZGVkZS00YzMyLWExZTEtOGE0YzY3NTVhYjBjIiwidXNlcm5hbWUiOiJjcmlwdF82YTRhZDM1YS0wZTQxLTRmYjQtYTJhZS1kZDhlZjQ5NTFlMDQifQ.Qg0SQYdS9ufRcO3B_GrCycKAqJGGOS-X2wjsHrXhlc-Qp3RyeSrUfL93RQBsBjGfhzSh0JNxJhOZYIyA-4PuxZORLRuf0o6URZ0iq8fwo-xlyL1ilHZFZADaMmV5fdu_mxeusjZIo7_TB4W2OcxqXCBIDALfhYytSwFbRDXYcnfQaJ2ftCwOnOvETQpwSG2yLnPGM5yoGXR8aSesJoLDsRRWllCyKEraAL9xisfz0uCXWnD4N7WcJOgVloqVvZ7ZbfyQgL25SwTYBb9ZCxw5TrEeTqI6-tv-ClFfNU6MVIB2wOqsbt3vFQp8uCQWGkDmAMrn3Oib-OnuGJjf0MJddw"
    storage_token = "eyJraWQiOiJ5SHVsWSsyMkpNUDFQNmFUd2hHbmhIa3RVRFRPYitDWkI0XC9SellmRGpPQT0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiLWlCYWRYX25VRWtMeDFQTUV5ajZqQSIsInN1YiI6ImFmYjRlZWU1LTAyNzgtNDhmZS04MTNhLWE4ZDc1Y2E0MDYzNiIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV92eUsxTjlwMjJfQ1JJUFQiXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV92eUsxTjlwMjIiLCJjb2duaXRvOnVzZXJuYW1lIjoiY3JpcHRfNmE0YWQzNWEtMGU0MS00ZmI0LWEyYWUtZGQ4ZWY0OTUxZTA0Iiwib3JpZ2luX2p0aSI6IjIzN2YwNjNkLTY3ZGEtNDE1ZC04YmE3LTgwYjk4YzkwZGYyYyIsImF1ZCI6IjRjbjlzNXIyMzA4OTFoMzhlNGVzYzE0NnBzIiwiaWRlbnRpdGllcyI6W3sidXNlcklkIjoiNmE0YWQzNWEtMGU0MS00ZmI0LWEyYWUtZGQ4ZWY0OTUxZTA0IiwicHJvdmlkZXJOYW1lIjoiQ1JJUFQiLCJwcm92aWRlclR5cGUiOiJPSURDIiwiaXNzdWVyIjpudWxsLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTcwNTYyMTY4ODQzOSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3MDU2MjE2OTAsImV4cCI6MTcwNzA3MDQ3MiwiaWF0IjoxNzA2OTg0MDcyLCJqdGkiOiJkOTY3OWQyZi04Mzg3LTRiZTUtYmUzNC1iY2NkODIwNGQ5N2EiLCJlbWFpbCI6ImFsZXhhbmRyYS5kdWJveUBnbWFpbC5jb20ifQ.UI9B3QXoFetvkklE5nXs3V43ToT5so-QiXk40fBD61CGKPF3cIWK4VJaigYEyNDrxgFa7FoA_G9vA1vTYkdfechEZ1cJWmQQ9xDm4ikMA58FZZ7lZUDs1uKBwCYq9ldkOaRZTTrv3JxFPvRHAGq7ksNQ108GRGZXKV2wpovpUi5CATjOcAOa7KViBpeUUC9wN_qbTOGzKmyVgbSwlQTyxC2bn8ktK2gmAylHDIBK0OF084bZWqF_3QSvKhqw8lso9qbOW_ehUJ382OgrGbzCgCWMjhDRfMiEZqbKWX1mB3TzzqJ3jolk9i809X6y7h-vzBQsow7_34Y47oRROqmV0A"


with cript.API(host="https://lb-stage.mycriptapp.org/", api_token=Config.token, storage_token=Config.storage_token) as api:  # "https://stage.mycriptapp.org/",
    print("\n------    PROJECT    ------- ")

    host = Config.host
    class_name = "Project"
    node_type = class_name.lower()
    object_name = "proj sing 999"
    object_name_change = "proj i9"
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
        toluene = cript.Material(name="toluene", identifier=[{"smiles": "Cc1ccccc1"}, {"pubchem_id": 1140}])
        styrene = cript.Material(name="styrene", identifier=[{"smiles": "c1ccccc1C=C"}, {"inchi": "InChI=1S/C8H8/c1-2-8-6-4-3-5-7-8/h2-7H,1H2"}])
        butanol = cript.Material(name="1-butanol", identifier=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])
        methanol = cript.Material(name="methanol", identifier=[{"smiles": "CO"}, {"names": ["Butan-1-ol", "Butyric alcohol", "Methylolpropane", "n-Butan-1-ol", "methanol"]}])

        project.material = [methanol]

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

        project.save()

        # print("experiment")

        # uuid0 = project.uuid
        # uuid1_obj = PrimaryBaseNode.fetch_object_data(object_type="project", uuid=uuid0)

        # print(" -- hey fetch_object_data-- ")
        # print(uuid1_obj)
        # print(" -- hey project -- ")
        # print(project)

        # now, when you do project.save()
        # the idea is that in the save method,
        # we would first get the uuid of the fetched data from the api ,

        # obtain from uuid from api
        # save that as deep_copy_1 (an object)
        # then get the diff from deep copy and the object at hand (self)
        # then send that diff to a patch

    else:
        print(f"Class {class_name} not found in the cript module")
