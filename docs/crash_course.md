# CRIPT Python SDK Crash Course

This Crash Course will guide you through some common commands of the CRIPT Python SDK.

---

## Install CRIPT

```bash
pip install cript
```

> It is recommended to install the <a href="https://pypi.org/project/cript/" target="_blank">CRIPT package</a> inside
> a [Python virtual environment](https://docs.python.org/3/library/venv.html).

For more please refer to <a href="../tutorials/installation" target="_blank">CRIPT installation guide</a>.

---

## Connect to CRIPT

Your API token can be found on the [CRIPT security settings page]().

!!! warning "Security Warning"
    It is **highly** recommended that you store your API token as an environment variable

## Directly Inputting Host and Token
``` python
import cript
import os

host = "criptapp.org"  # or any host eg. myPrivateWebsite.come
token = os.environ.get("CRIPT_API_KEY") # getting token via environment variable
cript.API(host, token)
```

## Getting Host and Token from Environment Variables
```python

```

## Create API Client Object with Configuration File
```python

```

---

## Create a Project
```python

```

## Create a Collection
```python

```

## Experiment
```python

```

## Add Process
```python

```

## Add Data
```python

```

## Add File
```python

```

## Create Reference
```python

```

## Add Citation
```python

```

## Save Your Data to CRIPT Database
```python

```

## View Your Data
```python

```
