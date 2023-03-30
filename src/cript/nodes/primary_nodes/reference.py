from dataclasses import dataclass, replace
from typing import List, Union

from cript.nodes.core import BaseNode


class Reference(BaseNode):
    """
    Reference node

    [Reference](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=15)

    Reference does not inherit from the PrimaryBaseNode unlike other primary nodes
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all reference nodes attributes

        all int types are also None type in case they are not present it should be properly shown as None instead of a placeholder number such as 0 or -1
        """

        node: str = "Reference"
        url: str = ""
        type: str = ""
        title: str = ""
        authors: List[str] = ""
        journal: str = ""
        publisher: str = ""
        year: int = None
        volume: int = None
        issue: int = None
        pages: List[int] = None
        doi: str = ""
        issn: str = ""
        arxiv_id: str = ""
        pmid: int = None
        website: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    # TODO fix the constructor
    def __init__(
        self,
        type: str,
        title: str,
        url: str = "",
        authors: List[str] = None,
        journal: str = "",
        publisher: str = "",
        year: Union[int, None] = None,
        volume: Union[int, None] = None,
        issue: int = Union[int, None],
        pages: Union[List[int], None] = None,
        doi: str = "",
        issn: str = "",
        arxiv_id: str = "",
        pmid: int = Union[int, None],
        website: str = "",
        **kwargs
    ):
        """
        create a reference node

        the only required attributes to create a reference node are:
            * url
            * type
            * title

        reference type must come from CRIPT controlled vocabulary

        Parameters
        ----------
        url: str
        type: str
        title: str
        authors: List[str] default=""
        journal: str default=""
        publisher: str default=""
        year: int default=None
        volume: int default=None
        issue: int default=None
        pages: List[int] default=None
        doi: str default=""
        issn: str default=""
        arxiv_id: str default=""
        pmid: int default=None
        website: str default=""

        there is currently no checks for conditional required fields for doi and issn
        """
        super().__init__(node="Reference")

        new_attrs = replace(
            self._json_attrs,
            url=url,
            type=type,
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

        self._update_json_attrs_if_valid(new_attrs)
        self.validate()

    @property
    def url(self) -> str:
        """
        get the url attribute for the reference node

        Notes
        -----
        Can only get the URL and not set it.
        Only the API can assign URLs to nodes

        Returns
        -------
        str
        """
        # TODO need to create the URl from the UUID
        return self._json_attrs.str

    @property
    def type(self) -> str:
        """
        get the reference type

        the reference type must come from the CRIPT controlled vocabulary

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
        get the reference title

        Returns
        -------
        str
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
    def authors(self) -> List[str]:
        """
        get the list of authors for this reference node

        Returns
        -------
        List[str]
        """
        return self._json_attrs.authors.copy()

    @authors.setter
    def authors(self, new_authors_list: List[str]) -> None:
        """
        set the list of authors for the reference node

        Parameters
        ----------
        new_authors_list: List[str]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, authors=new_authors_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def journal(self) -> str:
        """
        get the journal for this reference node

        Returns
        -------
        str
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
        get the publisher for this reference node

        Returns
        -------
        str
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
        get the year for the scholarly work

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
        get the volume of the scholarly work from the reference node

        Returns
        -------
        None
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
        get the issue of the scholarly work from the reference node

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
        gets the pages of the scholarly work from this reference node

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

        Returns
        -------
        None
        """
        return self._json_attrs.doi

    @doi.setter
    def doi(self, new_doi: str) -> None:
        """
        set the digital object identifier (DOI) for the scholarly work for this reference node

        Parameters
        ----------
        new_doi: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, doi=new_doi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def issn(self) -> str:
        """
        get the international standard serial number (ISSN) for this reference node

        Returns
        -------
        str
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
        get the arXiv identifier for the scholarly work for this reference node

        Returns
        -------
        str
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
        get the PubMed ID (PMID) for this reference node

        Returns
        -------
        int
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
        get the website URL for the scholarly work

        Returns
        -------
        str
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
