import cript
import pytest


def test_create_collection_slim() -> None:
    """
    test just to see if a collection can be made without any issues
    with just a collection name and nothing else

    Returns
    -------
    None
    """
    my_collection = cript.Collection(name="my collection name")


def test_create_collection_full() -> None:
    """
    test to see if Collection can be made with all the possible options filled

    Returns
    -------
    None
    """
    my_collection = cript.Collection(name="my collection name")
