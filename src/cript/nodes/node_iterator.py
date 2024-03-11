from dataclasses import fields
from typing import Any, List, Set


class NodeIterator:
    def __init__(self, root):
        self._iter_position: int = 0
        self._uuid_visited: Set[str] = set(str(root.uuid))
        self._stack: List[Any] = [root]
        self._depth_first(root)

    def _depth_first(self, node) -> None:
        """Helper function that does the traversal in depth first order and stores result in stack"""

        def handle_child_node(child_node):
            """Helper function that adds a child to the stack.

            This function can be called for both listed children and regular children attributes
            """
            self._stack.append(child_node)
            self._uuid_visited.add(str(child_node.uuid))
            # Recursive call to add all children
            self._depth_first(child_node)

        for attr_name in fields(node._json_attrs):
            attr = getattr(node._json_attrs, str(attr_name))
            try:  # Only attribute that have uuid, can be UUID children
                uuid = str(attr.uuid)
            except AttributeError:
                # Handle list attributes
                if isinstance(attr, list):
                    for list_attr in attr:
                        try:
                            list_uuid = str(attr.uuid)  # type: ignore
                        except AttributeError:
                            pass  # We do not handle non-uuid nodes
                        else:
                            if list_uuid not in self._uuid_visited:
                                handle_child_node(list_attr)
            else:
                if uuid not in self._uuid_visited:  # break cycles
                    handle_child_node(attr)

    def __next__(self):
        if self._iter_position >= len(self._stack):
            raise StopIteration
        self._iter_position += 1
        return self._stack[self._iter_position - 1]

    def __iter__(self):
        self._iter_position = 0
        return self
