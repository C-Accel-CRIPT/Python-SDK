import json

import pytest
from util import strip_uid_from_dict

import cript


def test_group_serialization_and_deserialization():
    """
    tests group JSON serialization and deserialization

    Notes
    -----
    since Group node cannot be properly instantiated,
    * this function takes a group node in json form
    * creates a python node from the json
    * serializes the python node into json again
    * compares that the two JSONs are the same
    """
    group_node_dict = {
        "node": ["Group"],
        # "name": "my group name",
        # "notes": "my group notes",
        # "admins": [
        #     {
        #         "node": ["User"],
        #         "username": "my admin username",
        #         "email": "admin_email@email.com",
        #         "orcid": "0000-0000-0000-0001",
        #     }
        # ],
        # "users": [{"node": ["User"], "username": "my username", "email": "user@email.com", "orcid": "0000-0000-0000-0002"}],
    }

    # convert dict to JSON
    # convert Json to Group node
    actual_group_node = cript.load_nodes_from_json(nodes_json=json.dumps(group_node_dict))

    # convert Group back to JSON
    actual_group_node = actual_group_node.json

    # convert JSON to dict for accurate comparison
    actual_group_node = json.loads(actual_group_node)

    # group node from JSON and original group JSON are equivalent
    assert strip_uid_from_dict(actual_group_node) == strip_uid_from_dict(group_node_dict)


@pytest.fixture(scope="session")
def group_node() -> cript.Group:
    """
    create a group from JSON that can be used by other tests

    Notes
    -----
    User node should only be created from JSON and not from instantiation

    Returns
    -------
    Group
    """

    # create group node
    group_dict = {
        "node": ["Group"],
        "name": "my group name",
        "notes": "my group notes",
        "admins": [
            {
                "node": ["User"],
                "username": "my admin username",
                "email": "admin_email@email.com",
                "orcid": "0000-0000-0000-0001",
            }
        ],
        "users": [{"node": ["User"], "username": "my username", "email": "user@email.com", "orcid": "0000-0000-0000-0002"}],
    }

    # convert Group dict to JSON
    group_json = json.dumps(group_dict, sort_keys=True)

    # convert JSON to Group node
    group_node = cript.load_nodes_from_json(nodes_json=group_json)

    # use group node in other tests
    yield group_node

    # reset the group node to stay consistent for all other tests
    group_node = cript.load_nodes_from_json(nodes_json=group_json)


def test_set_group_attributes(group_node):
    """
    tests that setting any group property throws an AttributeError

    Notes
    ----
    since User nodes also cannot be created
    instead of user node the setter is tested with a string
    because setting the group property at all should raise an exception
    """
    with pytest.raises(AttributeError):
        group_node.name = "my new group name"

    with pytest.raises(AttributeError):
        group_node.users = ["my new user"]

    with pytest.raises(AttributeError):
        group_node.notes = "my new notes"
