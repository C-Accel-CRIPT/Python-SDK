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

    ## How to Troubleshoot
    The easiest way to troubleshoot this is to examine the JSON that the SDK created via printing out the
    [Project](../../nodes/primary_nodes/project) node's JSON and checking the place that the schema validation
    says failed

    ### Example
    ```python
    print(my_project.json)
    ```
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
