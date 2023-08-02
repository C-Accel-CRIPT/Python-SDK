import copy
import inspect
import json
import uuid
from dataclasses import asdict
from typing import Dict, Optional, Set, Union

import cript.nodes
from cript.nodes.core import BaseNode
from cript.nodes.exceptions import (
    CRIPTDeserializationUIDError,
    CRIPTJsonDeserializationError,
    CRIPTJsonNodeError,
    CRIPTOrphanedComputationalProcessError,
    CRIPTOrphanedComputationError,
    CRIPTOrphanedDataError,
    CRIPTOrphanedMaterialError,
    CRIPTOrphanedProcessError,
)
from cript.nodes.primary_nodes.experiment import Experiment
from cript.nodes.primary_nodes.project import Project


class NodeEncoder(json.JSONEncoder):
    handled_ids: Set[str] = set()
    known_uuid: Set[str] = set()
    condense_to_uuid: Set[str] = set()
    suppress_attributes: Optional[Dict[str, Set[str]]] = None

    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, BaseNode):
            try:
                uid = obj.uid
            except AttributeError:
                pass
            else:
                if uid in NodeEncoder.handled_ids:
                    return {"node": obj._json_attrs.node, "uid": uid}

            # When saving graphs, some nodes can be pre-saved.
            # If that happens, we want to represent them as a UUID edge only
            try:
                uuid_str = str(obj.uuid)
            except AttributeError:
                pass
            else:
                if uuid_str in NodeEncoder.known_uuid:
                    return {"uuid": uuid_str}

            default_values = asdict(obj.JsonAttributes())
            serialize_dict = {}
            # Remove default values from serialization
            for key in default_values:
                if key in obj._json_attrs.__dataclass_fields__:
                    if getattr(obj._json_attrs, key) != default_values[key]:
                        serialize_dict[key] = copy.copy(getattr(obj._json_attrs, key))
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

    def _apply_modifications(self, serialize_dict):
        """
        Checks the serialize_dict to see if any other operations are required before it
        can be considered done. If other operations are required, then it passes it to the other operations
        and at the end returns the fully finished dict.

        This function is essentially a big switch case that checks the node type
        and determines what other operations are required for it.

        Parameters
        ----------
        serialize_dict: dict

        Returns
        -------
        serialize_dict: dict
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
            if isinstance(attribute, list):
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

        uid_of_condensed = []

        nodes_to_condense = serialize_dict["node"]
        for node_type in nodes_to_condense:
            if node_type in self.condense_to_uuid:
                attributes_to_process = self.condense_to_uuid[node_type]
                for attribute in attributes_to_process:
                    if attribute in serialize_dict:
                        attribute_to_condense = serialize_dict[attribute]
                        processed_attribute = process_attribute(attribute_to_condense)
                        serialize_dict[attribute] = processed_attribute

        # Check if the node is "Material" and convert the identifiers list to JSON fields
        if serialize_dict["node"] == ["Material"]:
            serialize_dict = _material_identifiers_list_to_json_fields(serialize_dict)

        return serialize_dict, uid_of_condensed


class _UIDProxy:
    """
    Proxy class for unresolvable UID nodes.
    This is going to be replaced by actual nodes.

    Report a bug if you find this class in production.
    """

    def __init__(self, uid: str):
        self.uid = uid
        print("proxy", uid)


class _NodeDecoderHook:
    def __init__(self, uid_cache: Optional[Dict] = None):
        """
        Initialize the custom JSON object hook used for CRIPT node deserialization.

        Parameters
        ----------
        uid_cache : Optional[Dict], optional
            A dictionary to cache Python objects with shared UIDs, by default None.

        Notes
        -----
        The `_NodeDecoderHook` class is used as an object hook for JSON deserialization,
        handling the conversion of JSON nodes into Python objects based on their node types.
        The `uid_cache` is an optional dictionary to store cached objects with shared UIDs
        to avoid unnecessary deserialization and circular references.


        """
        if uid_cache is None:
            uid_cache = {}
        self._uid_cache = uid_cache

    def __call__(self, node_str: Union[dict, str]) -> dict:
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
        node_str : Union[dict, str]
            The JSON representation of a node or a regular dictionary.

        Returns
        -------
        dict
            A Python dictionary representing the deserialized node or the input dictionary itself.

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
        if len(node_dict) == 2 and "uid" in node_dict and "node" in node_dict:
            try:
                return self._uid_cache[node_dict["uid"]]
            except KeyError:
                # TODO if we convince beartype to accept Proxy temporarily, enable return instead of raise
                raise CRIPTDeserializationUIDError(node_dict["node"], node_dict["uid"])
                # return _UIDProxy(node_dict["uid"])

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


def _material_identifiers_list_to_json_fields(serialize_dict: dict) -> dict:
    """
    input:
    ```json
        {
            "node":["Material"],
            "name":"my material",
            "identifiers":[ {"cas":"my material cas"} ],
            "uid":"_:a78203cb-82ea-4376-910e-dee74088cd37"
        }
    ```

    output:
    ```json
    {
        "node":["Material"],
        "name":"my material",
        "cas":"my material cas",
        "uid":"_:08018f4a-e8e3-4ac0-bdad-fa704fdc0145"
    }
    ```

    Parameters
    ----------
    serialize_dict: dict
        the serialized dictionary of the node

    Returns
    -------
    serialized_dict = dict
        new dictionary that has converted the list of dictionary identifiers into the dictionary as fields

    """

    # TODO this if statement might not be needed in future
    if "identifiers" in serialize_dict:
        for identifier in serialize_dict["identifiers"]:
            for key, value in identifier.items():
                serialize_dict[key] = value

        # remove identifiers list of objects after it has been flattened
        del serialize_dict["identifiers"]

    return serialize_dict


def _rename_field(serialize_dict: dict, old_name: str, new_name: str) -> dict:
    """
    renames `property_` to `property` the JSON
    """
    if "property_" in serialize_dict:
        serialize_dict[new_name] = serialize_dict.pop(old_name)

    return serialize_dict


def _is_node_field_valid(node_type_list: list) -> bool:
    """
    a simple function that checks if the node field has only a single node type in there
    and not 2 or None

    Parameters
    ----------
    node_type_list: list
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


def load_nodes_from_json(nodes_json: str):
    """
    User facing function, that return a node and all its children from a json input.
    """
    node_json_hook = _NodeDecoderHook()
    json_nodes = json.loads(nodes_json, object_hook=node_json_hook)

    # TODO: enable this logic to replace proxies, once beartype is OK with that.
    # def recursive_proxy_replacement(node, handled_nodes):
    #     if isinstance(node, _UIDProxy):
    #         try:
    #             node = node_json_hook._uid_cache[node.uid]
    #         except KeyError as exc:
    #             raise CRIPTDeserializationUIDError(node.node_type, node.uid)
    #         return node
    #     handled_nodes.add(node.uid)
    #     for field in node._json_attrs.__dict__:
    #         child_node = getattr(node._json_attrs, field)
    #         if not isinstance(child_node, list):
    #             if hasattr(cn, "__bases__") and BaseNode in child_node.__bases__:
    #                 child_node = recursive_proxy_replacement(child_node, handled_nodes)
    #                 node._json_attrs = replace(node._json_attrs, field=child_node)
    #         else:
    #             for i, cn in enumerate(child_node):
    #                 if hasattr(cn, "__bases__") and BaseNode in cn.__bases__:
    #                     if cn.uid not in handled_nodes:
    #                         child_node[i] = recursive_proxy_replacement(cn, handled_nodes)

    #     return node
    # handled_nodes = set()
    # recursive_proxy_replacement(json_nodes, handled_nodes)
    return json_nodes


def add_orphaned_nodes_to_project(project: Project, active_experiment: Experiment, max_iteration: int = -1):
    """
    Helper function that adds all orphaned material nodes of the project graph to the
    `project.materials` attribute.
    Material additions only is permissible with `active_experiment is None`.
    This function also adds all orphaned data, process, computation and computational process nodes
    of the project graph to the `active_experiment`.
    This functions call `project.validate` and might raise Exceptions from there.
    """
    if active_experiment is not None and active_experiment not in project.find_children({"node": ["Experiment"]}):
        raise RuntimeError(f"The provided active experiment {active_experiment} is not part of the project graph. Choose an active experiment that is part of a collection of this project.")

    counter = 0
    while True:
        if counter > max_iteration >= 0:
            break  # Emergency stop
        try:
            project.validate()
        except CRIPTOrphanedMaterialError as exc:
            # because calling the setter calls `validate` we have to force add the material.
            project._json_attrs.material.append(exc.orphaned_node)
        except CRIPTOrphanedDataError as exc:
            active_experiment.data += [exc.orphaned_node]
        except CRIPTOrphanedProcessError as exc:
            active_experiment.process += [exc.orphaned_node]
        except CRIPTOrphanedComputationError as exc:
            active_experiment.computation += [exc.orphaned_node]
        except CRIPTOrphanedComputationalProcessError as exc:
            active_experiment.computation_process += [exc.orphaned_node]
        else:
            break
        counter += 1
