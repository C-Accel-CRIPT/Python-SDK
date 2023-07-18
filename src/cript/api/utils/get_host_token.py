import json
import os
from pathlib import Path
from typing import Dict


def resolve_host_and_token(host, api_token, storage_token, config_file_path) -> Dict[str, str]:
    """
    resolves the host and token after passed into the constructor if it comes from env vars or config file

    ## priority level
    1. config file
    1. environment variable
    1. direct host and token

    Returns
    -------
    Dict[str, str]
        dict of host and token
    """
    if config_file_path:
        # convert str path or path object
        config_file_path = Path(config_file_path).resolve()

        # TODO the reading from config file can be separated into another function
        # read host and token from config.json
        with open(config_file_path, "r") as file_handle:
            config_file: Dict[str, str] = json.loads(file_handle.read())
            # set api host and token
            host = config_file["host"]
            api_token = config_file["api_token"]
            storage_token = config_file["storage_token"]

            return {"host": host, "api_token": api_token, "storage_token": storage_token}

    # if host and token is none then it will grab host and token from user's environment variables
    if host is None:
        host = _read_env_var(env_var_name="CRIPT_HOST")

    if api_token is None:
        api_token = _read_env_var(env_var_name="CRIPT_TOKEN")

    if storage_token is None:
        storage_token = _read_env_var(env_var_name="CRIPT_STORAGE_TOKEN")

    return {"host": host, "api_token": api_token, "storage_token": storage_token}


def _read_env_var(env_var_name: str) -> str:
    """
    reads the host or token from the env vars called `CRIPT_HOST` or `CRIPT_TOKEN`

    Returns
    -------
    str
    """
    env_var = os.environ.get(env_var_name)

    if env_var is None:
        raise RuntimeError(f"API initialized with `host=None` and `token=None` but environment variable `{env_var_name}` " f"was not found.")

    return env_var
