from typing import Dict, Optional


def find_json_node_by_name(list_of_nodes: Dict, target_name: str) -> Optional[Dict]:
    """
    Searches through a list of JSON nodes and finds the desired node by name

    Parameters
    ----------
    list_of_nodes: Dict
        list of nodes in JSON format
    target_name: str
        the name of the node you want to find from the list of nodes

    Returns
    -------
    Dict
        desired node in JSON format
    """
    for node_json in list_of_nodes:
        if node_json["name"] == target_name:
            return node_json

    return None
