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
