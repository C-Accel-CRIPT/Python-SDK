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
