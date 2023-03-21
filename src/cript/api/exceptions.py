
class CRIPTConnectionError(Exception):
    """
    Raised when the API object cannot connect to CRIPT with the given host and token
    """

    def __init__(self, host, token):
        self.host = host
        # Do not store full token in stack trace for security reasons
        uncovered_chars = len(token)//4
        self.token = token[:uncovered_chars]
        self.token += "*"*(len(token)-2*uncovered_chars)
        self.token += token[-uncovered_chars:]

    def __str__(self) -> str:
        """

        Returns
        -------
        str
            Explanation of the error
        """

        ret_str = f"Could not connect to CRIPT with the given host ({self.host}) and token ({self.token})."
        ret_str += " Please be sure both host and token are entered correctly."
        return ret_str


class InvalidVocabulary(Exception):
    """
    Raised when the CRIPT controlled vocabulary is invalid
    """

    # TODO add a the correct URL here
    vocab_URL: str = "https://cript.org/controlled-vocabulary"

    def __init__(self):
        pass

    def __str__(self) -> str:
        ret_str = "The vocabulary entered does not exist within the CRIPT controlled vocabulary."
        ret_str += f" Please pick a valid CRIPT vocabulary from {self.vocab_URL}"
        return ret_str


class CRIPTAPIAccessError(Exception):
    """
    Exception to be raise when the cached API object is requested, but no cached API exists yet.
    """
    def __init__(self):
        pass
    def __str__(self) -> str:
        ret_str = "An operation you requested (see stack trace) requires that you connect to a CRIPT host via an cript.API object first.\n"
        ret_str += "This is common for node creation, validation and modification.\n"
        ret_str += "It is necessary that you connect with the API via a context manager like this:\n"
        ret_str += "`with cript.API('https://criptapp.org/', secret_token) as api:\n"
        ret_str += "\t# code that use the API object explicitly (`api.save(..)`) or implicitly (`cript.Experiment(...)`)."
        ret_str += "See documentation of cript.API for more details."
        return ret_str
