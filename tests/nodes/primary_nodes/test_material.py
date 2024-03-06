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


def test_create_complex_material(cript_api, simple_material_node, simple_computational_forcefield_node, simple_process_node) -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    material_name = "my material name"
    identifier = [{"bigsmiles": "1234"}, {"bigsmiles": "4567"}]
    keyword = ["acetylene"]
    material_notes = "my material notes"

    component = [simple_material_node]
    forcefield = simple_computational_forcefield_node

    my_property = [cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")]

    my_material = cript.Material(name=material_name, identifier=identifier, keyword=keyword, component=component, process=simple_process_node, property=my_property, computational_forcefield=forcefield, notes=material_notes)

    assert isinstance(my_material, cript.Material)
    assert my_material.name == material_name
    assert my_material.identifier == identifier
    assert my_material.keyword == keyword
    assert my_material.component == component
    assert my_material.process == simple_process_node
    assert my_material.property == my_property
    assert my_material.computational_forcefield == forcefield
    assert my_material.notes == material_notes


def test_invalid_material_keywords() -> None:
    """
    tries to create a material with invalid keywords and expects to get an Exception
    """
    # with pytest.raises(InvalidVocabulary):
    pass


def test_all_getters_and_setters(simple_material_node, simple_property_node, simple_process_node, simple_computational_forcefield_node) -> None:
    """
    tests the getters and setters for the simple material object

    1. sets every possible attribute for the simple_material object
    2. gets every possible attribute for the simple_material object
    3. asserts that what was set and what was gotten are the same
    """
    # new attributes
    new_name = "new material name"
    new_notes = "new material notes"

    new_identifier = [{"bigsmiles": "6789"}]

    new_parent_material = cript.Material(
        name="my parent material",
        identifier=[
            {"bigsmiles": "9876"},
        ],
    )

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(
            name="my component material 1",
            identifier=[
                {"bigsmiles": "654321"},
            ],
        ),
    ]

    # set all attributes for Material node
    simple_material_node.name = new_name
    simple_material_node.identifier = new_identifier
    simple_material_node.property = [simple_property_node]
    simple_material_node.parent_material = new_parent_material
    simple_material_node.computational_forcefield = simple_computational_forcefield_node
    simple_material_node.keyword = new_material_keywords
    simple_material_node.component = new_components
    simple_material_node.notes = new_notes

    # get all attributes and assert that they are equal to the setter
    assert simple_material_node.name == new_name
    assert simple_material_node.identifier == new_identifier
    assert simple_material_node.property == [simple_property_node]
    assert simple_material_node.parent_material == new_parent_material
    assert simple_material_node.computational_forcefield == simple_computational_forcefield_node
    assert simple_material_node.keyword == new_material_keywords
    assert simple_material_node.component == new_components
    assert simple_material_node.notes == new_notes

    # remove optional attributes
    simple_material_node.property = []
    simple_material_node.parent_material = None
    simple_material_node.computational_forcefield = None
    simple_material_node.component = []
    simple_material_node.notes = ""

    # assert optional attributes have been removed
    assert simple_material_node.property == []
    assert simple_material_node.parent_material is None
    assert simple_material_node.computational_forcefield is None
    assert simple_material_node.component == []
    assert simple_material_node.notes == ""


def test_serialize_material_to_json(complex_material_dict, complex_material_node) -> None:
    """
    tests that it can correctly turn the material node into its equivalent JSON
    """
    # the JSON that the material should serialize to

    # compare dicts because that is more accurate
    ref_dict = json.loads(complex_material_node.get_json(condense_to_uuid={}).json)
    ref_dict = strip_uid_from_dict(ref_dict)

    assert ref_dict == complex_material_dict


def test_integration_material(cript_api, simple_project_node, simple_material_node) -> None:
    """
    integration test between Python SDK and API Client

    tests both POST and GET

    1. create a project
    1. create a material
    1. add a material to project
    1. save the project
    1. get the project
    1. deserialize the project
    1. compare the project node that was sent to API and the one API gave, that they are the same
    """
    # ========= test create =========
    # creating unique name to not bump into unique errors
    simple_project_node.name = f"test_integration_project_name_{uuid.uuid4().hex}"
    simple_material_node.name = f"test_integration_material_name_{uuid.uuid4().hex}"

    simple_project_node.material = [simple_material_node]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test update =========
    # update material attribute to trigger update
    simple_project_node.material[0].identifier = [{"bigsmiles": "my bigsmiles UPDATED"}]

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_material_node)


@pytest.mark.skip(reason="api")
def test_material_property_node_add(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_material.py::test_material_property_node_add
    """

    epoch_time = int(time.time())
    name_1 = f"my_proj_ali_{epoch_time}"
    mat_1 = f"my_mat__{epoch_time}"

    url_path = "/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"node": ["Material"], "name": mat_1, "property": [{"node": ["Property"], "key": "air_flow", "method": "prescribed", "type": "value"}]}]}

    try:
        create_response = cript_api._capsule_request(url_path=url_path, method="POST", data=json.dumps(create_payload))
        print(create_response)
    except Exception as e:
        print(e)

    print(create_response.json())
    cr_res_list = create_response.json()["data"]["result"]

    """
    1 - get existing material node by uuid - paginator
        - or create material node with a property

    2 - make an edit to a child node (property or process or component)
    3 - save the node
    """

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
                proj_uuid = item["uuid"]
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

        # add the properties to the material
        mat_loaded.property += [color]

        """
        1 - get existing material node by uuid - paginator
          - or create material node with a property

        2 - make an edit to a child node (property or process or component)
        3 - save the node
        """

        print("\n~~~~~~~~~~~~ SAVING NOW ~~~~~~~~~~~")
        print(mat_loaded)  # material_loaded
        # print(dir(mat_loaded))

        url_path = cript_api.save_node(mat_loaded)  # material_loaded

        # print("node_uuid: ", node_uuid)

        # payload = {"node": ["Material"], "property": [{"node": ["Property"], "key": "air_flow", "method": "chrom", "type": "value"}]}
        # # url1 = f"/material/{uuid}"

        url_path = url_path
        get_response = cript_api._capsule_request(url_path=url_path, method="GET")
        print("0~~0~~ \n")
        print(" get url_path: ", url_path)
        print(get_response.json())

        assert get_response.status_code == 200
        assert get_response.json()["data"]["result"][0]["node"] == ["Property"]

        # here delete the project thats created
        delete_url = f"/project/{proj_uuid}"
        del_response = cript_api._capsule_request(url_path=delete_url, method="DELETE")
        assert del_response.status_code == 200
        print("~~~~~~~~~~ WE GET HERE ? \n fine yes because get request for a material will not work unless material is public (this one is private), but you cannot delete a material that is public~~~~~~~~~~~~~~~~")

        quit()
        # cript_api.save_node(mat_loaded)  # material_loaded
        # print("\nBASICALLY now WE NEED TO ASSERT ON THE RESPONSE, WITH GET REQUEST EXCEPT ABOVE IS 😕 ")
        # print("\n-- probably need to fix save --\n---project after saved")

        # # get_url = f"/material/{uuid}"  # f"/project/{uuid}"

        # print("get_url1: ", get_url1)
        # url_path = f"/{mat_loaded.node[0].lower()}/{mat_loaded.uuid}"
        # print("url_path", url_path)
        # edited_result = cript_api._capsule_request(url_path=url_path, method="GET")
        # print("\n~~~~~~ saved reflected result")
        # print(edited_result.json())
        # assert len(edited_result.json()["data"]) == 1
        # final = edited_result.json()["data"][0]
        # assert len(final["property"]) == 2  # styrene and toluene
        # set1 = set([final["property"][0]["name"].lower(), final["property"][1]["name"].lower()])

        # quit()
        # set2 = set([json.loads(toluene.property.get_json().json)["name"].lower(), json.loads(styrene.property.get_json().json)["name"].lower()])
        # assert set1 == set2  # or material_003toluene.get_json().json)["name"]

        # print("\n___final")
        # print(final)
        # assert final["collection"][0]["name"] == json.loads(collection.get_json().json)["name"]
        # print("now deleting proj and eventually 2 mats")
        # print("only issue with this test is the toluene")

        # del_res = cript_api._capsule_request(url_path=f"/material/{uuid}", method="DELETE")
        # assert del_res.json()["code"] == 200


# @pytest.mark.skip(reason="api")
def test_material_property_node_change(cript_api) -> None:
    """
    pytest nodes/primary_nodes/test_material.py::test_material_property_node_change

    """

    epoch_time = int(time.time())
    name_1 = f"my_proj_ali_{epoch_time}"
    mat_1 = f"my_mat__{epoch_time}"

    url_path = "/project/"
    create_payload = {"node": ["Project"], "name": name_1, "material": [{"node": ["Material"], "name": mat_1, "property": [{"node": ["Property"], "key": "air_flow", "method": "prescribed", "type": "value"}]}]}

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
                item["uuid"]
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

        # print("node_uuid: ", node_uuid)

        # payload = {"node": ["Material"], "property": [{"node": ["Property"], "key": "air_flow", "method": "chrom", "type": "value"}]}
        # # url1 = f"/material/{uuid}"

        # url_path = url_path

        print("------````------`-`-`--`---")

        url_path1 = get_url1

        print("url_path1: ", url_path1)

        get_response = cript_api._capsule_request(url_path=url_path1, method="GET")
        print("\n___get_response")
        print(" get url_path: ", url_path1)
        print(get_response.json())

        assert get_response.status_code == 200
        assert get_response.json()["data"]["result"][0]["node"] == ["Property"]

        # here delete the project thats created
        # delete_url = f"/project/{proj_uuid}"
        # del_response = cript_api._capsule_request(url_path=delete_url, method="DELETE")
        # assert del_response.status_code == 200
        print("~~~~~~~~~~ WE GET HERE ? \n fine yes because get request for a material will not work unless material is public (this one is private), but you cannot delete a material that is public~~~~~~~~~~~~~~~~")

        quit()
