# CRIPT Python SDK Changelog

## Version 2.4.0

### New Features

- `cript.API` searches work as intended.
- SDK initiated searches can be controlled and interrupted for large queries.

### Known Issues and Bugs

- Saving projects is not supported. Temporarily, you can use `get_expanded_json` to store a JSON representation of projects, which can be uploaded into CRIPT at a later time.
- Permission settings in CRIPT do not influence the behavior of the SDK objects.
- Tests that require valid tokens (like saving or searching) are not included in CI/CD tests.
- BigSMILES searches can contain duplicates.

### Bug Fixes

- Search is now matched with the API requirements.

### Breaking Changes

- The Paginator interface changed to reflect the backend requirements.

### Health Report

````shell
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.11.2, pytest-7.4.3, pluggy-1.3.0
rootdir: /home/ludwig/git/Python-SDK
plugins: cov-4.1.0
collected 124 items

tests/test_node_util.py ...........                                                                                                                                                                         [  8%]
tests/api/test_api.py .....                                                                                                                                                                                 [ 12%]
tests/api/test_db_schema.py .....                                                                                                                                                                           [ 16%]
tests/api/test_search.py .....F                                                                                                                                                                             [ 21%]
tests/nodes/test_utils.py ..                                                                                                                                                                                [ 23%]
tests/nodes/primary_nodes/test_collection.py .....F                                                                                                                                                         [ 28%]
tests/nodes/primary_nodes/test_computation.py .....F                                                                                                                                                        [ 33%]
tests/nodes/primary_nodes/test_computational_process.py ....F                                                                                                                                               [ 37%]
tests/nodes/primary_nodes/test_data.py ....F                                                                                                                                                                [ 41%]
tests/nodes/primary_nodes/test_experiment.py ....F                                                                                                                                                          [ 45%]
tests/nodes/primary_nodes/test_inventory.py ..F                                                                                                                                                             [ 47%]
tests/nodes/primary_nodes/test_material.py ...F                                                                                                                                                             [ 50%]
tests/nodes/primary_nodes/test_process.py .....F                                                                                                                                                            [ 55%]
tests/nodes/primary_nodes/test_project.py ...F                                                                                                                                                              [ 58%]
tests/nodes/primary_nodes/test_reference.py ......F                                                                                                                                                         [ 64%]
tests/nodes/subobjects/test_algorithm.py ..F                                                                                                                                                                [ 66%]
tests/nodes/subobjects/test_citation.py ..F                                                                                                                                                                 [ 69%]
tests/nodes/subobjects/test_computational_forcefield.py ..F                                                                                                                                                 [ 71%]
tests/nodes/subobjects/test_condition.py ..F                                                                                                                                                                [ 74%]
tests/nodes/subobjects/test_equipment.py ..F                                                                                                                                                                [ 76%]
tests/nodes/subobjects/test_ingredient.py ..F                                                                                                                                                               [ 79%]
tests/nodes/subobjects/test_parameter.py ..F                                                                                                                                                                [ 81%]
tests/nodes/subobjects/test_property.py ..F                                                                                                                                                                 [ 83%]
tests/nodes/subobjects/test_quantity.py ..F                                                                                                                                                                 [ 86%]
tests/nodes/subobjects/test_software.py ...F                                                                                                                                                                [ 89%]
tests/nodes/subobjects/test_software_configuration.py ..F                                                                                                                                                   [ 91%]
tests/nodes/supporting_nodes/test_file.py ..s....F                                                                                                                                                          [ 98%]
tests/nodes/supporting_nodes/test_user.py ..

FAILED tests/nodes/primary_nodes/test_collection.py::test_integration_collection - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_computation.py::test_integration_computation - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_computational_process.py::test_integration_computational_process - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_data.py::test_integration_data - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_experiment.py::test_integration_experiment - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_inventory.py::test_integration_inventory - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_material.py::test_integration_material - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_process.py::test_integration_complex_process - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_project.py::test_integration_project - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/primary_nodes/test_reference.py::test_integration_reference - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_algorithm.py::test_integration_algorithm - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_citation.py::test_integration_citation - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_computational_forcefield.py::test_integration_computational_forcefield - AttributeError: 'NoneType' object has no attribute 'description'
FAILED tests/nodes/subobjects/test_condition.py::test_integration_process_condition - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_equipment.py::test_integration_equipment - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_ingredient.py::test_integration_ingredient - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_parameter.py::test_integration_parameter - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_property.py::test_integration_material_property - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_quantity.py::test_integration_quantity - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_software.py::test_integration_software - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/subobjects/test_software_configuration.py::test_integration_software_configuration - AttributeError: 'list' object has no attribute 'startswith'
FAILED tests/nodes/supporting_nodes/test_file.py::test_integration_file - AttributeError: 'list' object has no attribute 'startswith'
======================================================================== 22 failed, 101 passed, 1 skipped, 1 warning in 1506.18s (0:25:06) ========================================================================



## Version 2.3.0

### New Features

- `cript.API` objects now have a `DataSchema` attribute called `schema`, representing the JSON schema for node validation.
  - This includes the ability to enable and disable node validation.
- `cript.API` objects now have `logger` attributes from the Python `logging` module to control logging flows.
- Refactor of Paginator:
  - New Paginator objects for accessing data from the CRIPT data bank via search.
  - Paginator are now Python iterators. You can use `for node in paginator: ...` directly.
  - Paginator now return `cript.Node` objects natively.
  - JSON response can be requested from Paginator alternatively. This is helpful for internal work and debugging.
- Additional information is added to the logging message when nodes are validated. For primary nodes, `name` is displayed; for others, the `UUID` is displayed.
- HTTP requests are now optimized, leaving connections open and grouping requests for better performance.
- A native iterator for nodes is now offered. It iterates in depth-first order over all child nodes of the root node. Cycles are automatically broken, and every node is visited exactly once.
- Materials with no identifier issue a warning to users.
- Debugging messages show full API requests and responses for debugging.
- Automated UUID caching for nodes can now be explicitly circumvented when using `cript.load_nodes_from_json`. Mostly useful for development.

### Known Issues and Bugs

- Saving projects is not supported. Temporarily, you can use `get_expanded_json` to store a JSON representation of projects, which can be uploaded into CRIPT at a later time.
- BigSMILES search patterns are not supported.
- Searching for more than 1000 pages (10000 entries) is not supported.
- Permission settings in CRIPT do not influence the behavior of the SDK objects.
- Tests that require valid tokens (like saving or searching) are not included in CI/CD tests.

### Bugfixes

- `cript.load_nodes_from_json` can now load JSON files that store different nodes in lists or dictionaries.
- Not all nodes were correctly validated at all times, especially if instantiated from JSON. All nodes are automatically validated now.
- The documentation has been updated to remove certain mistakes.
- Users can have only one Python object with the same UUID to avoid mis-updates. This did not work in all cases, but it works in all cases now.

### Breaking Changes

- `cript.API()` objects no longer have functions related to JSON schema validation. Please use the new `DataSchema` class instead. The `DataSchema` class can be accessed via the `schema` property of the API class.
- Indirect logging control via the API is defunct. Please use the direct access to the `logger` attribute of API classes to control logging output.
- The SDK used to use `identifier` dictionaries for material identifiers. This is updated to use individual attributes of the material node. This is consistent with the JSON schema and front-end but is a breaking change to older SDK versions and the original CRIPT publication.
- Projects were checked to ensure the presence of material and computation in Experiments. These errors were converted into warnings.

### Health Report

```shell
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.11.2, pytest-7.4.3
plugins: cov-4.1.0
collected 124 items

tests/test_node_util.py ........... [ 8%]
tests/api/test_api.py ..... [ 12%]
tests/api/test_db_schema.py ..... [ 16%]
tests/api/test_search.py .....F [ 21%]
tests/nodes/test_utils.py .. [ 23%]
tests/nodes/primary_nodes/test_collection.py .....F [ 28%]
tests/nodes/primary_nodes/test_computation.py .....F [ 33%]
tests/nodes/primary_nodes/test_computational_process.py ....F [ 37%]
tests/nodes/primary_nodes/test_data.py ....F [ 41%]
tests/nodes/primary_nodes/test_experiment.py ....F [ 45%]
tests/nodes/primary_nodes/test_inventory.py ..F [ 47%]
tests/nodes/primary_nodes/test_material.py ...F [ 50%]
tests/nodes/primary_nodes/test_process.py .....F [ 55%]
tests/nodes/primary_nodes/test_project.py ...F [ 58%]
tests/nodes/primary_nodes/test_reference.py ......F [ 64%]
tests/nodes/subobjects/test_algorithm.py ..F [ 66%]
tests/nodes/subobjects/test_citation.py ..F [ 69%]
tests/nodes/subobjects/test_computational_forcefield.py ..F [ 71%]
tests/nodes/subobjects/test_condition.py ..F [ 74%]
tests/nodes/subobjects/test_equipment.py ..F [ 76%]
tests/nodes/subobjects/test_ingredient.py ..F [ 79%]
tests/nodes/subobjects/test_parameter.py ..F [ 81%]
tests/nodes/subobjects/test_property.py ..F [ 83%]
tests/nodes/subobjects/test_quantity.py ..F [ 86%]
tests/nodes/subobjects/test_software.py ...F [ 89%]
tests/nodes/subobjects/test_software_configuration.py ..F [ 91%]
tests/nodes/supporting_nodes/test_file.py ..s....F [ 98%]
tests/nodes/supporting_nodes/test_user.py .. [100%]
============================================================================================= short test summary info =============================================================================================
FAILED tests/api/test_search.py::test_api_search_bigsmiles - cript.nodes.exceptions.CRIPTJsonDeserializationError: JSON deserialization failed for node type Material with JSON str: Material
FAILED tests/nodes/primary_nodes/test_collection.py::test_integration_collection - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_computation.py::test_integration_computation - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_computational_process.py::test_integration_computational_process - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_data.py::test_integration_data - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_experiment.py::test_integration_experiment - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_inventory.py::test_integration_inventory - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_material.py::test_integration_material - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_process.py::test_integration_complex_process - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_project.py::test_integration_project - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/primary_nodes/test_reference.py::test_integration_reference - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_algorithm.py::test_integration_algorithm - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_citation.py::test_integration_citation - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_computational_forcefield.py::test_integration_computational_forcefield - AttributeError: 'NoneType' object has no attribute 'description'
FAILED tests/nodes/subobjects/test_condition.py::test_integration_process_condition - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_equipment.py::test_integration_equipment - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_ingredient.py::test_integration_ingredient - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_parameter.py::test_integration_parameter - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_property.py::test_integration_material_property - IndexError: list index out of range
FAILED tests/nodes/subobjects/test_quantity.py::test_integration_quantity - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_software.py::test_integration_software - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/subobjects/test_software_configuration.py::test_integration_software_configuration - AttributeError: 'list' object has no attribute 'starts with'
FAILED tests/nodes/supporting_nodes/test_file.py::test_integration_file - AttributeError: 'list' object has no attribute 'starts with'
======================================================================== 23 failed, 100 passed, 1 skipped, 1 warning in 905.51s (0:15:05) =========================================================================
````
