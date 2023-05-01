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


class CRIPTOrphranedNodesError(CRIPTException, ABC):
    def __init__(self, orphraned_node: "BaseNode"):
        self.orphaned_node = orphraned_node

    @abstractmethod
    def __str__(self):
        pass


class CRIPTOrphranedMaterialError(CRIPTOrphranedNodesError):
    def __init__(self, orphaned_node: "Material"):
        super().__init__(orphaned_node)

    def __str__(self):
        ret_string = "While validating a project graph, an orphraned material node was found. "
        ret_string += "This material is present in the graph, but not listed in the project. "
        ret_string += "Please add the node like: `your_project.materials += [orphaned_material]`. "
        ret_string += f"The orphraned material was {self.orphraned_node}."
        return ret_string


class CRIPTOrphranedExperimentError(CRIPTOrphranedNodesError):
    def __init__(self, orphaned_node):
        super().__init__(orphaned_node)

    def __str__(self):
        node_name = self.orphaned_node.node_type.lower()
        ret_string = f"While validating a project graph, an orphraned {node_name} node was found. "
        ret_string += f"This {node_name} node is present in the graph, but not listed in any experiment of the  project. "
        ret_string += f"Please add the node like: `your_experiment.{node_name} += [orphaned_{node_name}]`. "
        ret_string += f"The orphraned {node_name} was {self.orphraned_node}."
        return ret_string
