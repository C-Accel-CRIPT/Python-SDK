import copy


def strip_uid_from_dict(node_dict):
    """
    Remove "uid" attributes from nested dictionaries.
    Helpful for test purposes, since uids are always going to differ.
    """
    node_dict_copy = copy.deepcopy(node_dict)
    for key in node_dict:
        if key in ("uid", "uuid"):
            del node_dict_copy[key]
        if isinstance(node_dict, str):
            continue
        if isinstance(node_dict[key], dict):
            node_dict_copy[key] = strip_uid_from_dict(node_dict[key])
        elif isinstance(node_dict[key], list):
            for i, element in enumerate(node_dict[key]):
                if isinstance(element, dict):
                    node_dict_copy[key][i] = strip_uid_from_dict(element)
    return node_dict_copy
