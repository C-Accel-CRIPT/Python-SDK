from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.uuid_base import UUIDBaseNode


class Reference(UUIDBaseNode):
    """
    ## Definition

    The
    [Reference node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=15)

    contains the metadata for a literature publication, book, or anything external to CRIPT.
    The reference node does NOT contain the base attributes.

    The reference node is always used inside the citation
    sub-object to enable users to specify the context of the reference.

    ## Attributes
    | attribute | type      | example                                    | description                                   | required      | vocab |
    |-----------|-----------|--------------------------------------------|-----------------------------------------------|---------------|-------|
    | type      | str       | journal_article                            | type of literature                            | True          | True  |
    | title     | str       | 'Living' Polymers                          | title of publication                          | True          |       |
    | author   | list[str] | Michael Szwarc                             | list of authors                               |               |       |
    | journal   | str       | Nature                                     | journal of the publication                    |               |       |
    | publisher | str       | Springer                                   | publisher of publication                      |               |       |
    | year      | int       | 1956                                       | year of publication                           |               |       |
    | volume    | int       | 178                                        | volume of publication                         |               |       |
    | issue     | int       | 0                                          | issue of publication                          |               |       |
    | pages     | list[int] | [1168, 1169]                               | page range of publication                     |               |       |
    | doi       | str       | 10.1038/1781168a0                          | DOI: digital object identifier                | Conditionally |       |
    | issn      | str       | 1476-4687                                  | ISSN: international standard serial number    | Conditionally |       |
    | arxiv_id  | str       | 1501                                       | arXiv identifier                              |               |       |
    | pmid      | int       | ########                                   | PMID: PubMed ID                               |               |       |
    | website   | str       | https://www.nature.com/artic les/1781168a0 | website where the publication can be accessed |               |       |


    ## Available Subobjects
    * None

    !!! warning "Reference will always be public"
        Reference node is meant to always be public and static to allow globally link data to the reference
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        """
        all reference nodes attributes

        all int types are also None type in case they are not present it should be properly shown as None
        instead of a placeholder number such as 0 or -1
        """

        type: str = ""
        title: str = ""
        author: List[str] = field(default_factory=list)
        journal: str = ""
        publisher: str = ""
        year: int = None
        volume: int = None
        issue: int = None
        pages: List[int] = field(default_factory=list)
        doi: str = ""
        issn: str = ""
        arxiv_id: str = ""
        pmid: int = None
        website: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        type: str,
        title: str,
        author: List[str] = None,
        journal: str = "",
        publisher: str = "",
        year: int = None,
        volume: int = None,
        issue: int = None,
        pages: [int] = None,
        doi: str = "",
        issn: str = "",
        arxiv_id: str = "",
        pmid: int = None,
        website: str = "",
        **kwargs,
    ):
        """
        create a reference node

        reference type must come from CRIPT controlled vocabulary

        Parameters
        ----------
        type: str
            type of literature.
            The reference type must come from CRIPT controlled vocabulary
        title: str
            title of publication
        author: List[str] default=""
            list of authors
        journal: str default=""
            journal of publication
        publisher: str default=""
            publisher of publication
        year: int default=None
            year of publication
        volume: int default=None
            volume of publication
        issue: int default=None
            issue of publication
        pages: List[int] default=None
            page range of publication
        doi: str default=""
            DOI: digital object identifier
        issn: str default=""
            ISSN: international standard serial number
        arxiv_id: str default=""
            arXiv identifier
        pmid: int default=None
            PMID: PubMed ID
        website: str default=""
            website where the publication can be accessed


        Examples
        --------
        ```python
        my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")
        ```

        Returns
        -------
        None
            Instantiate a reference node
        """
        if author is None:
            author = []

        if pages is None:
            pages = []

        super().__init__(**kwargs)

        new_attrs = replace(self._json_attrs, type=type, title=title, author=author, journal=journal, publisher=publisher, year=year, volume=volume, issue=issue, pages=pages, doi=doi, issn=issn, arxiv_id=arxiv_id, pmid=pmid, website=website)

        self._update_json_attrs_if_valid(new_attrs)
        self.validate()

    # ------------------ Properties ------------------
    @property
    def type(self) -> str:
        """
        type of reference. The reference type must come from the CRIPT controlled vocabulary

        Examples
        --------
        ```python
        my_reference.type = "journal_article"
        ```

        Returns
        -------
        str
            reference type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_reference_type: str) -> None:
        """
        set the reference type attribute

        reference type must come from the CRIPT controlled vocabulary

        Parameters
        ----------
        new_reference_type: str

        Returns
        -------
        None
        """
        # TODO validate the reference type with CRIPT controlled vocabulary
        new_attrs = replace(self._json_attrs, type=new_reference_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def title(self) -> str:
        """
        title of publication

        Examples
        --------
        ```python
        my_reference.title = "my new title"
        ```

        Returns
        -------
        str
            title of publication
        """
        return self._json_attrs.title

    @title.setter
    def title(self, new_title: str) -> None:
        """
        set the title for the reference node

        Parameters
        ----------
        new_title: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, title=new_title)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def author(self) -> List[str]:
        """
        List of authors for this reference node

        Examples
        --------
        ```python
        my_reference.author = ["Bradley D. Olsen", "Dylan Walsh"]
        ```

        Returns
        -------
        List[str]
            list of authors
        """
        return self._json_attrs.author.copy()

    @author.setter
    def author(self, new_author: List[str]) -> None:
        """
        set the list of authors for the reference node

        Parameters
        ----------
        new_author: List[str]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, author=new_author)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def journal(self) -> str:
        """
        journal of publication

        Examples
        --------
        ```python
        my_reference.journal = "my new journal"
        ```

        Returns
        -------
        str
            journal of publication
        """
        return self._json_attrs.journal

    @journal.setter
    def journal(self, new_journal: str) -> None:
        """
        set the journal attribute for this reference node

        Parameters
        ----------
        new_journal: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, journal=new_journal)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def publisher(self) -> str:
        """
        publisher for this reference node

        Examples
        --------
        ```python
        my_reference.publisher = "my new publisher"
        ```

        Returns
        -------
        str
            publisher of this publication
        """
        return self._json_attrs.publisher

    @publisher.setter
    def publisher(self, new_publisher: str) -> None:
        """
        set the publisher for this reference node

        Parameters
        ----------
        new_publisher: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, publisher=new_publisher)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def year(self) -> int:
        """
        year for the scholarly work

        Examples
        --------
        ```python
        my_reference.year = 2023
        ```

        Returns
        -------
        int
        """
        return self._json_attrs.year

    @year.setter
    def year(self, new_year: int) -> None:
        """
        set the year for the scholarly work within the reference node

        Parameters
        ----------
        new_year: int


        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, year=new_year)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def volume(self) -> int:
        """
        Volume of the scholarly work from the reference node

        Examples
        --------
        ```python
        my_reference.volume = 1
        ```

        Returns
        -------
        int
            volume number of the publishing
        """
        return self._json_attrs.volume

    @volume.setter
    def volume(self, new_volume: int) -> None:
        """
        set the volume of the scholarly work for this reference node

        Parameters
        ----------
        new_volume: int

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, volume=new_volume)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def issue(self) -> int:
        """
        issue of the scholarly work for the reference node

        Examples
        --------
        ```python
        my_reference.issue = 2
        ```

        Returns
        -------
        None
        """
        return self._json_attrs.issue

    @issue.setter
    def issue(self, new_issue: int) -> None:
        """
        set the issue of the scholarly work

        Parameters
        ----------
        new_issue: int

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, issue=new_issue)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def pages(self) -> List[int]:
        """
        pages of the scholarly work used in the reference node

        Examples
        --------
        ```python
        my_reference.pages = [123, 456]
        ```

        Returns
        -------
        int
        """
        return self._json_attrs.pages.copy()

    @pages.setter
    def pages(self, new_pages_list: List[int]) -> None:
        """
        set the list of pages of the scholarly work for this reference node

        Parameters
        ----------
        new_pages_list: List[int]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, pages=new_pages_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def doi(self) -> str:
        """
        get the digital object identifier (DOI) for this reference node

        Examples
        --------
        ```python
        my_reference.doi = "100.1038/1781168a0"
        ```

        Returns
        -------
        str
            digital object identifier (DOI) for this reference node
        """
        return self._json_attrs.doi

    @doi.setter
    def doi(self, new_doi: str) -> None:
        """
        set the digital object identifier (DOI) for the scholarly work for this reference node

        Parameters
        ----------
        new_doi: str

        Examples
        --------
        ```python
        my_reference.doi = "100.1038/1781168a0"
        ```

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, doi=new_doi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def issn(self) -> str:
        """
        The international standard serial number (ISSN) for this reference node

        Examples
        ```python
        my_reference.issn = "1456-4687"
        ```

        Returns
        -------
        str
            ISSN for this reference node
        """
        return self._json_attrs.issn

    @issn.setter
    def issn(self, new_issn: str) -> None:
        """
        set the international standard serial number (ISSN) for the scholarly work for this reference node

        Parameters
        ----------
        new_issn: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, issn=new_issn)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def arxiv_id(self) -> str:
        """
        The arXiv identifier for the scholarly work for this reference node

        Examples
        --------
        ```python
        my_reference.arxiv_id = "1501"
        ```

        Returns
        -------
        str
            arXiv identifier for the scholarly work for this publishing
        """
        return self._json_attrs.arxiv_id

    @arxiv_id.setter
    def arxiv_id(self, new_arxiv_id: str) -> None:
        """
        set the arXiv identifier for the scholarly work for this reference node

        Parameters
        ----------
        new_arxiv_id: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, arxiv_id=new_arxiv_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def pmid(self) -> int:
        """
        The PubMed ID (PMID) for this reference node

        Examples
        --------
        ```python
        my_reference.pmid = 12345678
        ```

        Returns
        -------
        int
            the PubMedID of this publishing
        """
        return self._json_attrs.pmid

    @pmid.setter
    def pmid(self, new_pmid: int) -> None:
        """

        Parameters
        ----------
        new_pmid

        Returns
        -------

        """
        # TODO can possibly add validations, possibly in forms of length checking
        #  to be sure its the correct length
        new_attrs = replace(self._json_attrs, pmid=new_pmid)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def website(self) -> str:
        """
        The website URL for the scholarly work

        Examples
        --------
        ```python
        my_reference.website = "https://criptapp.org"
        ```

        Returns
        -------
        str
            the website URL of this publishing
        """
        return self._json_attrs.website

    @website.setter
    def website(self, new_website: str) -> None:
        """
        set the website URL for the scholarly work

        Parameters
        ----------
        new_website: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, website=new_website)
        self._update_json_attrs_if_valid(new_attrs)
