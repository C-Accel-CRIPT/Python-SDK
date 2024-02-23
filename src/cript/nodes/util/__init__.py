from cript.nodes.exceptions import (
    CRIPTOrphanedComputationalProcessError,
    CRIPTOrphanedComputationError,
    CRIPTOrphanedDataError,
    CRIPTOrphanedMaterialError,
    CRIPTOrphanedProcessError,
)
from cript.nodes.primary_nodes.experiment import Experiment
from cript.nodes.primary_nodes.project import Project

# trunk-ignore-begin(ruff/F401)
from .json import NodeEncoder, load_nodes_from_json

# trunk-ignore-end(ruff/F401)


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
