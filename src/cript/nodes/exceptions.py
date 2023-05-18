from abc import ABC, abstractmethod

from cript.exceptions import CRIPTException


class CRIPTNodeSchemaError(CRIPTException):
    """
    Exception that is raised when a DB schema validation fails for a node.
    """

    error_message: str

    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class CRIPTJsonDeserializationError(CRIPTException):
    """
    Exception to throw if deserialization of nodes fails.

    """

    def __init__(self, node_type: str, json_str: str):
        self.node_type = node_type
        self.json_str = json_str

    def __str__(self):
        return f"JSON deserialization failed for node type {self.node_type} with JSON str: {self.json_str}"


class CRIPTJsonNodeError(CRIPTJsonDeserializationError):
    """
    Exception that is raised if a `node` attribute is present, but not a single itemed list.
    """

    def __init__(self, node_list, json_str):
        self.node_list = node_list
        self.json_str = json_str

    def __str__(self):
        ret_str = f"Invalid JSON contains `node` attribute {self.node_list} but this is not a list with a single element."
        ret_str += " Expected is a single element list with the node name as a single string element."
        ret_str += f" Full json string was {self.json_str}."
        return ret_str


class CRIPTJsonSerializationError(CRIPTException):
    """
    Exception to throw if deserialization of nodes fails.

    """

    def __init__(self, node_type: str, json_dict: str):
        self.node_type = node_type
        self.json_str = str(json_dict)

    def __str__(self):
        return f"JSON Serialization failed for node type {self.node_type} with JSON dict: {self.json_str}"


class CRIPTAttributeModificationError(CRIPTException):
    """
    Exception that is thrown when a node attribute is modified, that wasn't intended to be modified.
    """

    def __init__(self, name, key, value):
        self.name = name
        self.key = key
        self.value = value

    def __str__(self):
        return (
            f"Attempt to modify an attribute of a node ({self.name}) that wasn't intended to be modified.\n"
            f"Here the non-existing attribute {self.key} of {self.name} was attempted to be modified.\n"
            "Most likely this is due to a typo in the attribute that was intended to be modified i.e. `project.materials` instead of `project.material`.\n"
            "To ensure compatibility with the underlying CRIPT data model we do not allow custom attributes.\n"
        )


class CRIPTExtraJsonAttributes(CRIPTException):
    def __init__(self, name_type: str, extra_attribute: str):
        self.name_type = name_type
        self.extra_attribute = extra_attribute

    def __str__(self):
        return (
            f"During the construction of a node {self.name_type} an additional attribute {self.extra_attribute} was detected.\n"
            "This might be a typo or an extra delivered argument from the back end.\n"
            f"In the latter case, you can disable this error temporarily by calling `cript.add_tolerated_extra_json('{self.extra_attribute}')`.\n"
        )


class CRIPTOrphanedNodesError(CRIPTException, ABC):
    """
    This error is raised when a child node is not attached to the
    appropriate parent node. For example, all material nodes used
    within a project must belong to the project inventory or are explictly listed as material of that project.
    If there is a material node that is used within a project but not a part of the
    inventory and the validation code finds it then it raises an `CRIPTOrphanedNodeError`

    Fixing this is simple and easy, just take the node that CRIPT Python SDK
    found a problem with and associate it with the appropriate parent via

    ```
    my_project.material += my_orphaned_material_node
    ```
    """

    def __init__(self, orphaned_node):
        self.orphaned_node = orphaned_node

    @abstractmethod
    def __str__(self):
        pass


class CRIPTOrphanedMaterialError(CRIPTOrphanedNodesError):
    """
    CRIPTOrphanedNodesError, but specific for orphaned materials.
    Handle this error by adding the orphaned materials into the parent project or its inventories.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.material import Material

        assert isinstance(orphaned_node, Material)
        super().__init__(orphaned_node)

    def __str__(self):
        ret_string = "While validating a project graph, an orphaned material node was found. "
        ret_string += "This material is present in the graph, but not listed in the project. "
        ret_string += "Please add the node like: `my_project.material += [orphaned_material]`. "
        ret_string += f"The orphaned material was {self.orphaned_node}."
        return ret_string


class CRIPTOrphanedExperimentError(CRIPTOrphanedNodesError):
    """
    CRIPTOrphanedNodesError, but specific for orphaned nodes that should be listed in one of the experiments.
    Handle this error by adding the orphaned node into one the parent project's experiments.
    """

    def __init__(self, orphaned_node):
        super().__init__(orphaned_node)

    def __str__(self) -> str:
        node_name = self.orphaned_node.node_type.lower()
        ret_string = f"While validating a project graph, an orphaned {node_name} node was found. "
        ret_string += f"This {node_name} node is present in the graph, but not listed in any of the experiments of the  project. "
        ret_string += f"Please add the node like: `your_experiment.{node_name} += [orphaned_{node_name}]`. "
        ret_string += f"The orphaned {node_name} was {self.orphaned_node}."
        return ret_string


def get_orphaned_experiment_exception(orphaned_node):
    """
    Return the correct specific Exception based in the orphaned node type for nodes not correctly listed in experiment.
    """
    from cript.nodes.primary_nodes.computation import Computation
    from cript.nodes.primary_nodes.computation_process import ComputationProcess
    from cript.nodes.primary_nodes.data import Data
    from cript.nodes.primary_nodes.process import Process

    if isinstance(orphaned_node, Data):
        return CRIPTOrphanedDataError(orphaned_node)
    if isinstance(orphaned_node, Process):
        return CRIPTOrphanedProcessError(orphaned_node)
    if isinstance(orphaned_node, Computation):
        return CRIPTOrphanedComputationError(orphaned_node)
    if isinstance(orphaned_node, ComputationProcess):
        return CRIPTOrphanedComputationalProcessError(orphaned_node)
    # Base case raise the parent exception. TODO add bug warning.
    return CRIPTOrphanedExperimentError(orphaned_node)


class CRIPTOrphanedDataError(CRIPTOrphanedExperimentError):
    """
    CRIPTOrphanedExeprimentError, but specific for orphaned Data node that should be listed in one of the experiments.
    Handle this error by adding the orphaned node into one the parent project's experiments `data` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.data import Data

        assert isinstance(orphaned_node, Data)
        super().__init__(orphaned_node)


class CRIPTOrphanedProcessError(CRIPTOrphanedExperimentError):
    """
    CRIPTOrphanedExeprimentError, but specific for orphaned Process node that should be listed in one of the experiments.
    Handle this error by adding the orphaned node into one the parent project's experiments `process` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.process import Process

        assert isinstance(orphaned_node, Process)
        super().__init__(orphaned_node)


class CRIPTOrphanedComputationError(CRIPTOrphanedExperimentError):
    """
    CRIPTOrphanedExeprimentError, but specific for orphaned Computation node that should be listed in one of the experiments.
    Handle this error by adding the orphaned node into one the parent project's experiments `Computation` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.computation import Computation

        assert isinstance(orphaned_node, Computation)
        super().__init__(orphaned_node)


class CRIPTOrphanedComputationalProcessError(CRIPTOrphanedExperimentError):
    """
    CRIPTOrphanedExeprimentError, but specific for orphaned ComputationalProcess node that should be listed in one of the experiments.
    Handle this error by adding the orphaned node into one the parent project's experiments `ComputationalProcess` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.computation_process import ComputationProcess

        assert isinstance(orphaned_node, ComputationProcess)
        super().__init__(orphaned_node)
