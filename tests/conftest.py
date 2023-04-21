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
    complex_project_node,
    complex_reference_node,
    simple_collection_node,
    simple_computation_node,
    simple_computational_process_node,
    simple_data_node,
    simple_experiment_node,
    simple_inventory_node,
    simple_material_node,
    simple_process_node,
    simple_project_node,
    simple_software_configuration,
)
from fixtures.subobjects import (
    simple_algorithm_dict,
    simple_algorithm_node,
    simple_citation_dict,
    simple_citation_node,
    simple_computation_forcefield,
    simple_computation_forcefield_dict,
    simple_computation_forcefield_node,
    simple_condition_dict,
    simple_condition_node,
    simple_equipment_dict,
    simple_equipment_node,
    simple_ingredient_dict,
    simple_ingredient_node,
    simple_parameter_dict,
    simple_parameter_node,
    simple_property_dict,
    simple_property_node,
    simple_quantity_dict,
    simple_quantity_node,
    simple_reference_dict,
    simple_reference_node,
    simple_software_configuration_dict,
    simple_software_configuration_node,
    simple_software_dict,
    simple_software_node,
)
from fixtures.supporting_nodes import simple_file_node
from util import strip_uid_from_dict

import cript


@pytest.fixture(scope="session")
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """

    assert cript.api.api._global_cached_api is None
    with cript.API("http://development.api.mycriptapp.org/", "123456789") as api:
        yield api
    assert cript.api.api._global_cached_api is None
