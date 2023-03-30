import copy
from typing import Union

from cript.api.exceptions import InvalidVocabulary, InvalidVocabularyCategory


# We could keep the module structe, but a class seems the better design to me.
class Vocabulary:
    """
    Class that holds the vocab and offers methods to work with it.
    """

    def __init__(self, vocab_data: dict):
        # Perform some test if we are supporting this version of the vocab

        self._data = vocab_data

    def get_vocabulary(self, vocab_category: str):
        """
        Returns
        -------
        dict
        controlled vocabulary
        """

        if vocab_category not in self._data:
            raise InvalidVocabularyCategory(vocab_category, self._data.keys())

        # Again, return a copy because we don't want
        # anyone being able to change the private attribute
        return copy.deepcopy(self._data[vocab_category])

    def is_vocab_valid(
        self, vocab_category: str, vocab_value: str
    ) -> Union[bool, InvalidVocabulary, InvalidVocabularyCategory]:
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
        # This is deactivated currently, no custom vocab allowed.
        if vocab_value.startswith("+"):
            return True

        # Raise Exeption if invalid category
        controlled_vocabulary = self.get_vocabulary(vocab_category)

        if vocab_value in controlled_vocabulary:
            return True
        # if the vocabulary does not exist in a given category
        raise InvalidVocabulary(vocab_value, controlled_vocabulary)
