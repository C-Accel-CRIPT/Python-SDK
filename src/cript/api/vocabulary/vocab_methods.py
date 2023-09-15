from typing import Dict, List

import requests
from beartype import beartype

from cript import VocabCategories
from cript.api.exceptions import InvalidVocabulary, APIError
from cript.api.api_config import _API_TIMEOUT


def _get_vocab(self) -> dict:
    """
    gets the entire CRIPT controlled vocabulary and stores it in _vocabulary

    1. loops through all controlled vocabulary categories
        1. if the category already exists in the controlled vocabulary then skip that category and continue
        1. if the category does not exist in the `_vocabulary` dict,
        then request it from the API and append it to the `_vocabulary` dict
    1. at the end the `_vocabulary` should have all the controlled vocabulary and that will be returned

       Examples
       --------
       The vocabulary looks like this
       ```json
       {'algorithm_key':
            [
                {
                'description': "Velocity-Verlet integration algorithm. Parameters: 'integration_timestep'.",
                'name': 'velocity_verlet'
                },
        }
       ```
    """

    # loop through all vocabulary categories and make a request to each vocabulary category
    # and put them all inside of self._vocab with the keys being the vocab category name
    for category in VocabCategories:
        if category in self._vocabulary:
            continue

        self._vocabulary[category.value] = self.get_vocab_by_category(category)

    return self._vocabulary


@beartype
def get_vocab_by_category(self, category: VocabCategories) -> List[Dict]:
    """
    get the CRIPT controlled vocabulary by category

    Parameters
    ----------
    category: str
        category of

    Returns
    -------
    List[dict]
        list of JSON containing the controlled vocabulary
    """

    # check if the vocabulary category is already cached
    if category.value in self._vocabulary:
        return self._vocabulary[category.value]

    vocabulary_category_url: str = f"{self.host}/cv/{category.value}/"

    # if vocabulary category is not in cache, then get it from API and cache it
    response: Dict = requests.get(url=vocabulary_category_url, timeout=_API_TIMEOUT).json()

    if response["code"] != 200:
        raise APIError(api_error=str(response), http_method="GET", api_url=vocabulary_category_url)

    # add to cache
    self._vocabulary[category.value] = response["data"]

    return self._vocabulary[category.value]


@beartype
def _is_vocab_valid(self, vocab_category: VocabCategories, vocab_word: str) -> bool:
    """
    checks if the vocabulary is valid within the CRIPT controlled vocabulary.
    Either returns True or InvalidVocabulary Exception

    1. if the vocabulary is custom (starts with "+")
        then it is automatically valid
    2. if vocabulary is not custom, then it is checked against its category
        if the word cannot be found in the category then it returns False

    Parameters
    ----------
    vocab_category: VocabCategories
        ControlledVocabularyCategories enums
    vocab_word: str
        the vocabulary word e.g. "CAS", "SMILES", "BigSmiles", "+my_custom_key"

    Returns
    -------
    a boolean of if the vocabulary is valid

    Raises
    ------
    InvalidVocabulary
        If the vocabulary is invalid then the error gets raised
    """

    # check if vocab is custom
    # This is deactivated currently, no custom vocab allowed.
    if vocab_word.startswith("+"):
        return True

    # get the entire vocabulary
    controlled_vocabulary = self._get_vocab()
    # get just the category needed
    controlled_vocabulary = controlled_vocabulary[vocab_category.value]

    # TODO this can be faster with a dict of dicts that can do o(1) look up
    #  looping through an unsorted list is an O(n) look up which is slow
    # loop through the list
    for vocab_dict in controlled_vocabulary:
        # check the name exists within the dict
        if vocab_dict.get("name") == vocab_word:
            return True

    raise InvalidVocabulary(vocab=vocab_word, possible_vocab=list(controlled_vocabulary))
