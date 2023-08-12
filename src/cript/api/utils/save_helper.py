import json
import re
import uuid
from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class _InternalSaveValues:
    """
    Class that carries attributes to be carried through recursive calls of _internal_save.
    """

    saved_uuid: Set[str] = field(default_factory=set)
    suppress_attributes: Dict[str, Set[str]] = field(default_factory=dict)

    def __add__(self, other: "_InternalSaveValues") -> "_InternalSaveValues":
        """
        Implement a short hand to combine two of these save values, with `+`.
        This unions, the `saved_uuid`.
        And safely unions `suppress_attributes` too.
        """
        # Make a manual copy of `self`.
        return_value = _InternalSaveValues(self.saved_uuid.union(other.saved_uuid), self.suppress_attributes)

        # Union the dictionary.
        for uuid_str in other.suppress_attributes:
            try:
                # If the uuid exists in both `suppress_attributes` union the value sets
                return_value.suppress_attributes[uuid_str] = return_value.suppress_attributes[uuid_str].union(other.suppress_attributes[uuid_str])
            except KeyError:
                # If it only exists in one, just copy the set into the new one.
                return_value.suppress_attributes[uuid_str] = other.suppress_attributes[uuid_str]
        return return_value

    def __gt__(self, other):
        """
        A greater comparison to see if something was added to the info.
        """
        if len(self.saved_uuid) > len(other.saved_uuid):
            return True
        if len(self.suppress_attributes) > len(other.suppress_attributes):
            return True
        # If the two dicts have the same key, make sure at least one key has more suppressed attributes
        if self.suppress_attributes.keys() == other.suppress_attributes.keys():
            longer_set_found = False
            for key in other.suppress_attributes:
                if len(self.suppress_attributes[key]) < len(other.suppress_attributes[key]):
                    return False
                if self.suppress_attributes[key] > other.suppress_attributes[key]:
                    longer_set_found = True
            return longer_set_found
        return False


def _fix_node_save(api, node, response, save_values: _InternalSaveValues) -> _InternalSaveValues:
    """
    Helper function, that attempts to fix a bad node.
    And if it is fixable, we resave the entire node.

    Returns set of known uuids, if fixable, otherwise False.
    """
    if response["code"] not in (400, 409):
        raise RuntimeError(f"The internal helper function `_fix_node_save` has been called for an error that is not yet implemented to be handled {response}.")

    if response["error"].startswith("Bad uuid:") or response["error"].strip().startswith("Duplicate uuid:"):
        missing_uuid = _get_uuid_from_error_message(response["error"])
        missing_node = find_node_by_uuid(node, missing_uuid)
        # If the missing node, is the same as the one we are trying to save, this not working.
        # We end the infinite loop here.
        if missing_uuid == str(node.uuid):
            return save_values
        # Now we save the bad node extra.
        # So it will be known when we attempt to save the graph again.
        # Since we pre-saved this node, we want it to be UUID edge only the next JSON.
        # So we add it to the list of known nodes
        returned_save_values = api._internal_save(missing_node, save_values)
        save_values += returned_save_values
        # The missing node, is now known to the API
        save_values.saved_uuid.add(missing_uuid)

    # Handle all duplicate items warnings if possible
    if response["error"].startswith("duplicate item"):
        for search_dict_str in re.findall(r"\{(.*?)\}", response["error"]):  # Regular expression finds all text elements enclosed in `{}`. In the error message this is the dictionary describing the duplicated item.
            # The error message contains a description of the offending elements.
            search_dict_str = "{" + search_dict_str + "}"
            search_dict_str = search_dict_str.replace("'", '"')
            search_dict = json.loads(search_dict_str)
            # These are in the exact format to use with `find_children` so we find all the offending children.
            all_duplicate_nodes = node.find_children(search_dict)
            for duplicate_node in all_duplicate_nodes:
                # Unfortunately, even patch errors if you patch with an offending element.
                # So we remove the offending element from the JSON
                # TODO IF THIS IS A TRUE DUPLICATE NAME ERROR, IT WILL ERROR AS THE NAME ATTRIBUTE IS MISSING.
                try:
                    # the search_dict convenient list all the attributes that are offending in the keys.
                    # So if we haven't listed the current node in the suppress attribute dict, we add the node with the offending attributes to suppress.
                    save_values.suppress_attributes[str(duplicate_node.uuid)] = set(search_dict.keys())
                except KeyError:
                    # If we have the current node in the dict, we just add the new elements to the list of suppressed attributes for it.
                    save_values.suppress_attributes[str(duplicate_node.uuid)].add(set(search_dict.keys()))  # type: ignore

                # Attempts to save the duplicate items element.
                save_values += api._internal_save(duplicate_node, save_values)
                # After the save, we can reduce it to just a UUID edge in the graph (avoiding the duplicate issues).
                save_values.saved_uuid.add(str(duplicate_node.uuid))

    return save_values


def _get_uuid_from_error_message(error_message: str) -> str:
    """
    takes an CRIPTAPISaveError and tries to get the UUID that the API is having trouble with
    and return that

    Parameters
    ----------
    error_message: str

    Returns
    -------
    UUID
        the UUID the API had trouble with
    """
    bad_uuid = None
    if error_message.startswith("Bad uuid: "):
        bad_uuid = error_message[len("Bad uuid: ") : -len(" provided")].strip()
    if error_message.strip().startswith("Duplicate uuid:"):
        bad_uuid = error_message[len(" Duplicate uuid:") : -len("provided")].strip()
    if bad_uuid is None or len(bad_uuid) != len(str(uuid.uuid4())):  # Ensure we found a full UUID describing string (here tested against a random new uuid length.)
        raise RuntimeError(f"The internal helper function `_get_uuid_from_error_message` has been called for an error message that is not yet implemented to be handled. error message {error_message}, found uuid {bad_uuid}.")

    return bad_uuid


def find_node_by_uuid(node, uuid_str: str):
    # Use the find_children functionality to find that node in our current tree
    # We can have multiple occurrences of the node,
    # but it doesn't matter which one we save
    # TODO some error handling, for the BUG case of not finding the UUID
    missing_node = node.find_children({"uuid": uuid_str})[0]

    return missing_node


def _identify_suppress_attributes(node, response: Dict) -> Dict[str, Set[str]]:
    suppress_attributes: Dict[str, Set[str]] = {}
    if response["error"].startswith("Additional properties are not allowed"):
        # Find all the attributes, that are listed in the error message with regex
        attributes = set(re.findall(r"'(.*?)'", response["error"]))  # regex finds all attributes in enclosing `'`. This is how the error message lists them.

        # At the end of the error message the offending path is given.
        # The structure of the error message is such, that is is after `path:`, so we find and strip the path out of the message.
        path = response["error"][response["error"].rfind("path:") + len("path:") :].strip()

        if path != "/":
            # TODO find the UUID this belongs to
            raise RuntimeError("Fixing non-root objects for patch, not implemented yet. This is a bug, please report it on https://github.com/C-Accel-CRIPT/Python-SDK/ .")

        try:
            suppress_attributes[str(node.uuid)].add(attributes)  # type: ignore
        except KeyError:
            suppress_attributes[str(node.uuid)] = attributes
    return suppress_attributes
