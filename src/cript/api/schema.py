from typing import Union

from api import API, _get_global_cached_api


def is_node_valid(node_json: str, api: Union[API, None] = None) -> bool:
    if api is None:
        api = _get_global_cached_api()
    return api.is_node_valid(node_json)
