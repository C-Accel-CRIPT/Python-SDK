import os
from pathlib import Path
from typing import Union

import requests

from cript.api.api_config import _API_TIMEOUT


def download_file_from_url(url: str, destination_path: Union[str, Path]) -> None:
    """
    downloads a file from URL

    Warnings
    ---------
    This is a very basic implementation that does not handle all URL files,
    and will likely throw errors.
    For example, some file URLs require a session or JS enabled to navigate to them
    such as "https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf"
    in those cases this implementation will fail.

    Parameters
    ----------
    url: str
        web URL to download the file from
        example: https://criptscripts.org/cript_graph/graph_ppt/CRIPT_Data_Structure_Template.pptx
    destination_path: Union[str, Path]
        which directory and file name the file should be written to after gotten from the web

    Returns
    -------
    None
        just downloads the file
    """

    response = requests.get(url=url, timeout=_API_TIMEOUT)

    # if not HTTP 200, then throw error
    response.raise_for_status()

    # get extension from URL
    file_extension = get_file_extension_from_url(url=url)

    # add the file extension to file path and file name
    destination_path = str(destination_path) + file_extension

    destination_path = Path(destination_path)

    # write contents to a file on user disk
    write_file_to_disk(destination_path=destination_path, file_contents=response.content)


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


def write_file_to_disk(destination_path: Union[str, Path], file_contents: bytes) -> None:
    """
    simply writes the file to the given destination

    Parameters
    ----------
    destination_path: Union[str, Path]
        which directory and file name the file should be written to after gotten from the web
    file_contents: bytes
        content of file to write to disk

    Returns
    -------
    None
        just writes the file to disk

    Raises
    ------
    FileNotFoundError
        In case the destination given to write the file to was not found or does not exist
    """
    # convert any type of path to a Path object
    destination_path = Path(destination_path)

    with open(file=destination_path, mode="wb") as file_handle:
        file_handle.write(file_contents)
