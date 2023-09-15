import json

import pytest
from tests.utils.util import strip_uid_from_dict

import cript


def test_user_serialization_and_deserialization(complex_user_dict, complex_user_node):
    """
    tests just to see if a user node can be correctly deserialized from json
    and serialized to json

    Notes
    -----
    * since a User node cannot be instantiated
    * a User node is created from JSON
    * then the user node attributes are compared to what they are expected
    * to check that the user node is created correctly
    """

    user_node_dict = complex_user_dict
    user_node = complex_user_node
    assert user_node_dict == strip_uid_from_dict(json.loads(user_node.json))

    # deserialize node from JSON
    user_node = cript.load_nodes_from_json(nodes_json=user_node.json)

    # checks that the user node has been created correctly by checking the properties
    assert user_node.username == user_node_dict["username"]
    assert user_node.email == user_node_dict["email"]
    assert user_node.orcid == user_node_dict["orcid"]

    # check serialize node to JSON is working correctly
    # convert dicts for better comparison
    assert strip_uid_from_dict(json.loads(user_node.json)) == user_node_dict


def test_set_user_properties(complex_user_node):
    """
    tests that setting any user property throws an AttributeError
    """
    with pytest.raises(AttributeError):
        complex_user_node.username = "my new username"

    with pytest.raises(AttributeError):
        complex_user_node.email = "my new email"

    with pytest.raises(AttributeError):
        complex_user_node.orcid = "my new orcid"

    with pytest.raises(AttributeError):
        # TODO try setting it via a group node
        #   either way it should give the same error
        complex_user_node.orcid = ["my new group"]
