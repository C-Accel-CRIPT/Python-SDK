import uuid
import warnings

from cript.nodes.exceptions import (
    CRIPTOrphanedComputationalProcessWarning,
    CRIPTOrphanedComputationWarning,
    CRIPTOrphanedDataWarning,
    CRIPTOrphanedExperimentWarning,
    CRIPTOrphanedMaterialWarning,
    CRIPTOrphanedProcessWarning,
)


def get_uuid_from_uid(uid):
    return str(uuid.UUID(uid[2:]))


def add_orphaned_nodes_to_project(project, active_experiment, max_iteration: int = -1):
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
    # Convert Errors into exceptions, so we can catch and fix them
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        while True:
            if counter > max_iteration >= 0:
                break  # Emergency stop
            try:
                project.validate()
            except CRIPTOrphanedMaterialWarning as exc:
                # because calling the setter calls `validate` we have to force add the material.
                project._json_attrs.material.append(exc.orphaned_node)
            except CRIPTOrphanedDataWarning as exc:
                active_experiment.data += [exc.orphaned_node]
            except CRIPTOrphanedProcessWarning as exc:
                active_experiment.process += [exc.orphaned_node]
            except CRIPTOrphanedComputationWarning as exc:
                active_experiment.computation += [exc.orphaned_node]
            except CRIPTOrphanedComputationalProcessWarning as exc:
                active_experiment.computation_process += [exc.orphaned_node]
            else:
                break
            counter += 1


def get_orphaned_experiment_exception(orphaned_node):
    """
    Return the correct specific Exception based in the orphaned node type for nodes not correctly listed in experiment.
    """
    from cript.nodes.primary_nodes.computation import Computation
    from cript.nodes.primary_nodes.computation_process import ComputationProcess
    from cript.nodes.primary_nodes.data import Data
    from cript.nodes.primary_nodes.process import Process

    if isinstance(orphaned_node, Data):
        return CRIPTOrphanedDataWarning(orphaned_node)
    if isinstance(orphaned_node, Process):
        return CRIPTOrphanedProcessWarning(orphaned_node)
    if isinstance(orphaned_node, Computation):
        return CRIPTOrphanedComputationWarning(orphaned_node)
    if isinstance(orphaned_node, ComputationProcess):
        return CRIPTOrphanedComputationalProcessWarning(orphaned_node)
    # Base case raise the parent exception. TODO add bug warning.
    return CRIPTOrphanedExperimentWarning(orphaned_node)


def iterate_leaves(obj):
    """Helper function that iterates over all leaves of nested dictionaries or lists."""

    if isinstance(obj, dict):
        for value in obj.values():
            yield from iterate_leaves(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iterate_leaves(item)
    else:
        yield obj
