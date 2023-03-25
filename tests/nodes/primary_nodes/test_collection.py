import pytest

import cript
from cript import Collection


def test_create_collection_full() -> None:
    """
    test to see if Collection can be made with all the possible options filled

    Returns
    -------
    None
    """
    my_collection = cript.Collection(name="my collection name")


@pytest.fixture(scope="session")
def collection_object() -> Collection:
    """
    test just to see if a collection can be made without any issues
    with just a collection name and nothing else

    Notes
    -----
    this object is later used for other test

    Returns
    -------
    Collection
    """
    pass
