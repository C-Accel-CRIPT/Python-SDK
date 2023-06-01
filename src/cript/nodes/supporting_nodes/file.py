from dataclasses import dataclass, replace
from pathlib import Path
from typing import Union

from cript.nodes.uuid_base import UUIDBaseNode


def _is_local_file(file_source: Union[str, Path]) -> bool:
    """
    Determines if the file the user is uploading is a local file or a link.

    the file is a local file path if it does Not start with "http" or isinstance of Path object

    Parameters
    ----------
    file_source: Union[str, Path]
        The source of the file

    Returns
    -------
    bool
        True if the file is local, False if it's a link.
    """

    # checking "http" so it works with both "https://" and "http://"
    if file_source.startswith("http"):
        return False
    else:
        return True


def _upload_file_and_get_url(source: Union[str, Path]) -> str:
    """
    uploads file to cloud storage and returns the file link

    1.  checks if the source is a local file path and not a web url
    1. if it is a local file path, then it uploads it to cloud storage
        * returns the file link in cloud storage
    1. else it returns the same file link because it is already on the web

    Parameters
    ----------
    source: str
        file source can be a relative or absolute file string or pathlib object

    Returns
    -------
    str
        file AWS S3 link
    """
    from cript.api.api import _get_global_cached_api

    if _is_local_file(file_source=source):
        api = _get_global_cached_api()
        url_source = api.upload_file(file_path=source)
        source = url_source

        return source


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
            file web link or path to local file
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

        Raises
        ------
        FileNotFoundError
            Raises [FileNotFoundError](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)
            if the file could not be found when the Python SDK goes to open the file from local storage
            to upload it to CRIPT storage.

        ## File Source
        File node `source` attribute can be either a link to a data file,such as
        [CRIPT Data Model PDF link](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf)
        or a path to a file on local storage.

        ### Local File
        For local file path source it can be a relative link from the current directory
        such as

        #### Relative File Path Example
        ```python
        my_file = cript.File(
            source="../my_data_file.csv",
            type="calibration",
        )
        ```

        #### Absolute File Path Example
        ```python
        my_file = cript.File(
            source=r"C:\\Users\\username\\Desktop\\my_data_file.csv",
            type="calibration",
        )
        ```

        ### Recommended: File Path Using [Pathlib](https://docs.python.org/3/library/pathlib.html) or [OS Module](https://docs.python.org/3/library/os.path.html)

        The benefits of using something like [Pathlib](https://docs.python.org/3/library/pathlib.html)
        over giving an absolute file path string is that it is platform independent and less chance of errors.

        ```python
        from pathlib import Path

        my_file_path = (Path(__file__).parent / "my_files" / "my_data").resolve()
        ```
        """

        super().__init__(**kwargs)

        # upload file source if local file
        source = _upload_file_and_get_url(source=source)

        # TODO add validation that extension must start with `.` or be uniform to work with it easier
        self._json_attrs = replace(
            self._json_attrs,
            type=type,
            source=source,
            extension=extension,
            data_dictionary=data_dictionary,
        )

        self.validate()

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
    def source(self, new_source: Union[str, Path]) -> None:
        """
        sets the source of the file node
        the source can either be a path to a file on local storage or a URL link to a file

        1. checks if the file source is a link or a local file path
        2. if the source is a link such as `https://en.wikipedia.org/wiki/Polymer`
            then it simply sets the URL as the file source and continues
        3. if the file source is a local file path such as
                `C:\\Users\\my_username\\Desktop\\cript\\file.txt`
            1. then it opens the file and reads it
            2. uploads it to the cloud storage
            3. gets back a URL from where in the cloud the file is found
            4. sets that URL as the source and continues

        Parameters
        ----------
        new_source: Union[str, Path]
            URL to file or local file path

        Example
        -------
        ```python
        my_file.source = "https://pubs.acs.org/doi/10.1021/acscentsci.3c00011"
        ```

        Returns
        -------
        None
        """

        file_url_source: str = _upload_file_and_get_url(source=new_source)

        new_attrs = replace(self._json_attrs, source=file_url_source)
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

    # TODO rename to `destination_directory_path`
    # TODO get file name from node itself as default and allow for customization as well optional
    # TODO make the destination path optional
    def download(self, destination_source: Union[str, Path], file_name: str) -> None:
        """
        download this file to current working directory or a specific destination

        Parameters
        ----------
        destination_source: Union[str, Path]
            where you want the file to be stored and what you want the name to be
        file_name: str
            what you want to name the file node on your computer

        Returns
        -------
        None
        """
        from cript.api.api import _get_global_cached_api
        api = _get_global_cached_api()

        existing_folder_path = Path(destination_source)
        # TODO add file extension to it
        file_name = f"{file_name}"
        absolute_file_path = str((existing_folder_path / file_name).resolve())

        api.download_file(file_url=self.source, destination_path=absolute_file_path)
