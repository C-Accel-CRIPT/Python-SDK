import copy
import json

import pytest

import cript


def test_create_simple_reference() -> None:
    """
    tests to see if a simple reference node with only minimal arguments can be successfully created
    """
    my_reference_type = "journal_article"
    my_reference_title = "'Living' Polymers"

    my_reference = cript.Reference(type=my_reference_type, title=my_reference_title)

    assert isinstance(my_reference, cript.Reference)
    assert my_reference.type == my_reference_type
    assert my_reference.title == my_reference_title


@pytest.fixture(scope="session")
def complex_reference() -> None:
    """
    tests that a complex reference node with all optional parameters can be made
    """

    # reference attributes
    reference_type = "journal_article"
    title = "'Living' Polymers"
    authors = ["Dylan J. Walsh", "Bradley D. Olsen"]
    journal = "Nature"
    publisher = "Springer"
    year = 2019
    volume = 3
    issue = 5
    pages = [123, 456, 789]
    doi = "10.1038/1781168a0"
    issn = "1476-4687"
    arxiv_id = "1501"
    pmid = 12345678
    website = "https://criptapp.org"

    # create complex reference node
    my_reference = cript.Reference(
        type=reference_type,
        title=title,
        authors=authors,
        journal=journal,
        publisher=publisher,
        year=year,
        volume=volume,
        issue=issue,
        pages=pages,
        doi=doi,
        issn=issn,
        arxiv_id=arxiv_id,
        pmid=pmid,
        website=website,
    )

    # create a copy to keep the original state
    my_reference_copy = copy.deepcopy(my_reference)
    yield my_reference_copy


def test_complex_reference(complex_reference) -> None:
    """
    testing that the complex reference node is working correctly
    """

    # complex reference node's attributes
    reference_type = "journal_article"
    title = "'Living' Polymers"
    authors = ["Dylan J. Walsh", "Bradley D. Olsen"]
    journal = "Nature"
    publisher = "Springer"
    year = 2019
    volume = 3
    issue = 5
    pages = [123, 456, 789]
    doi = "10.1038/1781168a0"
    issn = "1476-4687"
    arxiv_id = "1501"
    pmid = 12345678
    website = "https://criptapp.org"

    # assertions
    assert isinstance(complex_reference, cript.Reference)
    assert complex_reference.type == reference_type
    assert complex_reference.title == title
    assert complex_reference.authors == authors
    assert complex_reference.journal == journal
    assert complex_reference.publisher == publisher
    assert complex_reference.publisher == publisher
    assert complex_reference.year == year
    assert complex_reference.volume == volume
    assert complex_reference.issue == issue
    assert complex_reference.pages == pages
    assert complex_reference.doi == doi
    assert complex_reference.issn == issn
    assert complex_reference.arxiv_id == arxiv_id
    assert complex_reference.pmid == pmid
    assert complex_reference.website == website


def test_reference_vocabulary() -> None:
    """
    tests that a reference node type with valid CRIPT controlled vocabulary runs successfully
    and invalid reference type gives the correct errors
    """
    pass


def test_reference_conditional_attributes() -> None:
    """
    test conditional attributes (DOI and ISSN) that they are validating correctly
    and that an error is correctly raised when they are needed but not provided
    """
    pass


def test_serialize_reference_to_json() -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """
    # create reference node
    my_reference = cript.Reference(
        type="journal_article",
        title="Adding the Effect of Topological Defects to the Flory\u2013Rehner and Bray\u2013Merrill Swelling Theories",
        authors=["Nathan J. Rebello", "Haley K. Beech", "Bradley D. Olsen"],
        journal="ACS Macro Letters",
        publisher="American Chemical Society",
        year=2022,
        pages=[531, 537],
        doi="10.1021/acsmacrolett.0c00909",
    )

    expected_reference_dict = {
        "node": "Reference",
        "url": "",
        "type": "journal_article",
        "title": "Adding the Effect of Topological Defects to the Flory\u2013Rehner and Bray\u2013Merrill Swelling Theories",
        "author": ["Nathan J. Rebello", "Haley K. Beech", "Bradley D. Olsen"],
        "journal": "ACS Macro Letters",
        "publisher": "American Chemical Society",
        "year": 2022,
        "volume": 10,
        "pages": [531, 537],
        "doi": "10.1021/acsmacrolett.0c00909",
    }

    # convert reference to json and then to dict for better comparison
    my_reference = my_reference.json
    my_reference = json.loads(my_reference)

    print("\n \n")
    print(expected_reference_dict)
    print("\n \n")
    print(my_reference)

    assert my_reference == expected_reference_dict


# ---------- Integration tests ----------
def test_save_reference_to_api() -> None:
    """
    tests if the reference node can be saved to the API without errors and status code of 200
    """
    pass


def test_get_reference_from_api() -> None:
    """
    integration test: gets the reference node from the api that was saved prior
    """
    pass


def test_serialize_json_to_data() -> None:
    """
    tests that a JSON of a reference node can be correctly converted to python object
    """
    pass


def test_update_data_in_api() -> None:
    """
    reference nodes are immutable
    attempting to update a reference node should return an error from the API
    """
    pass


def test_delete_reference_from_api() -> None:
    """
    reference nodes are immutable, attempting to delete a reference node should return an error from the API
    """
    pass


def test_reference_url() -> None:
    """
    tests that the reference URL is correctly made using the UUID

    Returns
    -------
    None
    """
    pass
