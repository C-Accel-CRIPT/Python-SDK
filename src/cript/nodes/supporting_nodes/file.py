from dataclasses import dataclass, replace

from cript.nodes.uuid_base import UUIDBaseNode


def _is_local_file(file_source: str) -> bool:
    """
    Determines if the file the user is uploading is a local file or a link.

    Args:
        file_source (str): The source of the file.

    Returns:
        bool: True if the file is local, False if it's a link.
    """

    # checking "http" so it works with both "https://" and "http://"
    if file_source.startswith("http"):
        return False
    else:
        return True


class File(UUIDBaseNode):
    """
    ## Definition

    The [File node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001
    .pdf#page=28) provides a link to  scholarly work and allows users to specify in what way the work relates to that
    data. More specifically, users can specify that the data was directly extracted from, inspired by, derived from,
    etc.

    The file node is held in the [Data node](../../primary_nodes/data).

    ## Attributes

    | Attribute       | Type | Example                                                                                               | Description                                                                 | Required |
    |-----------------|------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------|
    | source          | str  | `"path/to/my/file"` or `"https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system"` | source to the file can be URL or local path                                 | True     |
    | type            | str  | `"logs"`                                                                                              | Pick from [CRIPT File Types](https://criptapp.org/keys/file-type/)          | True     |
    | extension       | str  | `".csv"`                                                                                              | file extension                                                              | False    |
    | data_dictionary | str  | `"my extra info in my data dictionary"`                                                               | set of information describing the contents, format, and structure of a file | False    |

    ## JSON
    ``` json
    {
        "node": "File",
        "source": "https://criptapp.org",
        "type": "calibration",
        "extension": ".csv",
        "data_dictionary": "my file's data dictionary",
    }
    ```

    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        """
        all file attributes
        """

        source: str = ""
        type: str = ""
        extension: str = ""
        data_dictionary: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, source: str, type: str, extension: str = "", data_dictionary: str = "", **kwargs):
        """
        create a File node

        Parameters
        ----------
        source: str
            link or path to local file
        type: str
            Pick a file type from CRIPT controlled vocabulary [File types]()
        extension:str
            file extension
        data_dictionary:str
            extra information describing the file
        **kwargs:dict
            for internal use. Any extra data needed to create this file node
            when deserializing the JSON response from the API

        Examples
        --------
        ??? Example "Minimal File Node"
            ```python
            my_file = cript.File(
                source="https://criptapp.org",
                type="calibration",
            )
            ```

        ??? Example "Maximal File Node"
            ```python
            my_file = cript.File(
                source="https://criptapp.org",
                type="calibration",
                extension=".csv",
                data_dictionary="my file's data dictionary"
                notes="my notes for this file"
            )
            ```
        """

        super().__init__(**kwargs)

        # TODO check if vocabulary is valid or not
        # is_vocab_valid("file type", type)

        # setting every attribute except for source, which will be handled via setter
        self._json_attrs = replace(
            self._json_attrs,
            type=type,
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
        The File node source can be set to be either a path to a local file on disk
        or a URL path to a file on the web.

        Example
        --------
        URL File Source
        ```python
        url_source = "https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf"
        my_file.source = url_source
        ```
        Local File Path
        ```python
        my_file.source = "/home/user/project/my_file.csv"
        ```

        Returns
        -------
        source: str
            A string representing the file source.
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

        Example
        -------
        ```python
        my_file.source = "https://pubs.acs.org/doi/10.1021/acscentsci.3c00011"
        ```

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
    def type(self) -> str:
        """
        The [File type]() must come from [CRIPT controlled vocabulary]()

        Example
        -------
        ```python
        my_file.type = "calibration"
        ```

        Returns
        -------
        file type: str
            file type must come from [CRIPT controlled vocabulary]()
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str) -> None:
        """
        set the file type

        file type must come from CRIPT controlled vocabulary

        Parameters
        -----------
        new_type: str

        Example
        -------
        ```python
        my_file.type = "computation_config"
        ```

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
        The file extension property explicitly states what is the file extension of the file node.

        Example
        -------
        ```python
        my_file_node.extension = ".csv"`
        ```

        Returns
        -------
        extension: str
            file extension
        """
        return self._json_attrs.extension

    @extension.setter
    def extension(self, new_extension) -> None:
        """
        sets the new file extension

        Parameters
        ----------
        new_extension: str
            new file extension to overwrite the current file extension

        Example
        -------
        ```python
        my_file.extension = ".pdf"
        ```

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
        The data dictionary contains additional information
        that the scientist needs to describe their file.

        Notes
        ------
        It is advised for this field to be written in JSON format

        Examples
        -------
        ```python
        my_file.data_dictionary = "{'notes': 'This is something that describes my file node.'}"
        ```

        Returns
        -------
        data_dictionary: str
            the file data dictionary attribute
        """
        return self._json_attrs.data_dictionary

    @data_dictionary.setter
    def data_dictionary(self, new_data_dictionary: str) -> None:
        """
        Sets the data dictionary for the file node.

        Parameters
        ----------
        new_data_dictionary: str
            The new data dictionary to be set.

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, data_dictionary=new_data_dictionary)
        self._update_json_attrs_if_valid(new_attrs)
