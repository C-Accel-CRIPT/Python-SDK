import cript


def test_create_simple_project(simple_collection_node) -> None:
    """
    test that a project node with only required arguments can be created
    """
    my_project_name = "my Project name"

    my_project = cript.Project(name=my_project_name, collections=[simple_collection_node])

    # assertions
    assert isinstance(my_project, cript.Project)
    assert my_project.name == my_project_name
    assert my_project.collections == [simple_collection_node]


def test_project_getters_and_setters(
    simple_project_node, simple_collection_node, complex_collection_node, simple_material_node
) -> None:
    """
    tests that a Project node getters and setters are working as expected

    1. use a simple project node
    2. set all of its attributes to something new
    3. get all of its attributes
    4. what was set and what was gotten should be equivalent
    """
    new_project_name = "my new project name"

    # set attributes
    simple_project_node.name = new_project_name
    simple_project_node.collections = [complex_collection_node]
    simple_project_node.materials = [simple_material_node]

    # get attributes and assert that they are the same
    assert simple_project_node.name == new_project_name
    assert simple_project_node.collections == [complex_collection_node]
    assert simple_project_node.materials == [simple_material_node]


def test_project_to_json():
    """
    test a project node can be correctly converted to JSON form
    """
    pass


def test_project_from_json():
    """
    tests a project node from be created from JSON
    """
    pass


def test_getters_and_setters():
    """
    tests that all getters and setters are working correctly
    1. gets the attributes from the project node
    2. sets all the attributes
    3. gets all the attributes again to be sure they have been set correctly
    """
    pass
