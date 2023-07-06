def save_main(project_node):
    """
    the main function that essentially coordinates the whole POST or PATCH requests to the API
    and brute forces it to save

    try to save project
        if `Bad UUID error`
            find the material that has that error
                posts that material
                and strip all material nodes and replace them with the posted UUID
    """
    pass


def send_post_request_to_api(node):
    """
    simply send POST request to the API

    raise error if not 200 from API

    Parameters
    ----------
    node

    Returns
    -------

    Notes
    -----
    Gets the host from cript.API property
    """
    pass


def find_node_by_uuid(project_node, uuid: str):
    """
    traverses the project JSON to find a full node from UUID

    Parameters
    ----------
    project_node
        project node that we want to save
    uuid: str
        uuid that the API says is bad

    Returns
    -------
    node: dict
        the full node dict from the uuid string
    """
    pass


def replace_node_with_saved_uuid(project_node, saved_uuid):
    """
    takes a project and traverses through the entire tree
    finds any place that has a full node instead of just a UUID
    and strips the node and replaces it with a UUID instead
    """
    pass
