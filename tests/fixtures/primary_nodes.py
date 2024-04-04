import copy
import json
import uuid

import pytest

import cript
from tests.utils.util import strip_uid_from_dict


@pytest.fixture(scope="function")
def simple_project_node(simple_collection_node) -> cript.Project:
    """
    create a minimal Project node with only required arguments for other tests to use

    Returns
    -------
    cript.Project
    """

    return cript.Project(name="my Project name", collection=[simple_collection_node])


@pytest.fixture(scope="function")
def complex_project_dict(complex_collection_node, simple_material_node, complex_user_node) -> dict:
    project_dict = {"node": ["Project"]}
    project_dict["locked"] = True
    project_dict["model_version"] = "1.0.0"
    project_dict["updated_by"] = json.loads(copy.deepcopy(complex_user_node).get_expanded_json())
    project_dict["created_by"] = json.loads(complex_user_node.get_expanded_json())
    project_dict["public"] = True
    project_dict["name"] = "my project name"
    project_dict["notes"] = "my project notes"
    project_dict["member"] = [json.loads(complex_user_node.get_expanded_json())]
    project_dict["admin"] = [json.loads(complex_user_node.get_expanded_json())]
    project_dict["collection"] = [json.loads(complex_collection_node.get_expanded_json())]
    project_dict["material"] = [json.loads(copy.deepcopy(simple_material_node).get_expanded_json())]
    return project_dict


@pytest.fixture(scope="function")
def complex_project_node(complex_project_dict) -> cript.Project:
    """
    a complex Project node that includes all possible optional arguments that are themselves complex as well
    """
    complex_project = cript.load_nodes_from_json(json.dumps(complex_project_dict))
    return complex_project


@pytest.fixture(scope="function")
def fixed_cyclic_project_node() -> cript.Project:
    project_json_string: str = "{\n"
    project_json_string += '"node": ["Project"],\n'
    project_json_string += '"uid": "_:0e487131-1dbf-4c6c-9ee0-650df148b06e",\n'
    project_json_string += '"uuid": "55a41f23-4791-4dc7-bf2c-48fd2b6fc90b",\n'
    project_json_string += '"updated_by": {\n'
    project_json_string += '"node": ["User"],\n'
    project_json_string += '"uid": "_:5838e9cc-f01d-468e-96de-93bfe6fb758f",\n'
    project_json_string += '"uuid": "5838e9cc-f01d-468e-96de-93bfe6fb758f",\n'
    project_json_string += '"created_at": "2024-03-12 15:58:12.486673",\n'
    project_json_string += '"updated_at": "2024-03-12 15:58:12.486681",\n'
    project_json_string += '"email": "test@emai.com",\n'
    project_json_string += '"model_version": "1.0.0",\n'
    project_json_string += '"orcid": "0000-0002-0000-0000",\n'
    project_json_string += '"picture": "/my/picture/path",\n'
    project_json_string += '"username": "testuser"\n'
    project_json_string += "},\n"
    project_json_string += '"created_by": {\n'
    project_json_string += '"node": ["User"],\n'
    project_json_string += '"uid": "_:2bb1fc16-6e72-480d-a3df-b74eac4d32e8",\n'
    project_json_string += '"uuid": "ab385d26-6ee5-40d4-9095-2d623616a162",\n'
    project_json_string += '"created_at": "2024-03-12 15:58:12.486673",\n'
    project_json_string += '"updated_at": "2024-03-12 15:58:12.486681",\n'
    project_json_string += '"email": "test@emai.com",\n'
    project_json_string += '"model_version": "1.0.0",\n'
    project_json_string += '"orcid": "0000-0002-0000-0000",\n'
    project_json_string += '"picture": "/my/picture/path",\n'
    project_json_string += '"username": "testuser"\n'
    project_json_string += "},\n"
    project_json_string += '"locked": true,\n'
    project_json_string += '"model_version": "1.0.0",\n'
    project_json_string += '"public": true,\n'
    project_json_string += '"name": "my project name",\n'
    project_json_string += '"notes": "my project notes",\n'
    project_json_string += '"member": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:2bb1fc16-6e72-480d-a3df-b74eac4d32e8"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"admin": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:2bb1fc16-6e72-480d-a3df-b74eac4d32e8"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"collection": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Collection"],\n'
    project_json_string += '"uid": "_:61a99328-108b-4307-bfcb-fccd12a5dd91",\n'
    project_json_string += '"uuid": "61a99328-108b-4307-bfcb-fccd12a5dd91",\n'
    project_json_string += '"name": "my complex collection name",\n'
    project_json_string += '"experiment": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Experiment"],\n'
    project_json_string += '"uid": "_:d2b3169d-c200-4143-811a-a0d07439dd96",\n'
    project_json_string += '"uuid": "d2b3169d-c200-4143-811a-a0d07439dd96",\n'
    project_json_string += '"name": "my experiment name",\n'
    project_json_string += '"process": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Process"],\n'
    project_json_string += '"uid": "_:5d649b93-8f2c-4509-9aa7-311213df9405",\n'
    project_json_string += '"uuid": "5d649b93-8f2c-4509-9aa7-311213df9405",\n'
    project_json_string += '"name": "my process name",\n'
    project_json_string += '"type": "affinity_pure",\n'
    project_json_string += '"ingredient": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Ingredient"],\n'
    project_json_string += '"uid": "_:21601ad5-c225-4626-8baa-3a7c1d64cafa",\n'
    project_json_string += '"uuid": "21601ad5-c225-4626-8baa-3a7c1d64cafa",\n'
    project_json_string += '"material": {\n'
    project_json_string += '"node": ["Material"],\n'
    project_json_string += '"uid": "_:ea9ad3e7-84a7-475f-82a8-16f5b9241e37",\n'
    project_json_string += '"uuid": "ea9ad3e7-84a7-475f-82a8-16f5b9241e37",\n'
    project_json_string += '"name": "my test material 9221be1d-247c-4f67-8a0a-fe1ec657705b",\n'
    project_json_string += '"property": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Property"],\n'
    project_json_string += '"uid": "_:fc504202-6fdd-43c7-830d-40c7d3f0cb8c",\n'
    project_json_string += '"uuid": "fc504202-6fdd-43c7-830d-40c7d3f0cb8c",\n'
    project_json_string += '"key": "modulus_shear",\n'
    project_json_string += '"type": "value",\n'
    project_json_string += '"value": 5.0,\n'
    project_json_string += '"unit": "GPa",\n'
    project_json_string += '"computation": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Computation"],\n'
    project_json_string += '"uid": "_:175708fa-cc29-4442-be7f-adf85e995330",\n'
    project_json_string += '"uuid": "175708fa-cc29-4442-be7f-adf85e995330",\n'
    project_json_string += '"name": "my computation name",\n'
    project_json_string += '"type": "analysis",\n'
    project_json_string += '"input_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Data"],\n'
    project_json_string += '"uid": "_:dcb516a1-951d-461a-beb6-bdf2aecd0778",\n'
    project_json_string += '"uuid": "dcb516a1-951d-461a-beb6-bdf2aecd0778",\n'
    project_json_string += '"name": "my data name",\n'
    project_json_string += '"type": "afm_amp",\n'
    project_json_string += '"file": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["File"],\n'
    project_json_string += '"uid": "_:c94aba31-adf2-4eeb-b51e-8c70568c2eb0",\n'
    project_json_string += '"uuid": "c94aba31-adf2-4eeb-b51e-8c70568c2eb0",\n'
    project_json_string += '"name": "my complex file node fixture",\n'
    project_json_string += '"source": "https://criptapp.org",\n'
    project_json_string += '"type": "calibration",\n'
    project_json_string += '"extension": ".csv",\n'
    project_json_string += '"data_dictionary": "my file\'s data dictionary"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"output_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Data"],\n'
    project_json_string += '"uid": "_:6a2e81af-861b-4c66-96fd-b969a38b81b1",\n'
    project_json_string += '"uuid": "6a2e81af-861b-4c66-96fd-b969a38b81b1",\n'
    project_json_string += '"name": "my data name",\n'
    project_json_string += '"type": "afm_amp",\n'
    project_json_string += '"file": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["File"],\n'
    project_json_string += '"uid": "_:ce01ba93-cfc5-4265-a6d6-8c38397deb43",\n'
    project_json_string += '"uuid": "ce01ba93-cfc5-4265-a6d6-8c38397deb43",\n'
    project_json_string += '"name": "my complex file node fixture",\n'
    project_json_string += '"source": "https://criptapp.org",\n'
    project_json_string += '"type": "calibration",\n'
    project_json_string += '"extension": ".csv",\n'
    project_json_string += '"data_dictionary": "my file\'s data dictionary"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"node": ["Computation"],\n'
    project_json_string += '"uid": "_:1aa11462-b394-4c35-906e-d0e9198be6da",\n'
    project_json_string += '"uuid": "1aa11462-b394-4c35-906e-d0e9198be6da",\n'
    project_json_string += '"name": "my computation name",\n'
    project_json_string += '"type": "analysis",\n'
    project_json_string += '"input_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:dcb516a1-951d-461a-beb6-bdf2aecd0778"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"output_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:6a2e81af-861b-4c66-96fd-b969a38b81b1"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"parent_material": {\n'
    project_json_string += '"node": ["Material"],\n'
    project_json_string += '"uid": "_:2ee56671-5efb-4f99-a7ea-d659f5b5dd9a",\n'
    project_json_string += '"uuid": "2ee56671-5efb-4f99-a7ea-d659f5b5dd9a",\n'
    project_json_string += '"name": "my test material 9221be1d-247c-4f67-8a0a-fe1ec657705b",\n'
    project_json_string += '"process": {\n'
    project_json_string += '"uid": "_:5d649b93-8f2c-4509-9aa7-311213df9405"\n'
    project_json_string += "},\n"
    project_json_string += '"property": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Property"],\n'
    project_json_string += '"uid": "_:fde629f5-8d3a-4546-8cd3-9de63b990187",\n'
    project_json_string += '"uuid": "fde629f5-8d3a-4546-8cd3-9de63b990187",\n'
    project_json_string += '"key": "modulus_shear",\n'
    project_json_string += '"type": "value",\n'
    project_json_string += '"value": 5.0,\n'
    project_json_string += '"unit": "GPa",\n'
    project_json_string += '"computation": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Computation"],\n'
    project_json_string += '"uid": "_:2818ed85-2758-45f9-9f30-5c3dfedd3d33",\n'
    project_json_string += '"uuid": "2818ed85-2758-45f9-9f30-5c3dfedd3d33",\n'
    project_json_string += '"name": "my computation name",\n'
    project_json_string += '"type": "analysis",\n'
    project_json_string += '"input_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Data"],\n'
    project_json_string += '"uid": "_:0a88e09d-488f-45ed-ad9c-14873792b8fd",\n'
    project_json_string += '"uuid": "0a88e09d-488f-45ed-ad9c-14873792b8fd",\n'
    project_json_string += '"name": "my data name",\n'
    project_json_string += '"type": "afm_amp",\n'
    project_json_string += '"file": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["File"],\n'
    project_json_string += '"uid": "_:1fc95012-2845-46ac-a8e3-7178fe19afcd",\n'
    project_json_string += '"uuid": "1fc95012-2845-46ac-a8e3-7178fe19afcd",\n'
    project_json_string += '"name": "my complex file node fixture",\n'
    project_json_string += '"source": "https://criptapp.org",\n'
    project_json_string += '"type": "calibration",\n'
    project_json_string += '"extension": ".csv",\n'
    project_json_string += '"data_dictionary": "my file\'s data dictionary"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"output_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Data"],\n'
    project_json_string += '"uid": "_:309b0d7b-027c-4422-ab5f-58069fe4adb1",\n'
    project_json_string += '"uuid": "309b0d7b-027c-4422-ab5f-58069fe4adb1",\n'
    project_json_string += '"name": "my data name",\n'
    project_json_string += '"type": "afm_amp",\n'
    project_json_string += '"file": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["File"],\n'
    project_json_string += '"uid": "_:e78cf3cf-de6c-4364-93c4-4fb3d352bde2",\n'
    project_json_string += '"uuid": "e78cf3cf-de6c-4364-93c4-4fb3d352bde2",\n'
    project_json_string += '"name": "my complex file node fixture",\n'
    project_json_string += '"source": "https://criptapp.org",\n'
    project_json_string += '"type": "calibration",\n'
    project_json_string += '"extension": ".csv",\n'
    project_json_string += '"data_dictionary": "my file\'s data dictionary"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"node": ["Computation"],\n'
    project_json_string += '"uid": "_:09cf72a4-a397-4953-baa6-7cdf5be067c4",\n'
    project_json_string += '"uuid": "09cf72a4-a397-4953-baa6-7cdf5be067c4",\n'
    project_json_string += '"name": "my computation name",\n'
    project_json_string += '"type": "analysis",\n'
    project_json_string += '"input_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:0a88e09d-488f-45ed-ad9c-14873792b8fd"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"output_data": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:309b0d7b-027c-4422-ab5f-58069fe4adb1"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"bigsmiles": "{[][$]COC[$][]}"\n'
    project_json_string += "},\n"
    project_json_string += '"bigsmiles": "{[][$]COC[$][]}"\n'
    project_json_string += "}\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"product": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:ea9ad3e7-84a7-475f-82a8-16f5b9241e37"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"computation": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:2818ed85-2758-45f9-9f30-5c3dfedd3d33"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:09cf72a4-a397-4953-baa6-7cdf5be067c4"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:175708fa-cc29-4442-be7f-adf85e995330"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:1aa11462-b394-4c35-906e-d0e9198be6da"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"data": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:0a88e09d-488f-45ed-ad9c-14873792b8fd"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:309b0d7b-027c-4422-ab5f-58069fe4adb1"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:dcb516a1-951d-461a-beb6-bdf2aecd0778"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"uid": "_:6a2e81af-861b-4c66-96fd-b969a38b81b1"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"inventory": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Inventory"],\n'
    project_json_string += '"uid": "_:1ff50987-e0a2-4aa3-a1a2-bdcefd54693d",\n'
    project_json_string += '"uuid": "1ff50987-e0a2-4aa3-a1a2-bdcefd54693d",\n'
    project_json_string += '"name": "my inventory name",\n'
    project_json_string += '"material": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:ea9ad3e7-84a7-475f-82a8-16f5b9241e37"\n'
    project_json_string += "},\n"
    project_json_string += "{\n"
    project_json_string += '"node": ["Material"],\n'
    project_json_string += '"uid": "_:845c90c1-5a93-416f-9c42-1bac1de0bd9a",\n'
    project_json_string += '"uuid": "845c90c1-5a93-416f-9c42-1bac1de0bd9a",\n'
    project_json_string += '"name": "material 2 730f2483-f018-4583-82d3-beb27947d470",\n'
    project_json_string += '"process": {\n'
    project_json_string += '"uid": "_:5d649b93-8f2c-4509-9aa7-311213df9405"\n'
    project_json_string += "},\n"
    project_json_string += '"property": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:fc504202-6fdd-43c7-830d-40c7d3f0cb8c"\n'
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"bigsmiles": "{[][$]COC[$][]}"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"doi": "10.1038/1781168a0",\n'
    project_json_string += '"citation": [\n'
    project_json_string += "{\n"
    project_json_string += '"node": ["Citation"],\n'
    project_json_string += '"uid": "_:1232d7be-d870-4357-bf41-f53a09707cca",\n'
    project_json_string += '"uuid": "1232d7be-d870-4357-bf41-f53a09707cca",\n'
    project_json_string += '"type": "reference",\n'
    project_json_string += '"reference": {\n'
    project_json_string += '"node": ["Reference"],\n'
    project_json_string += '"uid": "_:3fb7801f-7253-4d6b-813b-f1d2d25b6316",\n'
    project_json_string += '"uuid": "3fb7801f-7253-4d6b-813b-f1d2d25b6316",\n'
    project_json_string += '"type": "journal_article",\n'
    project_json_string += '"title": "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: SOft coarse grained Monte-Carlo Acceleration (SOMA)",\n'
    project_json_string += '"author": ["Ludwig Schneider", "Marcus M\u00fcller"],\n'
    project_json_string += '"journal": "Computer Physics Communications",\n'
    project_json_string += '"publisher": "Elsevier",\n'
    project_json_string += '"year": 2019,\n'
    project_json_string += '"pages": [463, 476],\n'
    project_json_string += '"doi": "10.1016/j.cpc.2018.08.011",\n'
    project_json_string += '"issn": "0010-4655",\n'
    project_json_string += '"website": "https://www.sciencedirect.com/science/article/pii/S0010465518303072"\n'
    project_json_string += "}\n"
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"
    project_json_string += "],\n"
    project_json_string += '"material": [\n'
    project_json_string += "{\n"
    project_json_string += '"uid": "_:2ee56671-5efb-4f99-a7ea-d659f5b5dd9a"\n'
    project_json_string += "}\n"
    project_json_string += "]\n"
    project_json_string += "}\n"

    return cript.load_nodes_from_json(project_json_string)


@pytest.fixture(scope="function")
def fixed_cyclic_project_dfs_uuid_order():
    expected_list = [
        "55a41f23-4791-4dc7-bf2c-48fd2b6fc90b",
        "ab385d26-6ee5-40d4-9095-2d623616a162",
        "61a99328-108b-4307-bfcb-fccd12a5dd91",
        "1232d7be-d870-4357-bf41-f53a09707cca",
        "3fb7801f-7253-4d6b-813b-f1d2d25b6316",
        "d2b3169d-c200-4143-811a-a0d07439dd96",
        "2818ed85-2758-45f9-9f30-5c3dfedd3d33",
        "0a88e09d-488f-45ed-ad9c-14873792b8fd",
        "1fc95012-2845-46ac-a8e3-7178fe19afcd",
        "309b0d7b-027c-4422-ab5f-58069fe4adb1",
        "e78cf3cf-de6c-4364-93c4-4fb3d352bde2",
        "09cf72a4-a397-4953-baa6-7cdf5be067c4",
        "175708fa-cc29-4442-be7f-adf85e995330",
        "dcb516a1-951d-461a-beb6-bdf2aecd0778",
        "c94aba31-adf2-4eeb-b51e-8c70568c2eb0",
        "6a2e81af-861b-4c66-96fd-b969a38b81b1",
        "ce01ba93-cfc5-4265-a6d6-8c38397deb43",
        "1aa11462-b394-4c35-906e-d0e9198be6da",
        "5d649b93-8f2c-4509-9aa7-311213df9405",
        "21601ad5-c225-4626-8baa-3a7c1d64cafa",
        "ea9ad3e7-84a7-475f-82a8-16f5b9241e37",
        "2ee56671-5efb-4f99-a7ea-d659f5b5dd9a",
        "fde629f5-8d3a-4546-8cd3-9de63b990187",
        "fc504202-6fdd-43c7-830d-40c7d3f0cb8c",
        "1ff50987-e0a2-4aa3-a1a2-bdcefd54693d",
        "845c90c1-5a93-416f-9c42-1bac1de0bd9a",
        "5838e9cc-f01d-468e-96de-93bfe6fb758f",
    ]
    return expected_list


@pytest.fixture(scope="function")
def simple_collection_node(simple_experiment_node) -> cript.Collection:
    """
    create a simple collection node for other tests to be able to easily and cleanly reuse

    Notes
    -----
    * [Collection](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=8)
    has no required attributes.
    * The Python SDK only requires Collections to have `name`
        * Since it doesn't make sense to have an empty Collection I added an Experiment to the Collection as well
    """
    my_collection_name = "my collection name"

    my_collection = cript.Collection(name=my_collection_name, experiment=[simple_experiment_node])

    return my_collection


@pytest.fixture(scope="function")
def complex_collection_node(simple_experiment_node, simple_inventory_node, complex_citation_node) -> cript.Collection:
    """
    Collection node with all optional arguments
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

    return my_collection


@pytest.fixture(scope="function")
def simple_experiment_node() -> cript.Experiment:
    """
    minimal experiment node to use for other tests

    Returns
    -------
    Experiment
    """

    return cript.Experiment(name="my experiment name")


@pytest.fixture(scope="function")
def simple_computation_process_node(complex_ingredient_node, simple_data_node) -> cript.ComputationProcess:
    """
    simple Computational Process node with only required arguments to use in other tests
    """
    my_computational_process_type = "cross_linking"

    my_computational_process = cript.ComputationProcess(
        name="my computational process name",
        type=my_computational_process_type,
        input_data=[copy.deepcopy(simple_data_node)],
        ingredient=[complex_ingredient_node],
    )

    return my_computational_process


@pytest.fixture(scope="function")
def simple_data_node(complex_file_node) -> cript.Data:
    """
    minimal data node
    """
    my_data = cript.Data(name="my data name", type="afm_amp", file=[complex_file_node])

    return my_data


@pytest.fixture(scope="function")
def complex_data_node(
    complex_file_node,
    simple_process_node,
    simple_computation_node,
    simple_computation_process_node,
    simple_material_node,
    complex_citation_node,
) -> None:
    """
    create a complex data node with all possible arguments for all tests to use when needed
    """
    my_complex_data = cript.Data(
        name="my complex data node name",
        type="afm_amp",
        file=[copy.deepcopy(complex_file_node)],
        sample_preparation=copy.deepcopy(simple_process_node),
        computation=[simple_computation_node],
        computation_process=[simple_computation_process_node],
        material=[simple_material_node],
        process=[copy.deepcopy(simple_process_node)],
        citation=[copy.deepcopy(complex_citation_node)],
    )

    return my_complex_data


@pytest.fixture(scope="function")
def simple_process_node() -> cript.Process:
    """
    simple process node to use in other tests to keep tests clean
    """
    my_process = cript.Process(name="my process name", type="affinity_pure")

    return my_process


@pytest.fixture(scope="function")
def complex_process_node(complex_ingredient_node, simple_equipment_node, complex_citation_node, simple_property_node, simple_condition_node, simple_material_node, simple_process_node) -> None:
    """
    create a process node with all possible arguments

    Notes
    -----
    * indirectly tests the vocabulary as well, as it gives it valid vocabulary
    """

    my_process_name = "my complex process node name"
    my_process_type = "affinity_pure"
    my_process_description = "my simple material description"

    process_waste = [
        cript.Material(name="my process waste material 1", bigsmiles="CC{[$][$]COC[$][]}"),
    ]

    my_process_keywords = [
        "anionic",
        "annealing_sol",
    ]

    my_complex_process = cript.Process(
        name=my_process_name,
        type=my_process_type,
        ingredient=[complex_ingredient_node],
        description=my_process_description,
        equipment=[simple_equipment_node],
        product=[simple_material_node],
        waste=process_waste,
        prerequisite_process=[simple_process_node],
        condition=[simple_condition_node],
        property=[simple_property_node],
        keyword=my_process_keywords,
        citation=[complex_citation_node],
    )

    return my_complex_process


@pytest.fixture(scope="function")
def simple_computation_node() -> cript.Computation:
    """
    simple computation node to use between tests
    """
    my_computation = cript.Computation(name="my computation name", type="analysis")

    return my_computation


@pytest.fixture(scope="function")
def simple_material_node() -> cript.Material:
    """
    simple material node to use between tests
    """
    # Use a unique name
    my_material = cript.Material(name="my test material " + str(uuid.uuid4()), bigsmiles="{[][$]COC[$][]}")

    return my_material


@pytest.fixture(scope="function")
def simple_material_dict() -> dict:
    """
    the dictionary that `simple_material_node` produces
    putting it in one location to make updating it easy
    """
    simple_material_dict: dict = {"node": ["Material"], "name": "my material", "bigsmiles": "{[][$]COC[$][]}"}

    return simple_material_dict


@pytest.fixture(scope="function")
def complex_material_dict(simple_property_node, simple_process_node, complex_computational_forcefield_node, simple_material_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_material_keyword = ["acetylene"]

    material_dict = {"node": ["Material"]}
    material_dict["name"] = "my complex material"
    material_dict["property"] = [json.loads(simple_property_node.get_expanded_json())]
    material_dict["process"] = json.loads(simple_process_node.get_expanded_json())
    material_dict["parent_material"] = json.loads(simple_material_node.get_expanded_json())
    material_dict["computational_forcefield"] = json.loads(complex_computational_forcefield_node.get_expanded_json())
    material_dict["bigsmiles"] = "{[][$]CC[$][]}"
    material_dict["keyword"] = my_material_keyword

    return strip_uid_from_dict(material_dict)


@pytest.fixture(scope="function")
def complex_material_node(simple_property_node, simple_process_node, complex_computational_forcefield_node, simple_material_node) -> cript.Material:
    """
    complex Material node with all possible attributes filled
    """
    my_material_keyword = ["acetylene"]

    my_complex_material = cript.Material(
        name="my complex material",
        bigsmiles="{[][$]CC[$][]}",
        property=[simple_property_node],
        process=copy.deepcopy(simple_process_node),
        parent_material=simple_material_node,
        computational_forcefield=complex_computational_forcefield_node,
        keyword=my_material_keyword,
    )

    return my_complex_material


@pytest.fixture(scope="function")
def simple_inventory_node(simple_material_node) -> None:
    """
    minimal inventory node to use for other tests
    """
    # set up inventory node

    material_2 = cript.Material(name="material 2 " + str(uuid.uuid4()), bigsmiles="{[][$]COC[$][]}")

    my_inventory = cript.Inventory(name="my inventory name", material=[])  # material=[simple_material_node, material_2])

    # my_inventory.material = []

    # use my_inventory in another test
    return my_inventory


@pytest.fixture(scope="function")
def simple_computational_process_node(simple_data_node, complex_ingredient_node) -> None:
    """
    simple/minimal computational_process node with only required arguments
    """
    my_computational_process = cript.ComputationProcess(
        name="my computational process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredient=[complex_ingredient_node],
    )

    return my_computational_process


@pytest.fixture(scope="function")
def simplest_computational_process_node(simple_data_node, simple_ingredient_node) -> cript.ComputationProcess:
    """
    minimal computational_process node
    """
    my_simplest_computational_process = cript.ComputationProcess(
        name="my computational process node name",
        type="cross_linking",
        input_data=[simple_data_node],
        ingredient=[simple_ingredient_node],
    )

    return my_simplest_computational_process
