"""
This module contains classes and functions that help with the json serialization and deserialization of nodes.
"""
import dataclasses
import inspect
import json
import uuid
from typing import Dict, List, Optional, Set, Union

import cript.nodes
from cript.nodes.core import BaseNode
from cript.nodes.exceptions import (
    CRIPTDeserializationUIDError,
    CRIPTJsonDeserializationError,
    CRIPTJsonNodeError,
)
from cript.nodes.util.core import iterate_leaves
from cript.nodes.uuid_base import UUIDBaseNode


@dataclasses.dataclass(frozen=True)
class UIDProxy:
    """Helper class that store temporarily unresolved UIDs."""

    uid: Optional[str] = None

    def __post_init__(self):
        if self.uid is None:
            raise RuntimeError("UID needs to be initialized")


class NodeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for serializing CRIPT nodes to JSON.

    This encoder is used to convert CRIPT nodes into JSON format while handling unique identifiers (UUIDs) and
    condensed representations to avoid redundancy in the JSON output.
    It also allows suppressing specific attributes from being included in the serialized JSON.

    Attributes
    ----------
    handled_ids : set[str]
        A set to store the UIDs of nodes that have been processed during serialization.
    known_uuid : set[str]
        A set to store the UUIDs of nodes that have been previously encountered in the JSON.
    condense_to_uuid : dict[str, set[str]]
        A set to store the node types that should be condensed to UUID edges in the JSON.
    suppress_attributes : Optional[dict[str, set[str]]]

    Methods
    -------
    ```python
    default(self, obj: Any) -> Any:
        # Convert CRIPT nodes and other objects to their JSON representation.
    ```

    ```python
    _apply_modifications(self, serialize_dict: dict) -> Tuple[dict, list[str]]:
        # Apply modifications to the serialized dictionary based on node types
        # and attributes to be condensed. This internal function handles node
        # condensation and attribute suppression during serialization.
    ```
    """

    handled_ids: Set[str] = set()
    known_uuid: Set[str] = set()
    condense_to_uuid: Dict[str, Set[str]] = dict()
    suppress_attributes: Optional[Dict[str, Set[str]]] = None

    def default(self, obj):
        """
        Convert CRIPT nodes and other objects to their JSON representation.

        This method is called during JSON serialization.
        It customizes the serialization process for CRIPT nodes and handles unique identifiers (UUIDs)
        to avoid redundant data in the JSON output.
        It also allows for attribute suppression for specific nodes.

        Parameters
        ----------
        obj : Any
            The object to be serialized to JSON.

        Returns
        -------
        dict
            The JSON representation of the input object, which can be a string, a dictionary, or any other JSON-serializable type.

        Raises
        ------
        CRIPTJsonDeserializationError
            If there is an issue with the JSON deserialization process for CRIPT nodes.

        Notes
        -----
        * If the input object is a UUID, it is converted to a string representation and returned.
        * If the input object is a CRIPT node (an instance of `BaseNode`), it is serialized into a dictionary
          representation. The node is first checked for uniqueness based on its UID (unique identifier), and if
          it has already been serialized, it is represented as a UUID edge only. If not, the node's attributes
          are added to the dictionary representation, and any default attribute values are removed to reduce
          redundancy in the JSON output.
        * The method `_apply_modifications()` is called to check if further modifications are needed before
          considering the dictionary representation done. This includes condensing certain node types to UUID edges
          and suppressing specific attributes for nodes.
        """
        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, UIDProxy):
            return obj.uid

        if isinstance(obj, BaseNode):
            try:
                uid = obj.uid
            except AttributeError:
                pass
            else:
                if uid in NodeEncoder.handled_ids:
                    return {"uid": uid}

            # When saving graphs, some nodes can be pre-saved.
            # If that happens, we want to represent them as a UUID edge only
            try:
                uuid_str = str(obj.uuid)
            except AttributeError:
                pass
            else:
                if uuid_str in NodeEncoder.known_uuid:
                    return {"uuid": uuid_str}

            default_dataclass = obj.JsonAttributes()
            serialize_dict = {}
            # Remove default values from serialization
            for field_name in [field.name for field in dataclasses.fields(default_dataclass)]:
                if getattr(default_dataclass, field_name) != getattr(obj._json_attrs, field_name):
                    serialize_dict[field_name] = getattr(obj._json_attrs, field_name)
            # add the default node type
            serialize_dict["node"] = obj._json_attrs.node

            # check if further modifications to the dict is needed before considering it done
            serialize_dict, condensed_uid = self._apply_modifications(serialize_dict)
            if uid not in condensed_uid:  # We can uid (node) as handled if we don't condense it to uuid
                NodeEncoder.handled_ids.add(uid)

            # Remove suppressed attributes
            if NodeEncoder.suppress_attributes is not None and str(obj.uuid) in NodeEncoder.suppress_attributes:
                for attr in NodeEncoder.suppress_attributes[str(obj.uuid)]:
                    del serialize_dict[attr]

            return serialize_dict
        return json.JSONEncoder.default(self, obj)

    def _apply_modifications(self, serialize_dict: Dict):
        """
        Checks the serialize_dict to see if any other operations are required before it
        can be considered done. If other operations are required, then it passes it to the other operations
        and at the end returns the fully finished dict.

        This function is essentially a big switch case that checks the node type
        and determines what other operations are required for it.

        Parameters
        ----------
        serialize_dict: Dict

        Returns
        -------
        serialize_dict: Dict
        """

        def process_attribute(attribute):
            def strip_to_edge_uuid(element):
                # Extracts UUID and UID information from the element
                try:
                    uuid = getattr(element, "uuid")
                except AttributeError:
                    uuid = element["uuid"]
                    if len(element) == 1:  # Already a condensed element
                        return element, None
                try:
                    uid = getattr(element, "uid")
                except AttributeError:
                    uid = element["uid"]

                element = {"uuid": str(uuid)}
                return element, uid

            # Processes an attribute based on its type (list or single element)
            if isinstance(attribute, List):
                processed_elements = []
                for element in attribute:
                    processed_element, uid = strip_to_edge_uuid(element)
                    if uid is not None:
                        uid_of_condensed.append(uid)
                    processed_elements.append(processed_element)
                return processed_elements
            else:
                processed_attribute, uid = strip_to_edge_uuid(attribute)
                if uid is not None:
                    uid_of_condensed.append(uid)
                return processed_attribute

        uid_of_condensed: List = []

        nodes_to_condense = serialize_dict["node"]
        for node_type in nodes_to_condense:
            if node_type in self.condense_to_uuid:
                attributes_to_process = self.condense_to_uuid[node_type]  # type: ignore
                for attribute in attributes_to_process:
                    if attribute in serialize_dict:
                        attribute_to_condense = serialize_dict[attribute]
                        processed_attribute = process_attribute(attribute_to_condense)
                        serialize_dict[attribute] = processed_attribute

        return serialize_dict, uid_of_condensed


class _NodeDecoderHook:
    def __init__(self, uid_cache: Optional[Dict] = None):
        """
        Initialize the custom JSON object hook used for CRIPT node deserialization.

        Parameters
        ----------
        uid_cache : Optional[dict], optional
            A dictionary to cache Python objects with shared UIDs, by default None.

        Notes
        -----
        The `_NodeDecoderHook` class is used as an object hook for JSON deserialization,
        handling the conversion of JSON nodes into Python objects based on their node types.
        The `uid_cache` is an optional dictionary to store cached objects with shared UIDs
        to never create two different python nodes with the same uid.
        """
        if uid_cache is None:
            uid_cache = {}
        self._uid_cache = uid_cache

    @property
    def uid_cache(self):
        return self._uid_cache

    def __call__(self, node_str: Union[Dict, str]) -> Union[Dict, UIDProxy]:
        """
        Internal function, used as a hook for json deserialization.

        This function is called recursively to convert every JSON of a node and its children from node to JSON.

        If given a JSON without a "node" field then it is assumed that it is not a node
        and just a key value pair data, and the JSON string is then just converted from string to dict and returned
        applicable for places where the data is something like

        ```json
        { "bigsmiles": "123456" }
        ```

        no serialization is needed in this case and just needs to be converted from str to dict

        if the node field is present, then continue and convert the JSON node into a Python object

        Parameters
        ----------
        node_str : Union[Dict, str]
            The JSON representation of a node or a regular dictionary.

        Returns
        -------
        Union[CRIPT Node, dict]
            Either returns a regular dictionary if the input JSON or input dict is NOT a node.
            If it is a node, it returns the appropriate CRIPT node object, such as `cript.Material`

        Raises
        ------
        CRIPTJsonNodeError
            If there is an issue with the JSON structure or the node type is invalid.
        CRIPTJsonDeserializationError
            If there is an error during deserialization of a specific node type.
        CRIPTDeserializationUIDError
            If there is an issue with the UID used for deserialization, like circular references.
        """
        node_dict = dict(node_str)  # type: ignore

        # Handle UID objects.
        if len(node_dict) == 1 and "uid" in node_dict:
            try:
                return self._uid_cache[node_dict["uid"]]
            except KeyError:
                # raise CRIPTDeserializationUIDError("Unknown", node_dict["uid"])
                proxy = UIDProxy(uid=node_dict["uid"])
                return proxy

        try:
            node_type_list = node_dict["node"]
        except KeyError:  # Not a node, just a regular dictionary
            return node_dict

        # TODO consider putting this into the try because it might need error handling for the dict
        if _is_node_field_valid(node_type_list):
            node_type_str = node_type_list[0]
        else:
            raise CRIPTJsonNodeError(node_type_list, str(node_str))

        # Iterate over all nodes in cript to find the correct one here
        for key, pyclass in inspect.getmembers(cript.nodes, inspect.isclass):
            if BaseNode in inspect.getmro(pyclass):
                if key == node_type_str:
                    try:
                        json_node = pyclass._from_json(node_dict)
                        self._uid_cache[json_node.uid] = json_node
                        return json_node
                    except Exception as exc:
                        raise CRIPTJsonDeserializationError(key, str(node_type_str)) from exc
        # Fall back
        return node_dict

    def resolve_unresolved_uids(self, node_iter):
        def handle_uid_replacement(node, name, attr):
            if isinstance(attr, UIDProxy):
                unresolved_uid = attr.uid
                try:
                    uid_node = self.uid_cache[unresolved_uid]
                except KeyError as exc:
                    raise CRIPTDeserializationUIDError("Unknown", unresolved_uid) from exc
                updated_attrs = dataclasses.replace(node._json_attrs, **{name: uid_node})
                node._update_json_attrs_if_valid(updated_attrs)

        for node_leaves in iterate_leaves(node_iter):
            if isinstance(node_leaves, BaseNode):
                for node in node_leaves:
                    field_names = [field.name for field in dataclasses.fields(node._json_attrs)]
                    for field_name in field_names:
                        field_attr = getattr(node._json_attrs, field_name)
                        handle_uid_replacement(node, field_name, field_attr)
                        if isinstance(field_attr, list):
                            for i in range(len(field_attr)):
                                if isinstance(field_attr[i], UIDProxy):
                                    try:
                                        field_attr[i] = self.uid_cache[field_attr[i].uid]
                                    except KeyError as exc:
                                        raise CRIPTDeserializationUIDError("Unknown", field_attr[i].uid) from exc
        return node_iter


def load_nodes_from_json(nodes_json: Union[str, Dict], api=None, _use_uuid_cache: Optional[Dict] = None, skip_validation: bool = False):
    """
    User facing function, that return a node and all its children from a json string input.

    Parameters
    ----------
    nodes_json: Union[str, dict]
        JSON string representation of a CRIPT node

    Examples
    --------
    >>> import cript
    >>> # Get updated project from API
    >>> my_paginator = api.search(
    ...     node_type=cript.Project,
    ...     search_mode=cript.SearchModes.EXACT_NAME,
    ...     value_to_search="my project name",
    ... ) # doctest: +SKIP
    >>> # Take specific Project you want from paginator
    >>> my_project_from_api_dict: dict = my_paginator.current_page_results[0] # doctest: +SKIP
    >>> # Deserialize your Project dict into a Project node
    >>> my_project_node_from_api = cript.load_nodes_from_json( # doctest: +SKIP
    ...     nodes_json=my_project_from_api_dict
    ... )

    Raises
    ------
    CRIPTJsonNodeError
        If there is an issue with the JSON of the node field.
    CRIPTJsonDeserializationError
        If there is an error during deserialization of a specific node.
    CRIPTDeserializationUIDError
        If there is an issue with the UID used for deserialization, like circular references.

    Notes
    -----
    This function uses a custom `_NodeDecoderHook` to convert JSON nodes into Python objects.
    The `_NodeDecoderHook` class is responsible for handling the deserialization of nodes
    and caching objects with shared UIDs to avoid redundant deserialization.

    The function is intended for deserializing CRIPT nodes and should not be used for generic JSON.

    Returns
    -------
    Union[CRIPT Node, List[CRIPT Node]]
        Typically returns a single CRIPT node,
        but if given a list of nodes, then it will serialize them and return a list of CRIPT nodes
    """
    from cript.api.api import _get_global_cached_api

    if api is None:
        api = _get_global_cached_api()

    # Initialize the custom decoder hook for JSON deserialization
    node_json_hook = _NodeDecoderHook()

    # Convert everything into a string. This is slightly inefficient for already encoded dicts,
    # but catches a lot of odd cases. And at the moment performance is not bottle necked here
    if not isinstance(nodes_json, str):
        nodes_json = json.dumps(nodes_json)

    # Store previous UUIDBaseNode Cache state
    previous_uuid_cache = UUIDBaseNode._uuid_cache

    if _use_uuid_cache is not None:  # If requested use a custom cache.
        UUIDBaseNode._uuid_cache = _use_uuid_cache

    previous_skip_validation = api.schema.skip_validation
    # Temporarily disable validation while loading nodes from JSON
    api.schema.skip_validation = True
    try:
        loaded_nodes = json.loads(nodes_json, object_hook=node_json_hook)
        loaded_nodes = node_json_hook.resolve_unresolved_uids(loaded_nodes)
    finally:
        # Definitively restore the old cache state
        UUIDBaseNode._uuid_cache = previous_uuid_cache
        api.schema.skip_validation = previous_skip_validation

    # If nodes are actually expected to be checked, do it now
    if not previous_skip_validation and not skip_validation:
        for node in iterate_leaves(loaded_nodes):
            if isinstance(node, BaseNode):
                node.validate()

    if _use_uuid_cache is not None:
        return loaded_nodes, _use_uuid_cache
    return loaded_nodes


def _rename_field(serialize_dict: Dict, old_name: str, new_name: str) -> Dict:
    """
    renames `property_` to `property` the JSON
    """
    if "property_" in serialize_dict:
        serialize_dict[new_name] = serialize_dict.pop(old_name)

    return serialize_dict


def _is_node_field_valid(node_type_list: List) -> bool:
    """
    a simple function that checks if the node field has only a single node type in there
    and not 2 or None

    Parameters
    ----------
    node_type_list: List
        e.g. "node": ["Material"]

    Returns
    ------
    bool
        if all tests pass then it returns true, otherwise false
    """

    # TODO consider having exception handling for the dict
    if isinstance(node_type_list, list) and len(node_type_list) == 1 and isinstance(node_type_list[0], str) and len(node_type_list[0]) > 0:
        return True
    else:
        return False
