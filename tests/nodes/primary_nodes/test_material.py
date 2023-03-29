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


def test_create_complex_material() -> None:
    """
    tests that a material can be created with all optional arguments
    """

    my_identifier = [{"alternative_names": "my material alternative name"}]

    my_components = [
        cript.Material(name="my component material 1",
                       identifiers=[{"alternative_names": "component 1 alternative name"}]),
        cript.Material(name="my component material 2",
                       identifiers=[{"alternative_names": "component 2 alternative name"}]),
    ]

    # TODO fill in a real property type later
    my_properties = [cript.Property(key="air_flow", type="my property type", unit="gram", value=1.00)]

    my_process = cript.Process(type="affinity_pure", description="my simple material description", keywords=["anionic"])

    parent_material = cript.Material(name="my parent material",
                                     identifiers=[{"alternative_names": "parent material 1"}])

    my_computation_forcefield = cript.ComputationForcefield(key="amber", building_block="atom")

    my_material_keywords = ["acetylene"]

    # construct the full material node
    my_material = cript.Material(
        name="my complex material",
        identifiers=my_identifier,
        components=my_components,
        properties=my_properties,
        process=my_process,
        parent_materials=parent_material,
        computation_forcefield=my_computation_forcefield,
        keywords=my_material_keywords,
    )

    # check that the material attributes match the expected values
    assert my_material.name == "my complex material"
    assert my_material.identifiers == my_identifier
    assert my_material.components == my_components
    assert my_material.properties == my_properties
    assert my_material.process == my_process
    assert my_material.parent_materials == parent_material
    assert my_material.computation_forcefield == my_computation_forcefield
    assert my_material.keywords == my_material_keywords


@pytest.fixture(scope="session")
def simple_material() -> cript.Material:
    """
    tests that it can create a material node with only required arguments

    Returns
    -------
    Material
    """

    # create material
    my_material = cript.Material(name="my material",
                                 identifiers=[{"alternative_names": "my material alternative name"}])

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

    new_properties = [
        cript.Property(key="air_flow", type="modulus_shear", unit="gram", value=1.00)
    ]

    new_process = [cript.Process(type="affinity_pure", description="my simple material description", keywords=["anionic"])]

    new_parent_material = cript.Material(name="my parent material",
                                     identifiers=[{"alternative_names": "parent material 1"}])

    new_computation_forcefield = cript.ComputationForcefield(key="amber", building_block="atom")

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(name="my component material 1",
                       identifiers=[{"alternative_names": "component 1 alternative name"}]),
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


def test_serialize_material_to_json() -> None:
    """
    tests that it can correctly turn the material node into its equivalent JSON
    """
    material_dict: dict = {"node": "Material", "name": "my material"}


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
    pass


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
