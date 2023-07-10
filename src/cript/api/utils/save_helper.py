def _fix_node_save(api, node, response, known_uuid):
    """
    Helper function, that attempts to fix a bad node.
    And if it is fixable, we resave the entire node.

    Returns set of known uuids, if fixable, otherwise False.
    """
    if response["code"] not in (400, 409):
        raise NotImplementedError(f"The internal helper function `_fix_node_save` has been called for an error that is not yet implemented to be handled {response}.")

    if response["error"].startswith("Bad uuid:") or response["error"].strip().startswith("Duplicate uuid:"):
        missing_uuid = _get_uuid_from_error_message(response["error"])
        missing_node = find_node_by_uuid(node, missing_uuid)

        # Now we save the bad node extra.
        # So it will be known when we attempt to save the graph again.
        # Since we pre-saved this node, we want it to be UUID edge only the next JSON.
        # So we add it to the list of known nodes
        known_uuid.union(api._internal_save(missing_node, known_uuid))  # type: ignore
        # The missing node, is now known to the API
        known_uuid.add(missing_uuid)
        # Recursive call.
        # Since we should have fixed the "Bad UUID" now, we can try to save the node again
        return api._internal_save(node, known_uuid)
    return False


def _get_uuid_from_error_message(error_message: str) -> str:
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
    bad_uuid = None
    if error_message.startswith("Bad uuid: "):
        bad_uuid = error_message[len("Bad uuid: ") : -len(" provided")].strip()
    if error_message.strip().startswith("Duplicate uuid:"):
        bad_uuid = error_message[len(" Duplicate uuid:") : -len("provided")].strip()
    if bad_uuid is None or len(bad_uuid) != 36:
        raise NotImplementedError(f"The internal helper function `_get_uuid_from_error_message` has been called for an error message that is not yet implemented to be handled. error message {error_message}, found uuid {bad_uuid}.")

    return bad_uuid


def find_node_by_uuid(node, uuid: str):
    # Use the find_children functionality to find that node in our current tree
    # We can have multiple occurrences of the node,
    # but it doesn't matter which one we save
    # TODO some error handling, for the BUG case of not finding the UUID
    missing_node = node.find_children({"uuid": uuid})[0]

    return missing_node
