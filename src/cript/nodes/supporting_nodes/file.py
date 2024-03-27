import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Union

from beartype import beartype

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


def _is_local_file(file_source: str) -> bool:
    """
    Determines if the file the user is uploading is a local file or a link.

    It basically tests if the path exists, and it is specifically a file
    on the local storage and not just a valid directory

    Notes
    -----
    since checking for URL is very easy because it has to start with HTTP it checks that as well
    if it starts with http then it makes the work easy, and it is automatically web URL

    Parameters
    ----------
    file_source: str
        The source of the file.

    Returns
    -------
    bool
        True if the file is local, False if it's a link or s3 object_name.
    """

    # convert local or relative file path str into a path object and resolve it to always get an absolute path
    file_source_abs_path: str = str(Path(file_source).resolve())

    # if it doesn't start with HTTP and exists on disk
    # checking "http" so it works with both "https://" and "http://"
    if not file_source.startswith("http") and os.path.isfile(file_source_abs_path):
        return True

    else:
        return False


def _upload_file_and_get_object_name(source: Union[str, Path], api=None) -> str:
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

    # convert source to str for `_is_local_file` and to return str
    source = str(source)

    if _is_local_file(file_source=source):
        if api is None:
            api = _get_global_cached_api()
        object_name = api.upload_file(file_path=source)
        # always getting a string for object_name
        source = str(object_name)

    # always returning a string
    return source


class File(PrimaryBaseNode):
    """
    ## Definition

    The [File node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001
    .pdf#page=28) provides a link to scholarly work and allows users to specify in what way the work relates to that
    data. More specifically, users can specify that the data was directly extracted from, inspired by, derived from,
    etc.

    The file node is held in the [Data node](../../primary_nodes/data).

    ## Attributes

    | Attribute       | Type | Example                                                                                               | Description                                                                 | Required |
    |-----------------|------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------|
    | name            | str  | `"my file name"`                                                                                      | descriptive name for the file node                                          | True     |
    | source          | str  | `"path/to/my/file"` or `"https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system"` | source to the file can be URL or local path                                 | True     |
    | type            | str  | `"logs"`                                                                                              | Pick from [CRIPT File Types](https://app.criptapp.org/vocab/file_type/)     | True     |
    | extension       | str  | `".csv"`                                                                                              | file extension                                                              | False    |
    | data_dictionary | str  | `"my extra info in my data dictionary"`                                                               | set of information describing the contents, format, and structure of a file | False    |
    | notes           | str  |                                                                                                       | miscellaneous information, or custom data structure (e.g.; JSON)            |          |

    ## JSON
    ``` json
    {
        "node": ["File"],
        "name": "my file node name",
        "source": "https://criptapp.org",
        "type": "calibration",
        "extension": ".csv",
        "data_dictionary": "my file's data dictionary",
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all file attributes
        """

        source: str = ""
        type: str = ""
        extension: str = ""
        data_dictionary: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, name: str, source: str, type: str, extension: str, data_dictionary: str = "", notes: str = "", **kwargs):
        """
        create a File node

        Parameters
        ----------
        name: str
            File node name
        source: str
            link or path to local file
        type: str
            Pick a file type from CRIPT controlled vocabulary
            [File types](https://app.criptapp.org/vocab/file_type)
        extension:str
            file extension
        data_dictionary:str
            extra information describing the file
        notes: str
            notes for the file node
        **kwargs:dict
            for internal use. Any extra data needed to create this file node
            when deserializing the JSON response from the API

        Examples
        --------
        ### Web URL File Node
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
        ...     type="calibration",
        ...     extension=".pdf",
        ...     data_dictionary="my file's data dictionary",
        ...     notes="my notes for this file",
        ... )

        ### Local Source File Node
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="/home/user/MIT/project/my_file.csv",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary",
        ...     notes="my notes for this file",
        ... )
        """

        super().__init__(name=name, notes=notes, **kwargs)

        # setting every attribute except for source, which will be handled via setter
        new_json_attrs = replace(
            self._json_attrs,
            type=type,
            # always giving the function the required str regardless if the input `Path` or `str`
            source=str(source),
            extension=extension,
            data_dictionary=data_dictionary,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    def ensure_uploaded(self, api=None):
        """
        Ensure that a local file is being uploaded into CRIPT accessible cloud storage.
        After this call, non-local files (file names that do not start with `http`) are uploaded.
        It is not necessary to call this function manually.
        A saved project automatically ensures uploaded files, it is recommend to rely on the automatic upload.

        Parameters
        -----------
        api: cript.API, optional
           API object that performs the upload.
           If None, the globally cached object is being used.

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="/local/path/to/file",
        ...     type="calibration",
        ...     extension="csv",
        ... )
        >>> my_file.ensure_uploaded()   # doctest: +SKIP
        >>> my_file.source # changed to cloud storage object name   # doctest: +SKIP
        """

        if _is_local_file(file_source=self.source):
            # upload file source if local file
            self.source = _upload_file_and_get_object_name(source=self.source)

    # TODO can be made into a function

    # --------------- Properties ---------------
    @property
    @beartype
    def source(self) -> str:
        """
        The File node source can be set to be either a path to a local file on disk
        or a URL path to a file on the web.

        Examples
        --------
        URL File Source
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ... )
        >>> my_file.source = "/home/user/project/my_file.csv"

        Returns
        -------
        source: str
            A string representing the file source.
        """
        return self._json_attrs.source

    @source.setter
    @beartype
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

        Examples
        --------
        >>> import cript
        >>> my_file.source = "https://pubs.acs.org/doi/10.1021/acscentsci.3c00011"

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, source=new_source)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        The [File type](https://app.criptapp.org/vocab/file_type) must come from CRIPT controlled vocabulary

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ... )
        >>> my_file.type = "calibration"

        Returns
        -------
        file type: str
            file type must come from [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/file_type)
        """
        return self._json_attrs.type

    @type.setter
    @beartype
    def type(self, new_type: str) -> None:
        """
        set the file type

        file type must come from CRIPT controlled vocabulary

        Parameters
        -----------
        new_type: str

        Examples
        --------
        >>> import cript
        >>> my_file.type = "computation_config"

        Returns
        -------
        None
        """
        # TODO check vocabulary is valid
        # is_vocab_valid("file type", self._json_attrs.type)
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def extension(self) -> str:
        """
        The file extension property explicitly states what is the file extension of the file node.

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".text",
        ... )
        >>> my_file.extension = ".csv"

        !!! Note "file extensions must start with a dot"
            File extensions must start with a dot, for example `.csv` or `.pdf`

        Returns
        -------
        extension: str
            file extension
        """
        return self._json_attrs.extension

    @extension.setter
    @beartype
    def extension(self, new_extension) -> None:
        """
        sets the new file extension

        Parameters
        ----------
        new_extension: str
            new file extension to overwrite the current file extension

        Examples
        --------
        >>> import cript
        >>> my_file.extension = ".pdf"

        Returns
        -------
            None
        """
        new_attrs = replace(self._json_attrs, extension=new_extension)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def data_dictionary(self) -> str:
        # TODO data dictionary needs documentation describing it and how to use it
        """
        The data dictionary contains additional information
        that the scientist needs to describe their file.

        Notes
        ------
        It is advised for this field to be written in JSON format

        Examples
        ---------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".png",
        ... )
        >>> my_file.data_dictionary = "{'notes': 'This is something that describes my file node.'}"

        Returns
        -------
        data_dictionary: str
            the file data dictionary attribute
        """
        return self._json_attrs.data_dictionary

    @data_dictionary.setter
    @beartype
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

    @beartype
    def download(
        self,
        destination_directory_path: Union[str, Path] = ".",
    ) -> None:
        """
        download this file to current working directory or a specific destination.
        The file name will come from the file_node.name and the extension will come from file_node.extension

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="/local/path/to/file",
        ...     type="calibration",
        ...     extension=".jpeg",
        ... )
        >>> my_file.ensure_uploaded()   # doctest: +SKIP
        >>> my_file.source # changed to cloud storage object name   # doctest: +SKIP
        >>> my_file.download()  # doctest: +SKIP

        Notes
        -----
        Whether the file extension is written like `.csv` or `csv` the program will work correctly

        Parameters
        ----------
        destination_directory_path: Union[str, Path]
            where you want the file to be stored and what you want the name to be
            by default it is the current working directory

        Returns
        -------
        None
        """
        from cript.api.api import _get_global_cached_api

        api = _get_global_cached_api()

        # convert the path from str to Path in case it was given as a str and resolve it to get the absolute path
        existing_folder_path = Path(destination_directory_path).resolve()

        # stripping dot from extension to make all extensions uniform, in case a user puts `.csv` or `csv` it will work
        file_name = f"{self.name}.{self.extension.lstrip('.')}"

        absolute_file_path = str((existing_folder_path / file_name).resolve())

        api.download_file(file_source=self.source, destination_path=absolute_file_path)
