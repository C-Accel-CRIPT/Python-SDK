import json
from typing import Union

import jsonschema
from beartype import beartype

from cript.api.exceptions import APIError, InvalidVocabulary
from cript.api.utils.helper_functions import _get_node_type_from_json
from cript.api.vocabulary_categories import VocabCategories
from cript.nodes.exceptions import CRIPTNodeSchemaError


class DataSchema:
    """
    ## Definition
    DataSchema class, handles the interactions with the JSON node validation schema.
    """

    _vocabulary: dict = {}
    _db_schema: dict = {}
    # Advanced User Tip: Disabling Node Validation
    # For experienced users, deactivating node validation during creation can be a time-saver.
    # Note that the complete node graph will still undergo validation before being saved to the back end.
    # Caution: It's advisable to keep validation active while debugging scripts, as disabling it can delay error notifications and complicate the debugging process.
    skip_validation: bool = False

    def __init__(self, api):
        """
        Initialize DataSchema class with a full hostname to fetch the node validation schema.

        Examples
        --------
        ### Create a stand alone DataSchema instance.
        >>> import cript
        >>> with cript.API(host="https://api.criptapp.org/") as api:
        ...    data_schema = cript.api.DataSchema(api)
        """
        self._api = api
        self._vocabulary = {}
        self._db_schema = self._get_db_schema()

    def _get_db_schema(self) -> dict:
        """
        Sends a GET request to CRIPT to get the database schema and returns it.
        The database schema can be used for validating the JSON request
        before submitting it to CRIPT.

        1. checks if the db schema is already set
            * if already exists then it skips fetching it from the API and just returns what it already has
        2. if db schema has not been set yet, then it fetches it from the API
            * after getting it from the API it saves it in the `_schema` class variable,
            so it can be easily and efficiently gotten next time
        """

        # check if db schema is already saved
        if bool(self._db_schema):
            return self._db_schema

        # fetch db_schema from API
        self._api.logger.info(f"Loading node validation schema from {self._api.host}/schema/")
        # fetch db schema from API
        response: dict = self._api._capsule_request(url_path="/schema/", method="GET").json()

        # raise error if not HTTP 200
        if response["code"] != 200:
            raise APIError(api_error=str(response), http_method="GET", api_url="/schema")

        self._api.logger.info(f"Loading node validation schema from {self._api.host}/schema/ was successful.")

        # get the data from the API JSON response
        db_schema = response["data"]

        return db_schema

    def _fetch_vocab_entry(self, category: VocabCategories):
        """
        Fetches one the CRIPT controlled vocabulary and stores it in self._vocabulary
        """

        vocabulary_category_url: str = f"/cv/{category.value}/"

        # if vocabulary category is not in cache, then get it from API and cache it
        response: dict = self._api._capsule_request(url_path=vocabulary_category_url, method="GET").json()
        if response["code"] != 200:
            raise APIError(api_error=str(response), http_method="GET", api_url=vocabulary_category_url)
        # add to cache
        self._vocabulary[category.value] = response["data"]

    @beartype
    def get_vocab_by_category(self, category: VocabCategories) -> list:
        """
        get the CRIPT controlled vocabulary by category

        Examples
        --------
        >>> import os
        >>> import cript
        >>> with cript.API(
        ...     host="https://api.criptapp.org/",
        ...     api_token=os.getenv("CRIPT_TOKEN"),
        ...     storage_token=os.getenv("CRIPT_STORAGE_TOKEN")
        ... ) as api:
        ...     api.schema.get_vocab_by_category(cript.VocabCategories.MATERIAL_IDENTIFIER_KEY)  # doctest: +SKIP

        Parameters
        ----------
        category: str
            category of

        Returns
        -------
        List[dict]
            list of JSON containing the controlled vocabulary
        """
        try:
            return self._vocabulary[category.value]
        except KeyError:
            self._fetch_vocab_entry(category)
            return self._vocabulary[category.value]

    @beartype
    def _is_vocab_valid(self, vocab_category: VocabCategories, vocab_word: str) -> bool:
        """
        checks if the vocabulary is valid within the CRIPT controlled vocabulary.
        Either returns True or InvalidVocabulary Exception

        1. if the vocabulary is custom (starts with "+")
            then it is automatically valid
        2. if vocabulary is not custom, then it is checked against its category
            if the word cannot be found in the category then it returns False

        Parameters
        ----------
        vocab_category: VocabCategories
            ControlledVocabularyCategories enums
        vocab_word: str
            the vocabulary word e.g. "CAS", "SMILES", "BigSmiles", "+my_custom_key"

        Returns
        -------
        a boolean of if the vocabulary is valid

        Raises
        ------
        InvalidVocabulary
            If the vocabulary is invalid then the error gets raised
        """

        # check if vocab is custom
        # This is deactivated currently, no custom vocab allowed.
        # if vocab_word.startswith("+"):
        #     return True

        # get just the category needed
        controlled_vocabulary = self.get_vocab_by_category(vocab_category)

        # TODO this can be faster with a dict of dicts that can do o(1) look up
        #  looping through an unsorted list is an O(n) look up which is slow
        # loop through the list
        for vocab_dict in controlled_vocabulary:
            # check the name exists within the dict
            if vocab_dict.get("name") == vocab_word:
                return True

        raise InvalidVocabulary(vocab=vocab_word, possible_vocab=list(controlled_vocabulary))

    @beartype
    def is_node_schema_valid(self, node_json: str, is_patch: bool = False, force_validation: bool = False) -> Union[bool, None]:
        """
        checks a node JSON schema against the db schema to return if it is valid or not.

        1. get db schema
        1. convert node_json str to dict
        1. take out the node type from the dict
            1. "node": ["material"]
        1. use the node type from dict to tell the db schema which node schema to validate against
            1. Manipulates the string to be title case to work with db schema

        Parameters
        ----------
        node_json: str
            a node in JSON form string
        is_patch: bool
            a boolean flag checking if it needs to validate against `NodePost` or `NodePatch`

        Notes
        -----
        This function does not take into consideration vocabulary validation.
            For vocabulary validation please check `is_vocab_valid`

        Raises
        ------
        CRIPTNodeSchemaError
            in case a node is invalid

        Returns
        -------
        bool
            whether the node JSON is valid or not
        """

        # Fast exit without validation
        if self.skip_validation and not force_validation:
            return None

        db_schema = self._db_schema

        node_type: str = _get_node_type_from_json(node_json=node_json)

        node_dict = json.loads(node_json)

        # logging out info to the terminal for the user feedback
        # (improve UX because the program is currently slow)
        log_message = f"Validating {node_type} graph"
        try:
            log_message += " '" + str(node_dict["name"]) + "'"
        except KeyError:
            try:
                log_message += " '" + str(node_dict["uid"]) + "'"
            except KeyError:
                pass

        log_message += " ... "

        if force_validation:
            log_message = "Forced: " + log_message + " if error occur, try setting `cript_api.schema.skip_validation = False` for debugging."
        else:
            log_message += " (Can be disabled by setting `cript_api.schema.skip_validation = True`.)"

        self._api.logger.info(log_message)

        # set the schema to test against http POST or PATCH of DB Schema
        schema_http_method: str

        if is_patch:
            schema_http_method = "Patch"
        else:
            schema_http_method = "Post"

        # set which node you are using schema validation for
        db_schema["$ref"] = f"#/$defs/{node_type}{schema_http_method}"

        try:
            jsonschema.validate(instance=node_dict, schema=db_schema)
        except jsonschema.exceptions.ValidationError as error:
            raise CRIPTNodeSchemaError(node_type=node_dict["node"], json_schema_validation_error=str(error)) from error

        # if validation goes through without any problems return True
        return True
