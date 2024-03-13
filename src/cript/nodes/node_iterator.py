from dataclasses import fields
from typing import Any, List, Set


class NodeIterator:
    def __init__(self, root, max_recursion_depth=-1):
        self._iter_position: int = 0
        self._uuid_visited: Set[str] = set()
        self._stack: List[Any] = []
        self._recursion_depth = []
        self._max_recursion_depth = max_recursion_depth
        self._depth_first(root, 0)

    def _add_node(self, child_node, recursion_depth: int):
        if child_node.uuid not in self._uuid_visited:
            self._stack.append(child_node)
            self._recursion_depth.append(recursion_depth)
            self._uuid_visited.add(child_node.uuid)
            return True
        return False

    def _check_recursion(self, child_node) -> bool:
        """Helper function that adds a child to the stack.

        This function can be called for both listed children and regular children attributes
        """
        try:
            uuid = child_node.uuid
        except AttributeError:
            return False

        if uuid not in self._uuid_visited:
            return True
        return False

    def _depth_first(self, node, recursion_depth: int) -> None:
        """Helper function that does the traversal in depth first order and stores result in stack"""
        node_added = self._add_node(node, recursion_depth)
        if not node_added:
            return

        if self._max_recursion_depth >= 0 and recursion_depth >= self._max_recursion_depth:
            return

        field_names = [field.name for field in fields(node._json_attrs)]
        for attr_name in sorted(field_names):
            attr = getattr(node._json_attrs, attr_name)
            if not isinstance(attr, list):
                attr = [attr]
            for list_attr in attr:
                if self._check_recursion(list_attr):
                    self._depth_first(list_attr, recursion_depth + 1)

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
