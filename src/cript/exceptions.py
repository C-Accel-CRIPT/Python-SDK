from abc import abstractmethod


class CRIPTException(Exception):
    """
    Parent CRIPT exception.
    All CRIPT exception inherit this class.
    """

    @abstractmethod
    def __str__(self) -> str:
        pass


class CRIPTWarning(Warning):
    """
    Parent CRIPT warning.
    All CRIPT warning inherit this class.
    """

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self):
        return str(self)
