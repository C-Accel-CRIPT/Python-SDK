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
