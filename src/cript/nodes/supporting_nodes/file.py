import os
from dataclasses import dataclass, replace
from typing import Union

from cript.nodes.core import BaseNode


def verify_file_source(file_source: str) -> Union[None, FileNotFoundError]:
    """
    checks if the file source is valid
    1. checks if the file is a link or path to file on local storage
        1. if source is link then it is considered valid
    2. if file source is not a path, then it tries to get the file
        1. if the file can be found then it returns None
        2. if file cannot be found on local storage then it throws an error

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        if file source is local path and file cannot be found on local storage
    """

    # checking "http" so it works with both "https://" and "http://"
    if file_source.startswith("http"):
        return None

    # if path to file on local storage
    if not os.path.exists(file_source):
        raise FileNotFoundError


class File(BaseNode):
    """
    File node
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all file attributes
        """

        source: str = ""
        type: str = ""
        extension: str = ""
        data_dictionary: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self, source: str, type: str, extension: str = "", data_dictionary: str = "", **kwargs
    ):
        super().__init__(node="File")
        verify_file_source(source)

        # TODO check if vocabulary is valid or not
        # is_vocab_valid("file type", type)

        self._json_attrs = replace(
            self._json_attrs,
            source=source,
            type=type,
            extension=extension,
            data_dictionary=data_dictionary,
        )
        self.validate()

    pass

    # TODO can be made into a function

    # --------------- Properties ---------------
    @property
    def source(self) -> str:
        """
        gets the source for the file node

        Returns
        -------
        str
            file source

        """
        return self._json_attrs.source

    @source.setter
    def source(self, new_source: str) -> None:
        """
        sets the source of the file node
        the source can either be a path to a file on local storage or a link to a file

        if the file source is a path to local file then it tries to check if it can find it
        and if it cannot then it throws an error saying that the file you pointed to does not
        exist

        Parameters
        ----------
        new_source

        Returns
        -------
        None
        """
        verify_file_source(new_source)
        new_attrs = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def type(self) -> str:
        """
        get file type

        Returns
        -------
        str
            file type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type) -> None:
        """
        sets the file type

        Parameters
        ----------
        new_type

        Returns
        -------
        None
        """
        # TODO check vocabulary is valid
        # is_vocab_valid("file type", self._json_attrs.type)
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def extension(self) -> str:
        """
        get the file extension

        Returns
        -------
        str
            file extension
        """
        return self._json_attrs.extension

    @extension.setter
    def extension(self, new_extension) -> None:
        """
        sets the new file extension

        Parameters
        ----------
        new_extension

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, extension=new_extension)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def data_dictionary(self) -> str:
        # TODO data dictionary needs documentation describing it and how to use it
        """
        gets the file attribute data_dictionary

        Returns
        -------
        str
            data_dictionary
        """
        return self._json_attrs.data_dictionary

    @data_dictionary.setter
    def data_dictionary(self, new_data_dictionary: str) -> None:
        """
        sets the data dictionary

        Parameters
        ----------
        new_data_dictionary

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data_dictionary=new_data_dictionary)
        self._update_json_attrs_if_valid(new_attrs)
