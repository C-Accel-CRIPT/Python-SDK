import json

from jsonschema import validate


class CRIPTSchema:
    """
    Data class representing the node schema of CRIPT.
    """

    _data: dict = {}

    def __init__(self, db_schema: dict):
        # TODO check that we support that version

        self._data = db_schema

    def is_node_valid(self, node_json: str) -> bool:
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

        # TODO currently validate says every syntactically valid JSON is valid
        # TODO do we want invalid schema to raise an exception?
        node_dict = json.loads(node_json)
        if validate(node_dict, self._data):
            return True
        else:
            return False
