::: cript.nodes.primary_nodes.collection

<!---
==============================

# Non-docstrings

## Definition

A `Collection` is nested inside of a <a href="../experiment" target="_blank">`Project`</a> node.
A `Collection` node can be thought as a folder/bucket that can hold either an 
<a href="../experiment" target="_blank">`Experiment`</a> or 
<a href="../inventory" target="_blank">`Inventory`</a> node.

## Navigating to Collection
`Collections` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/collection/" target="_blank">Collections link</a>

## Attributes

| Attribute             | Type                                                | Example                  | Description                                                                             | Required |
|-----------------------|-----------------------------------------------------|--------------------------|-----------------------------------------------------------------------------------------|----------|
| `url`                   | str                                                 | "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/" | Unique URL for the node              | True     |
| `uid`                   | str                                                 | "336d0584-04f9-49fe-9c0d-78772e2f1ead" | Unique ID for the node                                                    | True     |
| `group`                 | [Group](../nodes/group.md)               |                          | Group that owns the `Collection` node                                                   | True     |
| `project`                 | [Project](../nodes/project.md)                          |                          | Project associated with the `Collection` node                                           | True     |
| `name`                  | str                                                 | "Navid's collection"     | Name of the `Collection`  node                                                          | True     |
| `experiments`           | list[[Experiment](experiment.md)]                   | [exp_1, exp_2, exp_3]    | Experiments that relate to the `Collection` node                                        | False    |
| `inventories`           | list[[Inventory](inventory.md)]                     | [inv_1, inv_2, inv_3]    | Inventories owned by the `Collection` node                                              | False    |
| `citations`             | list[[Citation](../subobjects/citation.md)]         |                          | Reference to a book, paper, or scholarly work                                           | False    |
| `created_at`            | datetime                                            | "2022-11-23T00:59:01.453731Z" | Date and time the `Collection` node was created (UTC time)                         | True     |
| `updated_at`            | datetime                                            | "2022-11-23T00:59:01.453756Z" | Date and time the `Collection` node was last modified (UTC time)                   | True     |
| `public`                | bool                                                | False                    | Boolean indicating whether the node is publicly viewable | True     |

## Example
```json
{
    "url": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/",
    "uid": "336d0584-04f9-49fe-9c0d-78772e2f1ead",
    "group": "https://criptapp.org/api/group/68ed4c57-d1ca-4708-89b2-cb1c1609ace2/",
    "project": "https://criptapp.org/api/project/910445b2-88ca-43ac-88cf-f6424e85b1ba/",
    "name": "Navid's Collecton",
    "notes": null,
    "experiments": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/experiments/",
    "inventories": "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/inventories/",
    "citations": [],
    "created_at": "2022-11-23T00:59:01.453731Z",
    "updated_at": "2022-11-23T00:59:01.453756Z",
    "public": false
}

```

<br/>

!!! warning "Collection names"
    `Collection` names Must be unique within a <a href="../project" target="_blank">Project</a>

## Methods

### Create

_Definition:_

Both creates and saves (i.e., uploads to the CRIPT database) a `Collection` node. It has 2 required arguments: `project` and `name`.

`cript.Collection.create(project, name, **kwargs)`

_Parameters:_

| Name        | Type   | Description                                          | Default |
|-------------|--------|------------------------------------------------------|---------|
| `project`   | [`Project`](../nodes/project.md) node | `Project` to associate the `Collection` node with    | None    |
| `name`      | string | name of the `Collection` node                        | None    |
| `**kwargs`  |        | Arguments for the constructor.                       | `{}`    |

_Returns:_

`Collection` node of type `cript.data_model.nodes.BaseNode`

_Example:_

Creating a `Collection` called *"My Collection"*

```python
my_project = cript.Project.get(name = "My project") # retrieves an already-created project
my_collection = cript.Collection.create(project = my_project, name="My collection")
```

---

### Save

_Definition:_

Saves the `Collection` node to the CRIPT database. It can be used after initial instantiation of a
`Collection` node (e.g., `cript.Collection(project, name)`) or after modifying a `Collection` node. It does not have any required arguments.

`cript.Collection.save()`

_Parameters:_

| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |


_Returns:_

None

_Example:_

Instantiating a `Collection` node named _"My Collection"_ and saving it to CRIPT

```python
my_project = cript.Project.get(name = "My project") # retrieves an already-created project
my_collection = cript.Collection(project=my_project, name="My collection")
my_collection.save()
```

---
### Get

_Definition:_

Retrieves a `Collection` that has already been saved in the CRIPT database. At least 1 of `uid`, `url`, or `name`  is required as an argument
to retrieve a `Collection` node. If retrieving via `name`, one should also provide a `Project uid` to the `project` parameter because `Collection` names are not unique across different `Projects`.

`cript.Collection.get(name, project, uid, url, **kwargs)`

_Parameters:_


| Name        | Type   | Description                                          | Default |
|-------------|--------|------------------------------------------------------|---------|
| `name`      | string | Name of the Collection to get                        | " "     |
| `project`   | string | Project uid that the Collection is nested inside of | " "     |
| `uid`       | string | UID of the specific Collection to get                | " "     |
| `url`       | string | URL of the specific Collection to get                | " "     |
| `**kwargs`  |        | Arguments for the constructor.                       | `{}`    |

_Returns:_

CRIPT `Collection` node of type `cript.data_model.nodes.BaseNode`

_Examples:_

Getting a `Collection` node via UID:
``` python
my_collection = cript.Collection.get(uid="015fc459-ea9f-4c37-80aa-f51d509095df")
```

Getting a `Collection` node via URL:
``` python
my_collection = cript.Collection.get(url="https://criptapp.org/collection/015fc459-ea9f-4c37-80aa-f51d509095df/")
```

Getting a `Collection` Node via name:

``` python
project = cript.Project.get(name="My project")
collection = cript.Collection.get(name="My collection", project=project.uid)
```

??? note "Why `Project uid` is needed"
    `Collection` names are only unique within a project, not across projects, so when getting a `Collection` via name, the associated `Project` node must also be specified.


---

### Update

_Definition:_

Updates a saved `Collection` node with new values

`cript.Collection.update(name, **kwargs)`

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `name`      | string | New name of the `Collection`                        | " "     |
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

_Returns:_

None

_Example:_

```python
my_collection.update(name="My new collection name")
```

---
### Refresh Collection

_Definition:_

Refreshes a node to get the latest saved values from CRIPT. It does not have any required arguments.

`cript.Collection.refresh()`


_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

_Example:_

```python
my_collection.refresh()
```

---

### Delete Collection

_Definition:_

Deletes a `Collection` node from CRIPT database. It does not have any required arguments.

`cript.Collection.delete()`

_Returns:_

None

_Parameters:_


| Name              | Type    | Description                                                    | Default |
|-------------------|---------|----------------------------------------------------------------|---------|
| `**kwargs`        |         | Arguments for the constructor.                                 | `{}`    |

_Example:_

```python
my_collection.delete()
```

---

### Search Collection

_Definition:_

Searches for a `Collection` within CRIPT based on query arguments. Unlike the previously described
methods, this method should not be used with a particular `Collection` instance. It requires at least 1 of the following 
arguments: `uid`, `url`, `name`, `project`, `experiments`.

`cript.Collection.search(uid, url, name, project, experiments, limit=None, offset=None, **kwargs)`

_Parameters:_


| Name        | Type             | Description                           | Default |
|-------------|------------------|---------------------------------------|---------|
| `url`                   | str                                                 | "https://criptapp.org/api/collection/336d0584-04f9-49fe-9c0d-78772e2f1ead/" | Unique URL for the node              | True     |
| `uid`                   | str                                                 | "336d0584-04f9-49fe-9c0d-78772e2f1ead" | Unique ID for the node                                                    | True     |
| `project`                 | [Project.uid](../nodes/project.md)                          |                          | Project associated with the `Collection` node                                           | True     |
| `name`                  | str                                                 | "Navid's collection"     | Name of the `Collection`  node                                                          | True     |
| `experiments`           | list[[Experiment.uid](experiment.md)]                   | [exp_1, exp_2, exp_3]    | Experiments that relate to the `Collection` node                                        | False    |
| `limit`     | Union[int, None] | The max number of items to return     | None    |
| `offset`    | Union[int, None] | The starting position of the query    | None    |
| `**kwargs`  |                  | Arguments for the constructor.        | `{}`    |

_Returns:_

A Paginator object of type `cript.data_model.paginator.Paginator`


_Example:_


```python
results = cript.Collection.search(name = "My collection")
results.json()
```

--->