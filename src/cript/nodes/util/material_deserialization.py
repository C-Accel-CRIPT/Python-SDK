from typing import Dict, List

import cript


def _deserialize_flattened_material_identifiers(json_dict: Dict) -> Dict:
    """
    takes a material node in JSON format that has its identifiers as attributes and convert it to have the
    identifiers within the identifiers field of a material node

    1. gets the material identifiers controlled vocabulary from the API
    1. converts the API response from list[dicts] to just a list[str]
    1. loops through all the material identifiers and checks if they exist within the JSON dict
    1. if a material identifier is spotted in json dict, then that material identifier is moved from JSON attribute
    into an identifiers field


    ## Input
    ```python
    {
    "node": ["Material"],
    "name": "my cool material",
    "uuid": "_:my cool material",
    "smiles": "CCC",
    "bigsmiles": "my big smiles"
    }
    ```

    ## Output
    ```python
    {
       "node":["Material"],
       "name":"my cool material",
       "uuid":"_:my cool material",
       "identifiers":[
          {"smiles":"CCC"},
          {"bigsmiles":"my big smiles"}
       ]
    }
    ```

    Parameters
    ----------
    json_dict: Dict
         A JSON dictionary representing a node

    Returns
    -------
    json_dict: Dict
        A new JSON dictionary with the material identifiers moved from attributes to the identifiers field
    """
    from cript.api.api import _get_global_cached_api

    api = _get_global_cached_api()

    # get material identifiers keys from API and create a simple list
    # eg ["smiles", "bigsmiles", etc.]
    all_identifiers_list: List[str] = [identifier.get("name") for identifier in api.get_vocab_by_category(cript.ControlledVocabularyCategories.MATERIAL_IDENTIFIER_KEY)]

    # pop "name" from identifiers list because the node has to have a name
    all_identifiers_list.remove("name")

    identifier_argument: List[Dict] = []

    # move material identifiers from JSON attribute to identifiers attributes
    for identifier in all_identifiers_list:
        if identifier in json_dict:
            identifier_argument.append({identifier: json_dict[identifier]})
            # delete identifiers from the API JSON response as they are added to the material node
            del json_dict[identifier]
        json_dict["identifiers"] = identifier_argument

    return json_dict
