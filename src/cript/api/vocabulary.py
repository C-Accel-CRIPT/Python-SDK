import json
from typing import Union

import requests

from cript.api.api import _HOST
from cript.api.exceptions import InvalidVocabulary

# dictionary of the entire controlled vocabulary
_ENTIRE_CONTROLLED_VOCABULARY: dict = {}


def _get_controlled_vocabulary() -> dict:
    """
    gets the entire controlled vocabulary
    1. checks global variable to see if it is already set
        if it is already set then it just returns that
    2. if global variable is empty, then it makes a request to the API
        and gets the entire controlled vocabulary
        and then sets the global variable to it

    Returns
    -------
    dict
        controlled vocabulary
    """

    global _ENTIRE_CONTROLLED_VOCABULARY

    # if cache is empty then make request and set cache
    if len(_ENTIRE_CONTROLLED_VOCABULARY) == 0:
        # TODO make request to API to get controlled vocabulary
        response = requests.get(f"{_HOST}/controlled-vocabulary").json()

        # convert to dict for easier use
        response = json.loads(response)

        _ENTIRE_CONTROLLED_VOCABULARY = response

    return _ENTIRE_CONTROLLED_VOCABULARY


def is_vocab_valid(vocab_category: str, vocab_value: str) -> Union[bool, InvalidVocabulary]:
    """
    checks if the vocabulary is valid within the CRIPT controlled vocabulary.
    Either returns True or InvalidVocabulary Exception

    1. if the vocabulary is custom (starts with "+")
        then it is automatically valid
    2. if vocabulary is not custom, then it is checked against its category
        if the word cannot be found in the category then it returns False

    Parameters
    ----------
    vocab_category: str
        the category the vocabulary is in e.g. "Material keyword", "Data type", "Equipment key"
    vocab_value: str
        the vocabulary word e.g. "CAS", "SMILES", "BigSmiles", "+my_custom_key"

    Returns
    -------
    a boolean of if the vocabulary is valid or not

    Raises
    ------
    InvalidVocabulary
        If the vocabulary is invalid then the error gets raised
    """

    # check if vocab is custom
    if vocab_value.startswith("+"):
        return True

    controlled_vocabulary: dict = _get_controlled_vocabulary()

    try:
        if vocab_value in controlled_vocabulary[vocab_category]:
            return True
        else:
            # if the vocabulary does not exist in a given category
            raise InvalidVocabulary
    except KeyError:
        # either the category or vocabulary word did not exist within the dict
        raise InvalidVocabulary
