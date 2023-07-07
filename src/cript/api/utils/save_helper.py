from cript.api.api import _get_global_cached_api
from cript.api.exceptions import CRIPTAPISaveError


def brute_force_save(project, bad_uuid: str) -> None:
    """
    the API class tries to save the project, if the API gives a `Bad UUID` error
    then it will try to brute_force_save it

    try to save project
        if `Bad UUID error`
            find the node that has to be saved first before being referred to as just UUID in JSON
                save that material
                strip that node and replace them with the saved UUID only throughout the whole JSON
    """
    while True:
        try:
            # find the node that has bad UUID error
            node_to_save_first = find_node_by_uuid(project_node=project, uuid=bad_uuid)

            # save the node that was unsaved to the API
            api = _get_global_cached_api()
            api.send_post_request(node=node_to_save_first)

            # try to save the whole project again and see if it'll work this time
            api.save(project=project)

            # if everything went successfully and everything saved well, then exist
            break

        except CRIPTAPISaveError as error:
            # if there is a bad UUID error then it will catch it here
            # get the bad UUID, set the bad UUID, and try brute force saving again

            error_message = str(error)
            if error_message.startswith("API responded with 'http:400 Bad uuid: "):
                bad_uuid = get_bad_uuid_from_error_message(error_message=error_message)

            # there was an error with the save, so loop over again and try again

            # if we are not handling the error then raise it
            else:
                raise error


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
