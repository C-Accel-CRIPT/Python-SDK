import pytest
from pydantic_core._pydantic_core import ValidationError

import cript


def test_type_hint() -> None:
    """
    tests that the type hint is working correctly
    """
    # valid material
    cript.Material(name="my test material", identifier=[{"bigsmiles": "my bigsmiles"}])

    # invalid material
    with pytest.raises(ValidationError):
        # giving an invalid identifier of int when expected List[Dict[str, str]]
        invalid_identifier = 5
        cript.Material(name="my test material", identifier=invalid_identifier)

    # invalid collection
    with pytest.raises(ValidationError):
        cript.Collection(name=5)
