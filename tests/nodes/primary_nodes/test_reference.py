import json
import uuid
import warnings

from integration_test_helper import integrate_nodes_helper
from util import strip_uid_from_dict

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


def test_complex_reference() -> None:
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
        author=authors,
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

    # assertions
    assert isinstance(my_reference, cript.Reference)
    assert my_reference.type == reference_type
    assert my_reference.title == title
    assert my_reference.author == authors
    assert my_reference.journal == journal
    assert my_reference.publisher == publisher
    assert my_reference.year == year
    assert my_reference.volume == volume
    assert my_reference.issue == issue
    assert my_reference.pages == pages
    assert my_reference.doi == doi
    assert my_reference.issn == issn
    assert my_reference.arxiv_id == arxiv_id
    assert my_reference.pmid == pmid
    assert my_reference.website == website


def test_getters_and_setters_reference(complex_reference_node) -> None:
    """
    testing that the complex reference node is working correctly
    """

    # new attributes for the setter
    reference_type = "journal_article"
    title = "my title"
    authors = ["Ludwig Schneider"]
    journal = "my journal"
    publisher = "my publisher"
    year = 2023
    volume = 1
    issue = 2
    pages = [123, 456]
    doi = "100.1038/1781168a0"
    issn = "1456-4687"
    arxiv_id = "1501"
    pmid = 12345678
    website = "https://criptapp.org"

    # set reference attributes
    complex_reference_node.type = reference_type
    complex_reference_node.title = title
    complex_reference_node.author = authors
    complex_reference_node.journal = journal
    complex_reference_node.publisher = publisher
    complex_reference_node.year = year
    complex_reference_node.volume = volume
    complex_reference_node.issue = issue
    complex_reference_node.pages = pages
    complex_reference_node.doi = doi
    complex_reference_node.issn = issn
    complex_reference_node.arxiv_id = arxiv_id
    complex_reference_node.pmid = pmid
    complex_reference_node.website = website

    # assertions: test getter and setter
    assert isinstance(complex_reference_node, cript.Reference)
    assert complex_reference_node.type == reference_type
    assert complex_reference_node.title == title
    assert complex_reference_node.author == authors
    assert complex_reference_node.journal == journal
    assert complex_reference_node.publisher == publisher
    assert complex_reference_node.year == year
    assert complex_reference_node.volume == volume
    assert complex_reference_node.issue == issue
    assert complex_reference_node.pages == pages
    assert complex_reference_node.doi == doi
    assert complex_reference_node.issn == issn
    assert complex_reference_node.arxiv_id == arxiv_id
    assert complex_reference_node.pmid == pmid
    assert complex_reference_node.website == website

    # remove optional attributes
    complex_reference_node.author = []
    complex_reference_node.journal = ""
    complex_reference_node.publisher = ""
    complex_reference_node.year = None
    complex_reference_node.volume = None
    complex_reference_node.issue = None
    complex_reference_node.pages = []
    complex_reference_node.doi = ""
    complex_reference_node.issn = ""
    complex_reference_node.arxiv_id = ""
    complex_reference_node.pmid = None
    complex_reference_node.website = ""
    
    # assert optional attributes have been removed
    assert complex_reference_node.author == []
    assert complex_reference_node.journal == ""
    assert complex_reference_node.publisher == ""
    assert complex_reference_node.year == None
    assert complex_reference_node.volume == None
    assert complex_reference_node.issue == None
    assert complex_reference_node.pages == []
    assert complex_reference_node.doi == ""
    assert complex_reference_node.issn == ""
    assert complex_reference_node.arxiv_id == ""
    assert complex_reference_node.pmid == None
    assert complex_reference_node.website == ""


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


def test_serialize_reference_to_json(complex_reference_node, complex_reference_dict) -> None:
    """
    tests that it can correctly turn the data node into its equivalent JSON
    """

    # convert reference to json and then to dict for better comparison
    reference_dict = json.loads(complex_reference_node.json)
    reference_dict = strip_uid_from_dict(reference_dict)

    assert reference_dict == complex_reference_dict


def test_integration_reference(cript_api, simple_project_node, complex_citation_node, complex_reference_node):
    """
    integration test between Python SDK and API Client

    1. POST to API
    1. GET from API
    1. assert they're both equal

    Notes
    -----
    indirectly tests citation node along with reference node
    """
    # ========= test create =========
    simple_project_node.name = f"test_integration_reference_name_{uuid.uuid4().hex}"

    simple_project_node.collection[0].citation = [complex_citation_node]

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)

    # TODO deserialization with citation in collection is wrong
    # raise Exception("Citation is missing from collection node from API")
    warnings.warn("Uncomment the Reference integration test Exception and check the API response has citation on collection")

    # ========= test update =========
    # change simple attribute to trigger update
    #   TODO can enable this later
    #  complex_reference_node.type = "book"
    simple_project_node.collection[0].citation[0].reference.title = "reference title UPDATED"

    integrate_nodes_helper(cript_api=cript_api, project_node=simple_project_node)
