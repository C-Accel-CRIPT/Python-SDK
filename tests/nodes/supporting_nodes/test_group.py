import pytest

import cript
from cript.nodes.exceptions import UneditableAttributeError


def test_create_group_from_json():
    """
    simply tests if a valid group node can be created from API JSON
    """
    pass


@pytest.fixture(scope="session")
def group_node() -> cript.Group:
    """
    create a group from JSON that can be used by other tests

    Returns
    -------
    Group
    """
    # TODO create group object from JSON instead of code
    my_group = cript.Group(name="my group", admins=["admin 1"], users=["user 1"])
    return my_group


def test_group_to_json(group_node) -> None:
    """
    tests if the group node can be correctly serialized to JSON
    """
    pass


def test_set_group_name(group_node):
    """
    tests that setting any group property throws an UneditableAttributeError

    Notes
    ----
    since User nodes also cannot be created
    instead of user node the setter is tested with a string
    because setting the group property at all should raise an exception
    """
    with pytest.raises(UneditableAttributeError):
        group_node.name = "my new group name"

    with pytest.raises(UneditableAttributeError):
        group_node.users = ["my new user"]

    with pytest.raises(UneditableAttributeError):
        group_node.notes = "my new notes"
