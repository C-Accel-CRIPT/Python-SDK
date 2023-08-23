import pytest
from beartype.roar import BeartypeCallHintParamViolation

import cript


def test_type_hint() -> None:
    """
    tests that the type hint is working correctly
    """
    # valid material
    cript.Material(name="my test material", identifier=[{"bigsmiles": "my bigsmiles"}])


    with pytest.raises(BeartypeCallHintParamViolation) as error:
        # giving an invalid identifier of int when expected List[Dict[str, str]]
        invalid_identifier = 5
        cript.Material(name="my test material", identifier=invalid_identifier)


