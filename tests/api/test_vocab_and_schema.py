import pytest

# from cript.api.schema_validation import _get_db_schema
# from cript.api.vocabulary import _get_controlled_vocabulary


@pytest.fixture(scope="session")
def cript_api():
    """
    Create an API instance for the rest of the tests to use.

    Returns:
        API: The created API instance.
    """
    pass


def test_get_db_schema(cript_api):
    """
    just checks if that function gives anything back or not.

    Parameters
    ----------
    cript_api

    Returns
    -------
    NoneType
        None

    """
    # return _get_db_schema()
    pass


def test_db_schema_success(cript_api):
    """
    Tests a valid material node JSON against the DB Schema, and it should pass

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_db_schema_fail(cript_api):
    """

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_get_vocabulary(cript_api):
    """
    just checks if that function can successfully get a JSON response or not.

    Parameters
    ----------
    cript_api

    Returns
    -------
    NoneType
        None
    """
    # return _get_controlled_vocabulary()
    pass


def test_vocabulary_success(cript_api):
    """
    Test a material node with a BigSmiles identifier.
    The vocabulary should be correct and pass.

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass


def test_vocabulary_fail(cript_api):
    """
    Test a material node with invalid vocabulary for identifier.
    This test is expected to fail

    Parameters
    ----------
    cript_api

    Returns
    -------
    None
    """
    pass
