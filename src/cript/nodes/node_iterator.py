from dataclasses import fields
from typing import Any, List, Set


class NodeIterator:
    def __init__(self, root, max_recursion_depth=-1):
        self._iter_position: int = 0
        self._uuid_visited: Set[str] = set(str(root.uuid))
        self._stack: List[Any] = []
        self._recursion_depth = []
        self._max_recursion_depth = max_recursion_depth
        self._depth_first(root, 0)

    def _handle_child_node(self, child_node, recusrion_depth: int) -> bool:
        """Helper function that adds a child to the stack.

        This function can be called for both listed children and regular children attributes
        """
        try:
            uuid = str(child_node.uuid)
        except AttributeError:
            return False

        if uuid not in self._uuid_visited:
            self._stack.append(child_node)
            self._uuid_visited.add(str(child_node.uuid))
            self._recursion_depth.append(recusrion_depth)
            return True
        return False

    def _depth_first(self, node, recusrion_depth: int) -> None:
        """Helper function that does the traversal in depth first order and stores result in stack"""

        successfull_add = self._handle_child_node(node, recusrion_depth)
        if self._max_recursion_depth >= 0 and recusrion_depth >= self._max_recursion_depth:
            return

        if successfull_add:
            for attr_name in fields(node._json_attrs):
                attr = getattr(node._json_attrs, str(attr_name.name))
                node_added = self._handle_child_node(attr, recusrion_depth)
                if node_added:
                    self._depth_first(node, recusrion_depth + 1)
                else:
                    if isinstance(attr, list):
                        for list_attr in attr:
                            node_added = self._handle_child_node(list_attr, recusrion_depth)
                            if node_added:
                                self._depth_first(list_attr, recusrion_depth + 1)

    def __next__(self):
        if self._iter_position >= len(self._stack):
            raise StopIteration
        self._iter_position += 1
        return self._stack[self._iter_position - 1]

    def __iter__(self):
        self._iter_position = 0
        return self

    def __len__(self):
        return len(self._stack)

    def __getitem__(self, idx: int):
        return self._stack[idx]
