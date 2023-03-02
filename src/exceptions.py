class ConnectionError(Exception):
    """
    Raised when API object cannot connect to CRIPT with the give host and token
    """

    def __init__(self):
        pass

    def __str__(self):
        return "Could not connect to CRIPT with the given host and token. Please be sure both host and token are correct."
