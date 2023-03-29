from abc import abstractmethod


class CRIPTException(Exception):
    """
    Parent CRIPT exception.
    All CRIPT exception inherit this clas.
    """

    @abstractmethod
    def __str__(self) -> str:
        pass
