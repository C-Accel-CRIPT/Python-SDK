import json

import pytest

import cript
from cript.api.exceptions import InvalidVocabulary
from cript.nodes.exceptions import CRIPTNodeSchemaError


def test_get_db_schema_from_api(cript_api: cript.API) -> None:
    """
    tests that the Python SDK can successfully get the db schema from API
    """
    schema = cript_api.schema

    assert bool(schema._db_schema)
    assert isinstance(schema._db_schema, dict)

    # db schema should have at least 30 fields
    assert len(schema._db_schema["$defs"]) > 30


def test_is_node_schema_valid(cript_api: cript.API) -> None:
    """
    test that a CRIPT node can be correctly validated and invalidated with the db schema

    * test a couple of nodes to be sure db schema validation is working fine
        * material node
        * file node
    * test db schema validation with an invalid node, and it should be invalid

    Notes
    -----
    * does not test if serialization/deserialization works correctly,
    just tests if the node schema can work correctly if serialization was correct

    # TODO the tests here only test POST db schema and not PATCH yet, those tests must be added
    """

    # ------ invalid node schema------
    invalid_schema = {"invalid key": "invalid value", "node": ["Material"]}

    with pytest.raises(CRIPTNodeSchemaError):
        cript_api.schema.is_node_schema_valid(node_json=json.dumps(invalid_schema), is_patch=False)

    # ------ valid material schema ------
    # valid material node
    valid_material_dict = {"node": ["Material"], "name": "0.053 volume fraction CM gel", "uid": "_:0.053 volume fraction CM gel"}

    # convert dict to JSON string because method expects JSON string
    assert cript_api.schema.is_node_schema_valid(node_json=json.dumps(valid_material_dict), is_patch=False) is True
    # ------ valid file schema ------
    valid_file_dict = {
        "node": ["File"],
        "source": "https://criptapp.org",
        "type": "calibration",
        "extension": ".csv",
        "data_dictionary": "my files data dictionary",
    }

    # convert dict to JSON string because method expects JSON string
    assert cript_api.schema.is_node_schema_valid(node_json=json.dumps(valid_file_dict), is_patch=False) is True


def test_is_node_schema_valid_skipped(cript_api: cript.API) -> None:
    """
    test that a CRIPT node can be correctly validated and invalidated with the db schema, when skipping tests is active

    * test db schema validation with an invalid node, and it should be invalid, but only detected if forced

    Notes
    -----
    * does not test if serialization/deserialization works correctly,
    just tests if the node schema can work correctly if serialization was correct

    """

    def extract_base_url(url):
        # Split the URL by "//" first to separate the scheme (like http, https)
        parts = url.split("//", 1)
        scheme, rest = parts if len(parts) > 1 else ("", parts[0])

        # Split the rest by the first "/" to separate the domain
        domain = rest.split("/", 1)[0]
        return f"{scheme}//{domain}" if scheme else domain

    with cript.API(host=extract_base_url(cript_api.host), api_token=cript_api._api_token, storage_token=cript_api._storage_token) as local_cript_api:
        local_cript_api.schema.skip_validation = True
        # ------ invalid node schema------
        invalid_schema = {"invalid key": "invalid value", "node": ["Material"]}

        # Test should be skipped
        assert local_cript_api.schema.is_node_schema_valid(node_json=json.dumps(invalid_schema), is_patch=False) is None

        with pytest.raises(CRIPTNodeSchemaError):
            local_cript_api.schema.is_node_schema_valid(node_json=json.dumps(invalid_schema), is_patch=False, force_validation=True)


def test_get_vocabulary_by_category(cript_api: cript.API) -> None:
    """
    tests if a vocabulary can be retrieved by category
    1. tests response is a list of dicts as expected
    1. create a new list of just material identifiers
    1. tests that the fundamental identifiers exist within the API vocabulary response

    Warnings
    --------
    This test only gets the vocabulary category for "material_identifier_key" and does not test all the possible
    CRIPT controlled vocabulary
    """

    material_identifier_vocab_list = cript_api.schema.get_vocab_by_category(cript.VocabCategories.MATERIAL_IDENTIFIER_KEY)

    # test response is a list of dicts
    assert isinstance(material_identifier_vocab_list, list)

    material_identifiers = [identifier["name"] for identifier in material_identifier_vocab_list]

    # assertions
    assert "bigsmiles" in material_identifiers
    assert "smiles" in material_identifiers
    assert "pubchem_cid" in material_identifiers


def test_is_vocab_valid(cript_api: cript.API) -> None:
    """
    tests if the method for vocabulary is validating and invalidating correctly

    * test with custom key to check it automatically gives valid
    * test with a few vocabulary_category and vocabulary_words
        * valid category and valid vocabulary word
    * test that invalid category throws the correct error
        * invalid category and valid vocabulary word
    * test that invalid vocabulary word throws the correct error
        * valid category and invalid vocabulary word
    tests invalid category and invalid vocabulary word
    """
    # custom vocab
    # assert cript_api.schema._is_vocab_valid(vocab_category=cript.VocabCategories.ALGORITHM_KEY, vocab_word="+my_custom_key") is True

    # valid vocab category and valid word
    assert cript_api.schema._is_vocab_valid(vocab_category=cript.VocabCategories.FILE_TYPE, vocab_word="calibration") is True
    assert cript_api.schema._is_vocab_valid(vocab_category=cript.VocabCategories.QUANTITY_KEY, vocab_word="mass") is True
    assert cript_api.schema._is_vocab_valid(vocab_category=cript.VocabCategories.UNCERTAINTY_TYPE, vocab_word="fwhm") is True

    # valid vocab category but invalid vocab word
    with pytest.raises(InvalidVocabulary):
        cript_api.schema._is_vocab_valid(vocab_category=cript.VocabCategories.FILE_TYPE, vocab_word="some_invalid_word")
