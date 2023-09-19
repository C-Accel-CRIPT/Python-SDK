import cript
from cript.api.utils.helper_functions import get_node_type_snake_case


def test_get_node_type_snake_case(simple_computation_process_node) -> None:
    """
    tests that given a node_type in string, object, or class that it gets the
    node type in snake case correctly
    """
    # get node_type using the node object
    assert get_node_type_snake_case(node_type=simple_computation_process_node) == "computation_process"

    # get node_type using the node class name
    assert get_node_type_snake_case(node_type=cript.ComputationProcess) == "computation_process"

    # get node_type using the node string
    assert get_node_type_snake_case(node_type="computation_process") == "computation_process"
