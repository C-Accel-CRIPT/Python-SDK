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

        for attr_name in fields(node._json_attrs):
            attr = getattr(node._json_attrs.attr_name)
            try:  # Only attribute that have uuid, can be UUID children
                uuid = str(attr.uuid)
            except AttributeError:
                pass  # Ignore non-uuid nodes
            else:
                if uuid not in self._uuid_visited:  # break cycles
                    self._stack.append(attr)
                    self._uuid_visited.add(uuid)
                    # Recursive call to add all children
                    self._add_children(attr)

    def __next__(self):
        if self._iter_position >= len(self._stack):
            raise StopIteration
        self._iter_position += 1
        return self._stack[self._iter_position - 1]

    def __iter__(self):
        self._iter_position = 0
        return self
