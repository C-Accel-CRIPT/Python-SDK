class CRIPTNodeSchemaError(Exception):
    """
    Exception that is raised when a DB schema validation fails for a node.

    This is a dummy implementation. This needs to be way more sophisticated for good error reporting.
    """

    def __init__(self):
        pass

    def __str__(self):
        return (
            "Dummy Schema validation failed. TODO replace with actual implementation."
        )


class UneditableNodeError(Exception):
    """
    This exception is raised when the user attempts to edit a node
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
        return "This node cannot be edited."


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
