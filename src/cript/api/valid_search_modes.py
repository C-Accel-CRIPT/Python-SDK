"""
the types of search that are possible on the CRIPT platform
"""

from enum import Enum


class SearchModes(Enum):
    """
    Search modes to be used with cript.API.search
    KEYS are in uppercase because that is convention
    values are in lowercase because that is easier to type and remember
    """

    NODE_TYPE = ""
    EXACT_NAME = "exact_name"
    CONTAINS_NAME = "contains_name"
    UUID = "uuid"
    # UUID_CHILDREN = "uuid_children"
