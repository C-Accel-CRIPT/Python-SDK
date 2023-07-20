import os
from pathlib import Path
from typing import Union


def get_file_extension_from_file_path(file_path: Union[str, Path]) -> str:
    """
    gets a file extension from a file path string

    Parameters
    ----------
    file_path: str
        an absolute or relative file path

    Returns
    -------
    file_extension: str
        example: returns a file extension starting with a dot `.csv`
    """
    file_path_object = Path(file_path).resolve()
    file_name, file_extension = os.path.splitext(os.path.basename(file_path_object))

    return file_extension


def get_file_extension_from_url(url: str) -> str:
    """
    takes a file url and returns only the extension with the dot

    Parameters
    ----------
    url: str
        web URL
        example: "https://criptscripts.org/cript_graph/graph_ppt/CRIPT_Data_Structure_Template.pptx"

    Returns
    -------
    file extension: str
        file extension with dot
        example: ".pptx"
    """
    file_extension = os.path.splitext(url)[1]

    return file_extension
