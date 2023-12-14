import requests
import logging
from beartype import beartype

from cript.api.api_config import _API_TIMEOUT
from cript.api.vocabulary_categories import VocabCategories


class DataSchema:
    """
    ## Definition
    DataSchema class, handles the interactions with the JSON node validation schema.
    """

    _vocabulary: dict[str, str] = {}
    _db_schema: dict[str, str] = {}

    def _get_db_schema(self, host:str) -> dict[str, str]:
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
        else:
            logging.info(f"Loading node validation schema from {self.host}/schema/")
            # fetch db schema from API
            response: requests.Response = requests.get(url=f"{host}/schema/", timeout=_API_TIMEOUT)

            # raise error if not HTTP 200
            response.raise_for_status()
            logging.info(f"Loading node validation schema from {host}/schema/ was successfull.")

            # if no error, take the JSON from the API response
            response_dict: dict = response.json()

            # get the data from the API JSON response
            self._db_schema = response_dict["data"]

            return self._db_schema


    def __init__(self, host:str):
        """
        Initialize DataSchema class with a full hostname to fetch the node validation schema.

        Examples
        --------
        ### Create a stand alone DataSchema instance.
        >>> import cript
        >>> data_schema = cript.DataSchema("https://api.criptapp.org/v1")

        """

        self._db_schema = self._get_db_schema(host)
        self._vocabulary = self._get_vocab(host)


    def _get_vocab(self, host:str) -> dict[str,str]:
        """
        gets the entire CRIPT controlled vocabulary and stores it in _vocabulary

        1. loops through all controlled vocabulary categories
            1. if the category already exists in the controlled vocabulary then skip that category and continue
            1. if the category does not exist in the `_vocabulary` dict,
            then request it from the API and append it to the `_vocabulary` dict
        1. at the end the `_vocabulary` should have all the controlled vocabulary and that will be returned

           Examples
           --------
           The vocabulary looks like this
           ```json
           {'algorithm_key':
                [
                    {
                    'description': "Velocity-Verlet integration algorithm. Parameters: 'integration_timestep'.",
                    'name': 'velocity_verlet'
                    },
            }
           ```
        """

        vocabulary: dict[str, str] = {}
        # loop through all vocabulary categories and make a request to each vocabulary category
        # and put them all inside of self._vocab with the keys being the vocab category name
        for category in VocabCategories:
            vocabulary_category_url: str = f"{self.host}/cv/{category.value}/"

            # if vocabulary category is not in cache, then get it from API and cache it
            response: dict = requests.get(url=vocabulary_category_url, timeout=_API_TIMEOUT).json()

            if response["code"] != 200:
                raise APIError(api_error=str(response), http_method="GET", api_url=vocabulary_category_url)

            # add to cache
            vocabulary[category.value] = response["data"]

        return vocabulary

    @beartype
    def get_vocab_by_category(self, category: VocabCategories) -> List[dict]:
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
        ...     api.validation_schema.get_vocab_by_category(cript.VocabCategories.MATERIAL_IDENTIFIER_KEY)  # doctest: +SKIP

        Parameters
        ----------
        category: str
            category of

        Returns
        -------
        List[dict]
            list of JSON containing the controlled vocabulary
        """

        # check if the vocabulary category is already cached
        if category.value in self._vocabulary:
            return self._vocabulary[category.value]


        return self._vocabulary[category.value]
