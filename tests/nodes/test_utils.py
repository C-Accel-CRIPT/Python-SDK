from cript.nodes.util import _is_node_field_valid


def test_is_node_field_valid() -> None:
    """
    test the `_is_node_field_valid()` function to be sure it does the node type check correctly

    checks both in places it should be valid and invalid
    """
    assert _is_node_field_valid(node_type_list=["Project"]) is True

    assert _is_node_field_valid(node_type_list=["Project", "Material"]) is False

    assert _is_node_field_valid(node_type_list=[""]) is False

    assert _is_node_field_valid(node_type_list="Project") is False

    assert _is_node_field_valid(node_type_list=[]) is False
