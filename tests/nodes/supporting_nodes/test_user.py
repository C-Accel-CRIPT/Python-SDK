import pytest

import cript
from cript.nodes.exceptions import UneditableAttributeError


def test_user_from_json():
    """
    tests just to see if a user node can be created from json
    """
    pass


@pytest.fixture(scope="session")
def user_node() -> cript.User:
    """
    create a user node for other tests to use

    Notes
    -----
    User node should only be created from JSON and not from instantiation

    Returns
    -------
    User
    """
    # TODO create this user node from JSON instead of instantiation
    my_user = cript.User(
        username="my username",
        email="my_email@email.com",
        orcid="123456",
        groups=["my group"],
    )
    return my_user


def test_set_user_properties(user_node):
    """
    tests that setting any user property throws an UneditableAttributeError
    """
    with pytest.raises(UneditableAttributeError):
        user_node.username = "my new username"

    with pytest.raises(UneditableAttributeError):
        user_node.email = "my new email"

    with pytest.raises(UneditableAttributeError):
        user_node.orcid = "my new orcid"

    with pytest.raises(UneditableAttributeError):
        # TODO try setting it via a group node
        #   either way it should give the same error
        user_node.orcid = ["my new group"]


def test_user_to_json():
    """
    tests that a user node can be converted to JSON correctly
    """
    pass
