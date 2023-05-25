from abc import ABC, abstractmethod
from typing import List

from cript.exceptions import CRIPTException


class CRIPTNodeSchemaError(CRIPTException):
    """
    ## Definition
    This error is raised when the CRIPT [json database schema](https://json-schema.org/)
    validation fails for a node.

    Please keep in mind that the CRIPT Python SDK converts all the Python nodes inside the
    [Project](../../nodes/primary_nodes/project) into a giant JSON
    and sends an HTTP `POST` or `PATCH` request to the API to be processed.

    However, before a request is sent to the API, the JSON is validated against API database schema
    via the [JSON Schema library](https://python-jsonschema.readthedocs.io/en/stable/),
    and if the database schema validation fails for whatever reason this error is shown.

    ### Possible Reasons

    1. There was a mistake in nesting of the nodes
    1. There was a mistake in creating the nodes
    1. Nodes are missing
    1. Nodes have invalid vocabulary
        * The database schema wants something a different controlled vocabulary than what is provided
    1. There was an error with the way the JSON was created within the Python SDK
        * The format of the JSON the CRIPT Python SDK created was invalid
    1. There is something wrong with the database schema

    ## How to Fix
    The easiest way to troubleshoot this is to examine the JSON that the SDK created via printing out the
    [Project](../../nodes/primary_nodes/project) node's JSON and checking the place that the schema validation
    says failed

    ### Example
    ```python
    print(my_project.json)
    ```
    """

    node_type: str = ""
    json_schema_validation_error: str = ""

    def __init__(self, node_type: str, json_schema_validation_error: str) -> None:
        self.json_schema_validation_error: str = json_schema_validation_error
        self.node_type = node_type

    def __str__(self) -> str:
        error_message: str = f"JSON database schema validation for node {self.node_type} failed."
        error_message += f"Error: {self.json_schema_validation_error}"

        return error_message


class CRIPTJsonDeserializationError(CRIPTException):
    """
    ## Definition
    This exception is raised when converting a node from JSON to Python class fails.
    This process fails when the attributes within the JSON does not match the node's class
    attributes within the `JsonAttributes` of that specific node

    ### Error Example
    Invalid JSON that cannot be deserialized to a CRIPT Python SDK Node

    ```json
    ```


    ### Valid Example
    Valid JSON that can be deserialized to a CRIPT Python SDK Node

    ```json
    ```

    ## How to Fix
    """

    def __init__(self, node_type: str, json_str: str) -> None:
        self.node_type = node_type
        self.json_str = json_str

    def __str__(self) -> str:
        return f"JSON deserialization failed for node type {self.node_type} with JSON str: {self.json_str}"


class CRIPTJsonNodeError(CRIPTJsonDeserializationError):
    """
    ## Definition
    This exception is raised if a `node` attribute is present in JSON,
    but the list has more or less than exactly one type of node type.

    > Note: It is expected that there is only a single node type per JSON object.

    ### Example
    !!! Example "Valid JSON representation of a Material node"
        ```json
        {
          "node": [
            "Material"
          ],
          "name": "Whey protein isolate",
          "uid": "_:Whey protein isolate"
        },
        ```

    ??? Example "Invalid JSON representation of a Material node"

        ```json
        {
          "node": [
            "Material",
            "Property"
          ],
          "name": "Whey protein isolate",
          "uid": "_:Whey protein isolate"
        },
        ```

        ---

        ```json
        {
          "node": [],
          "name": "Whey protein isolate",
          "uid": "_:Whey protein isolate"
        },
        ```


    ## How to Fix
    Debugging skills are most helpful here as there is no one-size-fits-all approach.

    It is best to identify whether the invalid JSON was created in the Python SDK
    or if the invalid JSON was given from the API.

    If the Python SDK created invalid JSON during serialization, then it is helpful to track down and
    identify the point where the invalid JSON was started.

    You may consider, inspecting the python objects to see if the node type are written incorrectly in python
    and the issue is only being caught during serialization or if the Python node is written correctly
    and the issue is created during serialization.

    If the problem is with the Python SDK or API, it is best to leave an issue or create a discussion within the
    [Python SDK GitHub repository](https://github.com/C-Accel-CRIPT/Python-SDK) for one of the members of the
    CRIPT team to look into any issues that there could have been.
    """

    def __init__(self, node_list: List, json_str: str) -> None:
        self.node_list = node_list
        self.json_str = json_str

    def __str__(self) -> str:
        error_message: str = (
            f"The 'node' attribute in the JSON string must be a single element list with the node name "
            f" such as `'node: ['Material']`. The `node` attribute provided was: `{self.node_list}`"
            f"The full JSON was: {self.json_str}."
        )

        return error_message


class CRIPTJsonSerializationError(CRIPTException):
    """
    ## Definition
    This Exception is raised if serialization of node from JSON to Python Object fails.

    ## How to Fix
    """

    def __init__(self, node_type: str, json_dict: str) -> None:
        self.node_type = node_type
        self.json_str = str(json_dict)

    def __str__(self) -> str:
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
    ## Definition
    This error is raised when a child node is not attached to the
    appropriate parent node. For example, all material nodes used
    within a project must belong to the project inventory or are explicitly listed as material of that project.
    If there is a material node that is used within a project but not a part of the
    inventory and the validation code finds it then it raises an `CRIPTOrphanedNodeError`

    ## How To Fix
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
    ## Definition
    CRIPTOrphanedNodesError, but specific for orphaned materials.

    ## How To Fix
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
    ## Definition
    CRIPTOrphanedNodesError, but specific for orphaned nodes that should be listed in one of the experiments.

    ## How To Fix
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
    ## Definition
    CRIPTOrphanedExeprimentError, but specific for orphaned Data node that should be listed in one of the experiments.

    ## How To Fix
    Handle this error by adding the orphaned node into one the parent project's experiments `data` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.data import Data

        assert isinstance(orphaned_node, Data)
        super().__init__(orphaned_node)


class CRIPTOrphanedProcessError(CRIPTOrphanedExperimentError):
    """
    ## Definition
    CRIPTOrphanedExeprimentError, but specific for orphaned Process node that should be
    listed in one of the experiments.

    ## How To Fix
    Handle this error by adding the orphaned node into one the parent project's experiments
    `process` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.process import Process

        assert isinstance(orphaned_node, Process)
        super().__init__(orphaned_node)


class CRIPTOrphanedComputationError(CRIPTOrphanedExperimentError):
    """
    ## Definition
    CRIPTOrphanedExeprimentError, but specific for orphaned Computation node that should be
    listed in one of the experiments.

    ## How To Fix
    Handle this error by adding the orphaned node into one the parent project's experiments
    `Computation` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.computation import Computation

        assert isinstance(orphaned_node, Computation)
        super().__init__(orphaned_node)


class CRIPTOrphanedComputationalProcessError(CRIPTOrphanedExperimentError):
    """
    ## Definition
    CRIPTOrphanedExeprimentError, but specific for orphaned ComputationalProcess
    node that should be listed in one of the experiments.

    ## How To Fix
    Handle this error by adding the orphaned node into one the parent project's experiments
    `ComputationalProcess` attribute.
    """

    def __init__(self, orphaned_node):
        from cript.nodes.primary_nodes.computation_process import ComputationProcess

        assert isinstance(orphaned_node, ComputationProcess)
        super().__init__(orphaned_node)
