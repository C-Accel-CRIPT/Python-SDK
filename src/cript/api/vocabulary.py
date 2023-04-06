from typing import Union

from api import API, _get_global_cached_api

from cript.api.exceptions import InvalidVocabulary, InvalidVocabularyCategory


def get_vocabulary(vocab_category: str, api: Union[API, None] = None):
    if api is None:
        api = _get_global_cached_api()

    return api.get_vocabulary(vocab_category)


def is_vocab_valid(
    vocab_category: str, vocab_value: str, api: Union[API, None] = None
) -> Union[bool, InvalidVocabulary, InvalidVocabularyCategory]:
    if api is None:
        api = _get_global_cached_api()

    return api.is_vocab_valid(vocab_category, vocab_value)
