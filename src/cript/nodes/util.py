import inspect
import json
from dataclasses import asdict

import cript.nodes
from cript.nodes.core import BaseNode
from cript.nodes.exceptions import (
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
    handled_ids = set()

    def default(self, obj):
        if isinstance(obj, BaseNode):
            try:
                uid = obj.uid
            except AttributeError:
                pass
            else:
                if uid in NodeEncoder.handled_ids:
                    return {"node": obj._json_attrs.node, "uid": uid}
                NodeEncoder.handled_ids.add(uid)
            default_values = asdict(obj.JsonAttributes())
            serialize_dict = {}
            # Remove default values from serialization
            for key in default_values:
                if key in obj._json_attrs.__dataclass_fields__:
                    if getattr(obj._json_attrs, key) != default_values[key]:
                        serialize_dict[key] = getattr(obj._json_attrs, key)
            serialize_dict["node"] = obj._json_attrs.node
            return serialize_dict
        return json.JSONEncoder.default(self, obj)


def _node_json_hook(node_str: str):
    """
    Internal function, used as a hook for json deserialization.
    """
    node_dict = dict(node_str)
    try:
        node_list = node_dict["node"]
    except KeyError:  # Not a node, just a regular dictionary
        return node_dict

    if isinstance(node_list, list) and len(node_list) == 1 and isinstance(node_list[0], str):
        node_str = node_list[0]
    else:
        raise CRIPTJsonNodeError(node_list, node_str)

    # Iterate over all nodes in cript to find the correct one here
    for key, pyclass in inspect.getmembers(cript.nodes, inspect.isclass):
        if BaseNode in inspect.getmro(pyclass):
            if key == node_str:
                try:
                    return pyclass._from_json(node_dict)
                except Exception as exc:
                    raise CRIPTJsonDeserializationError(key, node_str) from exc
    # Fall back
    return node_dict


def load_nodes_from_json(nodes_json: str):
    """
    User facing function, that return a node and all its children from a json input.
    """
    return json.loads(nodes_json, object_hook=_node_json_hook)


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
            # beccause calling the setter calls `validate` we have to force add the material.
            project._json_attrs.material.append(exc.orphaned_node)
        except CRIPTOrphanedDataError as exc:
            active_experiment.data += [exc.orphaned_node]
        except CRIPTOrphanedProcessError as exc:
            active_experiment.process += [exc.orphaned_node]
        except CRIPTOrphanedComputationError as exc:
            active_experiment.computation += [exc.orphaned_node]
        except CRIPTOrphanedComputationalProcessError as exc:
            active_experiment.computational_process += [exc.orphaned_node]
        else:
            break
        counter += 1
