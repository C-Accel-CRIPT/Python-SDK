import json

import pytest

import cript


def test_create_simple_material() -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    my_identifiers = [{"alternative_names": "my material alternative name"}]

    material_name = "my material"

    my_material = cript.Material(name=material_name, identifiers=my_identifiers)

    assert my_material.identifiers == my_identifiers
    assert my_material.name == material_name


@pytest.fixture(scope="session")
def complex_material() -> None:
    """
    complex material fixture to use for other tests
    """

    my_identifier = [{"alternative_names": "my material alternative name"}]

    my_components = [
        cript.Material(name="my component material 1", identifiers=[{"alternative_names": "component 1 alternative name"}]),
        cript.Material(name="my component material 2", identifiers=[{"alternative_names": "component 2 alternative name"}]),
    ]

    # TODO fill in a real property type later
    my_properties = [cript.Property(key="air_flow", type="my property type", unit="gram", value=1.00)]

    my_process = cript.Process(type="affinity_pure", description="my simple material description", keywords=["anionic"])

    parent_material = cript.Material(name="my parent material", identifiers=[{"alternative_names": "parent material 1"}])

    my_computation_forcefield = cript.ComputationForcefield(key="amber", building_block="atom")

    my_material_keywords = ["acetylene"]

    # construct the full material node
    my_complex_material = cript.Material(
        name="my complex material",
        identifiers=my_identifier,
        components=my_components,
        properties=my_properties,
        process=my_process,
        parent_materials=parent_material,
        computation_forcefield=my_computation_forcefield,
        keywords=my_material_keywords,
    )

    # use complex material for other tests
    yield my_complex_material

    # reset the material to its original state
    my_complex_material.name = "my complex material"
    my_complex_material.identifiers = my_identifier
    my_complex_material.components = my_components
    my_complex_material.properties = my_properties
    my_complex_material.process = my_process
    my_complex_material.parent_materials = parent_material
    my_complex_material.computation_forcefield = my_computation_forcefield
    my_complex_material.keywords = my_material_keywords

    # check that the material attributes match the expected values
    # assert my_complex_material.name == "my complex material"
    # assert my_complex_material.identifiers == my_identifier
    # assert my_complex_material.components == my_components
    # assert my_complex_material.properties == my_properties
    # assert my_complex_material.process == my_process
    # assert my_complex_material.parent_materials == parent_material
    # assert my_complex_material.computation_forcefield == my_computation_forcefield
    # assert my_complex_material.keywords == my_material_keywords


@pytest.fixture(scope="session")
def simple_material() -> cript.Material:
    """
    tests that it can create a material node with only required arguments

    Returns
    -------
    Material
    """

    # create material
    my_material = cript.Material(name="my material", identifiers=[{"alternative_names": "my material alternative name"}])

    # use fixture in other tests
    yield my_material

    # reset material to original state
    my_material = my_material


def test_invalid_material_keywords() -> None:
    """
    tries to create a material with invalid keywords and expects to get an Exception
    """
    # with pytest.raises(InvalidVocabulary):
    pass


def test_all_getters_and_setters(simple_material) -> None:
    """
    tests the getters and setters for the simple material object

    1. sets every possible attribute for the simple_material object
    2. gets every possible attribute for the simple_material object
    3. asserts that what was set and what was gotten are the same
    """
    # new attributes
    new_name = "new material name"

    new_identifiers = [
        {"alternative_names": "my material alternative name"},
        {"preferred_name": "my preferred material name"},
    ]

    new_properties = [cript.Property(key="air_flow", type="modulus_shear", unit="gram", value=1.00)]

    new_process = [cript.Process(type="affinity_pure", description="my simple material description", keywords=["anionic"])]

    new_parent_material = cript.Material(name="my parent material", identifiers=[{"alternative_names": "parent material 1"}])

    new_computation_forcefield = cript.ComputationForcefield(key="amber", building_block="atom")

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(name="my component material 1", identifiers=[{"alternative_names": "component 1 alternative name"}]),
    ]

    # set all attributes for Material node
    simple_material.name = new_name
    simple_material.identifiers = new_identifiers
    simple_material.properties = new_properties
    simple_material.process = new_process
    simple_material.parent_materials = new_parent_material
    simple_material.computation_forcefield = new_computation_forcefield
    simple_material.keywords = new_material_keywords
    simple_material.components = new_components

    # get all attributes and assert that they are equal to the setter
    assert simple_material.name == new_name
    assert simple_material.identifiers == new_identifiers
    assert simple_material.properties == new_properties
    assert simple_material.process == new_process
    assert simple_material.parent_materials == new_parent_material
    assert simple_material.computation_forcefield == new_computation_forcefield
    assert simple_material.keywords == new_material_keywords
    assert simple_material.components == new_components


def test_serialize_material_to_json(complex_material) -> None:
    """
    tests that it can correctly turn the material node into its equivalent JSON
    """
    # the JSON that the material should serialize to
    expected_dict = {
        "node": "Material",
        "name": "my complex material",
        "identifiers": [{"alternative_names": "my material alternative name"}],
        "components": [
            {
                "node": "Material",
                "name": "my component material 1",
                "identifiers": [{"alternative_names": "component 1 alternative name"}],
            },
            {
                "node": "Material",
                "name": "my component material 2",
                "identifiers": [{"alternative_names": "component 2 alternative name"}],
            },
        ],
        "properties": [
            {
                "node": "Property",
                "key": "air_flow",
                "type": "my property type",
                "value": 1.0,
                "unit": "gram",
            }
        ],
        "process": {
            "node": "Process",
            "type": "affinity_pure",
            "description": "my simple material description",
            "keywords": ["anionic"],
        },
        "parent_materials": {
            "node": "Material",
            "name": "my parent material",
            "identifiers": [{"alternative_names": "parent material 1"}],
        },
        "computation_forcefield": {
            "node": "ComputationForcefield",
            "key": "amber",
            "building_block": "atom",
        },
        "keywords": ["acetylene"],
    }

    # convert JSON str to dict for better comparison
    expected_json = json.dumps(expected_dict, sort_keys=True)
    assert complex_material.json == expected_json


# ---------- Integration Tests ----------
def test_save_material_to_api() -> None:
    """
    tests if the material can be saved to the API without errors and status code of 200
    """
    pass


def test_get_material_from_api() -> None:
    """
    integration test: gets the material from the api that was saved prior
    """
    pass


def test_deserialize_material_from_json() -> None:
    """
    tests that a JSON of a material node can be correctly converted to python object
    """
    api_material = {
        "name": "my cool material",
        "component_count": 0,
        "computational_forcefield_count": 0,
        "created_at": "2023-03-14T00:45:02.196297Z",
        "identifier_count": 0,
        "identifiers": [],
        "model_version": "1.0.0",
        "node": "Material",
        "notes": "",
        "property_count": 0,
        "uid": "0x24a08",
        "updated_at": "2023-03-14T00:45:02.196276Z",
        "uuid": "403fa02c-9a84-4f9e-903c-35e535151b08",
    }

    material_string = json.dumps(api_material)
    print(material_string)
    my_material = cript.load_nodes_from_json(nodes_json=material_string)
    print(type(my_material))

    # assertions
    assert isinstance(my_material, cript.Material)
    assert my_material.name == api_material["name"]
    assert my_material.identifiers == []
    assert my_material.components == []
    assert my_material.properties == []
    assert my_material.process == []
    assert my_material.parent_materials == []
    assert my_material.computation_forcefield == []
    assert my_material.keywords == []
    assert my_material.notes == api_material["notes"]


def test_update_material_to_api() -> None:
    """
    tests that the material can be correctly updated within the API
    """
    pass


def test_delete_material_from_api() -> None:
    """
    integration test: tests that the material can be deleted correctly from the API
    tries to get the material from API, and it is expected for the API to give an error response
    """
    pass
