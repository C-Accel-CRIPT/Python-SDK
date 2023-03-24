import requests
from jsonschema import validate

from cript.api.api import _get_global_cached_api

_DB_SCHEMA: dict = None


def _get_db_schema() -> dict:
    """
    Sends a GET request to CRIPT to get the database schema and returns it.
    The database schema can be used for validating the JSON request
    before submitting it to CRIPT.

    1. Checks if the class variable is already set and if it is then it just returns that.
    2. If db schema is not already saved, then it makes a request to get it from CRIPT
    3. after successfully getting it from CRIPT, it sets the class variable

    Returns
    -------
    json
        The database schema in JSON format.
    """
    host: str = _get_global_cached_api().host
    global _DB_SCHEMA

    # if db_schema is already set then just return it
    if _DB_SCHEMA:
        return _DB_SCHEMA

    # if db_schema is not already set, then request it
    response = requests.get(f"{host}/api/v1/schema/").json()
    _DB_SCHEMA = response

    return _DB_SCHEMA


def is_schema_valid(node: dict) -> bool:
    """
    checks a node JSON schema against the db schema to return if it is valid or not.
    This function does not take into consideration vocabulary validation.
    For vocabulary validation please check `is_vocab_valid`

    Parameters
    ----------
    node:
        a node in JSON form

    Returns
    -------
    bool
        whether the node JSON is valid or not
    """

    db_schema = _get_db_schema()

    # TODO currently validate says every syntactically valid JSON is valid
    # TODO do we want invalid schema to raise an exception?
    if validate(node, db_schema):
        return True
    else:
        return False
