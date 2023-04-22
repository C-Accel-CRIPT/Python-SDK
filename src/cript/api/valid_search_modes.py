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
    CONTAINS_NAME = "contains_name"
    UUID_CHILDREN = "uuid_children"


class ExactSearchModes(Enum):
    """
    Search modes to be used with cript.API.search_exact
    KEYS are in uppercase because that is convention
    values are in lowercase because that is easier to type and remember
    """

    UUID = "uuid"
    NAME = "exact_name"
