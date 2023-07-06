from cript.api.exceptions import CRIPTAPISaveError


def brute_force_save(project, bad_uuid):
    """
    the main function that essentially coordinates the whole POST or PATCH requests to the API
    and brute forces it to save

    try to save project
        if `Bad UUID error`
            find the material that has that error
                posts that material
                and strip all material nodes and replace them with the posted UUID
    """
    try:
        node_to_save_first = find_node_by_uuid(project_node=project, uuid=bad_uuid)
    except CRIPTAPISaveError as error:
        pass


def get_bad_uuid_from_error_message(error_message: str) -> str:
    """
    takes an CRIPTAPISaveError and tries to get the UUID that the API is having trouble with
    and return that

    Parameters
    ----------
    error_message: str

    Returns
    -------
    UUID
        the UUID the API had trouble with
    """
    # stripping left and right side of the UUID from error message to isolate the UUID
    bad_uuid = error_message.lstrip("API responded with 'http:400 Bad uuid: ").rstrip(" provided'")
    return bad_uuid


def find_node_by_uuid(project_node, uuid: str):
    all_materials = project_node.find_children({"node": ["Material"]})

    for material in all_materials:
        if material.uuid == uuid:
            return material

    # TODO This should not be triggered and should be handled better
    raise Exception("could not find any material with that UUID")


def replace_node_with_saved_uuid(project_node, saved_uuid):
    """
    takes a project and traverses through the entire tree
    finds any place that has a full node instead of just a UUID
    and strips the node and replaces it with a UUID instead
    """
    pass
