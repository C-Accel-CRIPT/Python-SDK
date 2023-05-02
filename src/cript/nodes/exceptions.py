from cript.exceptions import CRIPTException
from cript.nodes.core import BaseNode


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

    # TODO accept both node type string and the actual node to get the node typ from
    # TODO fix how this error is raised
    def __init__(self, node: BaseNode, json_schema_validation_error: str) -> None:
        # get the node type from node e.g. "Project" or "Material"
        self.node_type = node.node_type[0].title()
        self.json_schema_validation_error: str = json_schema_validation_error

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
    """

    def __init__(self, node_type: str, json_str: str) -> None:
        self.node_type = node_type
        self.json_str = json_str

    def __str__(self) -> str:
        return f"JSON deserialization failed for node type {self.node_type} with JSON str: {self.json_str}"


class CRIPTJsonNodeError(CRIPTJsonDeserializationError):
    """
    Exception that is raised if a `node` attribute is present, but not a single itemed list.
    """

    def __init__(self, node_list, json_str) -> None:
        self.node_list = node_list
        self.json_str = json_str

    def __str__(self) -> str:
        error_message: str = f"Invalid JSON contains `node` attribute {self.node_list} "
        error_message += "but this is not a list with a single element. "
        error_message += " Expected is a single element list with the node name as a single string element. "
        error_message += f" Full json string was {self.json_str}. "

        return error_message


class CRIPTJsonSerializationError(CRIPTException):
    """
    Exception to throw if deserialization of nodes fails.

    """

    def __init__(self, node_type: str, json_dict: str) -> None:
        self.node_type = node_type
        self.json_str = str(json_dict)

    def __str__(self) -> str:
        return f"JSON Serialization failed for node type {self.node_type} with JSON dict: {self.json_str}"
