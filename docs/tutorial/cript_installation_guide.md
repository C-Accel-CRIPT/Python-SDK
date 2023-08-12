# How to Install CRIPT

!!! abstract

    This page will give you a through guide on how to install the 
    [CRIPT Python SDK](https://pypi.org/project/cript/) on your system.

## Steps

1.  Install [Python 3.7+](https://www.python.org/downloads/)
2.  Create a virtual environment

    > It is best practice to create a dedicated [python virtual environment](https://docs.python.org/3/library/venv.html) for each python project

    === ":fontawesome-brands-windows: **_Windows:_**"
        ```bash 
        python -m venv .\venv
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ```bash 
        python3 -m venv ./venv
        ```

3.  Activate your virtual environment

    === ":fontawesome-brands-windows: **_Windows:_**"
        ```bash 
        .\venv\Scripts\activate
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ```bash 
        source venv/bin/activate
        ```

4.  Install [CRIPT from Python Package Index (PyPI)](https://pypi.org/project/cript/)
    ```bash
     pip install cript
    ```
5.  Create your CRIPT Script!


??? info "Install Package From our [GitHub](https://github.com/C-Accel-CRIPT/Python-SDK)"
    Please note that it is also possible to install this package from our 
    [GitHub](https://github.com/C-Accel-CRIPT/Python-SDK).

    Formula: `pip install git+[repository URL]@[branch or tag]`

    Install from [Main](https://github.com/C-Accel-CRIPT/Python-SDK/tree/main): 
    `pip install git+https://github.com/C-Accel-CRIPT/Python-SDK@main`
    
    or to download the latest in [development code](https://github.com/C-Accel-CRIPT/Python-SDK/tree/develop)
    `pip install git+https://github.com/C-Accel-CRIPT/Python-SDK@develop`

