"""
the types of search that are possible on the CRIPT platform
"""

from enum import Enum


class SearchModes(Enum):
    """
    KEYS are in uppercase because that is convention
    values are in lowercase because that is easier to type and remember
    """
    NODE_TYPE = ""
    UUID = "uuid"
    CONTAINS_NAME = "contains_name"
    EXACT_NAME = "exact_name"
    UUID_CHILDREN = "uuid_children"
