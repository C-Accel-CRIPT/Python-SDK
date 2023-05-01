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
