import json
from typing import Dict, List, Union

from cript.nodes.exceptions import CRIPTJsonNodeError
from cript.nodes.util.json import _is_node_field_valid


def _get_node_type_from_json(node_json: Union[Dict, str]) -> str:
    """
    takes a node JSON and output the node_type `Project`, `Material`, etc.

    1. convert node JSON dict or str to dict
    1. do check the node list to be sure it only has a single type in it
    1. get the node type and return it

    Parameters
    ----------
    node_json: [Dict, str]

    Notes
    -----
    Takes a str or dict to be more versatile

    Returns
    -------
    str:
        node type
    """
    # convert all JSON node strings to dict for easier handling
    if isinstance(node_json, str):
        node_json = json.loads(node_json)
    try:
        node_type_list: List[str] = node_json["node"]  # type: ignore
    except KeyError:
        raise CRIPTJsonNodeError(node_list=node_json["node"], json_str=json.dumps(node_json))  # type: ignore

    # check to be sure the node list has a single type "node": ["Material"]
    if _is_node_field_valid(node_type_list=node_type_list):
        return node_type_list[0]

    # if invalid then raise error
    else:
        raise CRIPTJsonNodeError(node_list=node_type_list, json_str=str(node_json))
