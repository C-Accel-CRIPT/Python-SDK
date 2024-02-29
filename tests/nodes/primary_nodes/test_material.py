import json
import uuid

import cript
from tests.utils.integration_test_helper import (
    delete_integration_node_helper,
    save_integration_node_helper,
)
from tests.utils.util import strip_uid_from_dict


def test_create_complex_material(simple_material_node, simple_computational_forcefield_node, simple_process_node) -> None:
    """
    tests that a simple material can be created with only the required arguments
    """

    material_name = "my material name"
    keyword = ["acetylene"]
    material_notes = "my material notes"

    amino_acid = "adenosine"
    bigsmiles = "NC{[$][$]CC[$][]}"
    chem_formula = "NC5"
    chem_repeat = ["CC"]
    chemical_id = "my chemid"
    inchi = "my inchi"
    lot_number = "lot 1"
    names = ["polyethylene"]
    pubchem_cid = 155
    smiles = "*CC*"
    vendor = "my vendor"

    component = [simple_material_node]
    forcefield = [simple_computational_forcefield_node]

    my_property = [cript.Property(key="modulus_shear", type="min", value=1.23, unit="gram")]

    my_material = cript.Material(
        name=material_name,
        keyword=keyword,
        component=component,
        process=simple_process_node,
        property=my_property,
        computational_forcefield=forcefield,
        notes=material_notes,
        amino_acid=amino_acid,
        bigsmiles=bigsmiles,
        chem_formula=chem_formula,
        chemical_id=chemical_id,
        inchi=inchi,
        lot_number=lot_number,
        names=names,
        pubchem_cid=pubchem_cid,
        smiles=smiles,
        vendor=vendor,
    )

    assert isinstance(my_material, cript.Material)
    assert my_material.name == material_name
    assert my_material.keyword == keyword
    assert my_material.component == component
    assert my_material.process == simple_process_node
    assert my_material.property == my_property
    assert my_material.computational_forcefield == forcefield
    assert my_material.notes == material_notes
    assert my_material.amino_acid == amino_acid
    assert my_material.bigsmiles == bigsmiles
    assert my_material.chem_formula == chem_formula
    assert my_material.chem_repeat == chem_repeat
    assert my_material.chemical_id == chemical_id
    assert my_material.inchi == inchi
    assert my_material.lot_number == lot_number
    assert my_material.names == names
    assert my_material.pubchem_cid == pubchem_cid
    assert my_material.smiles == smiles
    assert my_material.vendor == vendor


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

    new_parent_material = cript.Material(
        name="my parent material",
    )

    new_material_keywords = ["acetylene"]

    new_components = [
        cript.Material(
            name="my component material 1",
        ),
    ]

    amino_acid = "adenosine"
    bigsmiles = "NC{[$][$]CC[$][]}"
    chem_formula = "NC5"
    chem_repeat = ["CC"]
    chemical_id = "my chemid"
    inchi = "my inchi"
    lot_number = "lot 1"
    names = ["polyethylene"]
    pubchem_cid = 155
    smiles = "*CC*"
    vendor = "my vendor"

    # set all attributes for Material node
    simple_material_node.name = new_name
    simple_material_node.property = [simple_property_node]
    simple_material_node.parent_material = new_parent_material
    simple_material_node.computational_forcefield = simple_computational_forcefield_node
    simple_material_node.keyword = new_material_keywords
    simple_material_node.component = new_components
    simple_material_node.notes = new_notes
    simple_material_node.amino_acid = amino_acid
    simple_material_node.bigsmiles = bigsmiles
    simple_material_node.chem_formula = chem_formula
    simple_material_node.chem_repeat = chem_repeat
    simple_material_node.chemical_id = chemical_id
    simple_material_node.inchi = inchi
    simple_material_node.lot_number = lot_number
    simple_material_node.names = names
    simple_material_node.pubchem_cid = pubchem_cid
    simple_material_node.smiles = smiles
    simple_material_node.vendor = vendor

    # get all attributes and assert that they are equal to the setter
    assert simple_material_node.name == new_name
    assert simple_material_node.property == [simple_property_node]
    assert simple_material_node.parent_material == new_parent_material
    assert simple_material_node.computational_forcefield == simple_computational_forcefield_node
    assert simple_material_node.keyword == new_material_keywords
    assert simple_material_node.component == new_components
    assert simple_material_node.notes == new_notes
    assert simple_material_node.amino_acid == amino_acid
    assert simple_material_node.bigsmiles == bigsmiles
    assert simple_material_node.chem_formula == chem_formula
    assert simple_material_node.chem_repeat == chem_repeat
    assert simple_material_node.chemical_id == chemical_id
    assert simple_material_node.inchi == inchi
    assert simple_material_node.lot_number == lot_number
    assert simple_material_node.names == names
    assert simple_material_node.pubchem_cid == pubchem_cid
    assert simple_material_node.smiles == smiles
    assert simple_material_node.vendor == vendor

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
    simple_project_node.material[0].bigsmiles = "CC{[$][$]CC[$][]} UPDATED"

    save_integration_node_helper(cript_api=cript_api, project_node=simple_project_node)

    # ========= test delete =========
    delete_integration_node_helper(cript_api=cript_api, node_to_delete=simple_material_node)
