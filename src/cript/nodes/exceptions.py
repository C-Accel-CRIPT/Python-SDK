class CRIPTNodeSchemaError(Exception):
    """
    Exception that is raised when a DB schema validation fails for a node.

    This is a dummy implementation.
    This needs to be way more sophisticated for good error reporting.
    """

    def __init__(self):
        pass

    def __str__(self):
        return "Dummy Schema validation failed. TODO replace with actual implementation."


class CRIPTJsonDeserializationError(Exception):
    """
    Exception to throw if deserialization of nodes fails.

    """

    def __init__(self, node_type: str, json_str: str):
        self.node_type = node_type
        self.json_str = json_str

    def __str__(self):
        return f"JSON deserialization failed for node type {self.node_type} with JSON str: {self.json_str}"


class CRIPTJsonSerializationError(Exception):
    """
    Exception to throw if deserialization of nodes fails.

    """

    def __init__(self, node_type: str, json_dict: str):
        self.node_type = node_type
        self.json_str = str(json_dict)

    def __str__(self):
        return f"JSON Serialization failed for node type {self.node_type} with JSON dict: {self.json_str}"


class UneditableAttributeError(Exception):
    """
    This exception is raised when the user attempts to edit a read only field
    that they do not have permissions to edit, or they cannot edit through the Python SDK
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        """
        Error Message
        Returns
        -------
        str:
            Error message
        """
        # TODO documentation needed to explain this error, when it applies, and how to edit
        #   the node if needed
        return "This node attribute cannot be edited."
