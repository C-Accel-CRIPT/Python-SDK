"""
the types of search that are possible on the CRIPT platform
"""

from enum import Enum
from typing import List


# from typing import NamedTuple other option to Enum is NamedTuple


class SearchModes(Enum):
    NODE_TYPE = ""
    UUID = "uuid"
    CONTAINS_NAME = "contains_name"
    EXACT_NAME = "exact_name"
    UUID_CHILDREN = "uuid_children"


# list of valid search mode values "", "uuid", "contains_name", etc.
_VALID_SEARCH_MODES: List[str] = [mode.value for mode in SearchModes]
