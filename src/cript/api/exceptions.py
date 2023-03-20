class CRIPTConnectionError(Exception):
    """
    Raised when the API object cannot connect to CRIPT with the given host and token
    """

    def __init__(self):
        pass

    def __str__(self) -> str:
        """

        Returns
        -------
        str
            Explanation of the error
        """
        return "Could not connect to CRIPT with the given host and token. Please be sure both host and token are entered correctly."


class InvalidVocabulary(Exception):
    """
    Raised when the CRIPT controlled vocabulary is invalid
    """
    # TODO add a the correct URL here
    vocab_URL: str = "https://cript.org/controlled-vocabulary"

    def __init__(self):
        pass

    def __str__(self) -> str:
        return f"The vocabulary entered does not exist within the CRIPT controlled vocabulary. Please pick a valid CRIPT vocabulary from {self.vocab_URL}"


class CRIPTAPIAccessError(Exception):
    """
    Exception to be raise when the cached API object is requested, but no cached API exists yet.
    """
    def __init__(self):
        pass
    def __str__(self) -> str:
        ret_str = "An operation you requested (see stack trace) requires that you connect to a CRIPT host via an cript.API object first.\n"
        ret_str +=
