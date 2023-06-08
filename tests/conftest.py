# trunk-ignore-all(ruff/F401)
"""
This conftest file contains simple nodes (nodes with minimal required arguments)
and complex node (nodes that have all possible arguments), to use for testing.

Since nodes often depend on other nodes copying and pasting nodes is not ideal,
and keeping all nodes in one file makes it easier/cleaner to create tests.

The fixtures are all functional fixtures that stay consistent between all tests.
"""

import json

import pytest
from fixtures.primary_nodes import (
    complex_collection_node,
    complex_data_node,
    complex_material_node,
    complex_project_dict,
    complex_project_node,
    simple_collection_node,
    simple_computation_node,
    simple_computation_process_node,
    simple_computational_process_node,
    simple_data_node,
    simple_experiment_node,
    simple_inventory_node,
    simple_material_dict,
    simple_material_node,
    simple_process_node,
    simple_project_node,
    simple_software_configuration,
)
from fixtures.subobjects import (
    complex_algorithm_dict,
    complex_algorithm_node,
    complex_citation_dict,
    complex_citation_node,
    complex_computational_forcefield_dict,
    complex_computational_forcefield_node,
    complex_condition_dict,
    complex_condition_node,
    complex_equipment_dict,
    complex_equipment_node,
    complex_ingredient_dict,
    complex_ingredient_node,
    complex_parameter_dict,
    complex_parameter_node,
    complex_property_dict,
    complex_property_node,
    complex_quantity_dict,
    complex_quantity_node,
    complex_reference_dict,
    complex_reference_node,
    complex_software_configuration_dict,
    complex_software_configuration_node,
    complex_software_dict,
    complex_software_node,
    simple_computational_forcefield_node,
    simple_condition_node,
    simple_equipment_node,
    simple_property_dict,
    simple_property_node,
)
from fixtures.supporting_nodes import (
    complex_file_node,
    complex_user_dict,
    complex_user_node,
)
from util import strip_uid_from_dict

import cript


@pytest.fixture(scope="session", autouse=True)
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """
    host: str = "http://development.api.mycriptapp.org/"
    token = "123456"

    assert cript.api.api._global_cached_api is None
    with cript.API(host=host, token=token) as api:
        with open("db_schema.json", "w") as file_handle:
            json.dump(api.schema, file_handle, indent=2)
        yield api
    assert cript.api.api._global_cached_api is None
