from dataclasses import dataclass, replace

from cript.nodes.core import BaseNode


def _is_local_file(file_source: str) -> bool:
    """
    determines if the file the user is uploading is a local file or a link

    Parameters
    ----------
    file_source: str

    Returns
    -------
    bool
    """

    # checking "http" so it works with both "https://" and "http://"
    if file_source.startswith("http"):
        return False
    else:
        return True


class File(BaseNode):
    """
    [File node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=28)
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all file attributes
        """

        source: str = ""
        type_: str = ""
        extension: str = ""
        data_dictionary: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, source: str, type_: str, extension: str = "", data_dictionary: str = "", **kwargs):
        super().__init__(node="File")

        # TODO check if vocabulary is valid or not
        # is_vocab_valid("file type", type)

        # setting every attribute except for source, which will be handled via setter
        self._json_attrs = replace(
            self._json_attrs,
            type_=type_,
            extension=extension,
            data_dictionary=data_dictionary,
        )

        self.source = source

        self.validate()

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

        1. checks if the file source is a link or a local file path
        2. if the source is a link such as `https://wikipedia.com` then it sets the URL as the file source
        3. if the file source is a local file path such as
                `C:\\Users\\my_username\\Desktop\\cript\\file.txt`
            1. then it opens the file and reads it
            2. uploads it to the cloud storage
            3. gets back a URL from where in the cloud the file is found
            4. sets that as the source

        Parameters
        ----------
        new_source: str

        Returns
        -------
        None
        """

        if _is_local_file(new_source):
            with open(new_source, "r") as file:
                # TODO upload a file to Argonne Labs or directly to the backend
                #   get the URL of the uploaded file
                #   set the source to the URL just gotten from argonne
                print(file)
                pass

        new_attrs = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def type_(self) -> str:
        """
        get file type

        file type must come from CRIPT controlled vocabulary

        Returns
        -------
        str
            file type
        """
        return self._json_attrs.type_

    @type_.setter
    def type_(self, new_type_) -> None:
        """
        sets the file type

        file type must come from CRIPT controlled vocabulary

        Parameters
        ----------
        new_type_

        Returns
        -------
        None
        """
        # TODO check vocabulary is valid
        # is_vocab_valid("file type", self._json_attrs.type)
        new_attrs = replace(self._json_attrs, type_=new_type_)
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
