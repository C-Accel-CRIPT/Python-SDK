from typing import Union, List
from cript.nodes.core import BaseNode
from dataclasses import dataclass, replace, field


class Reference(BaseNode):
    """
    Reference node
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node: str = "Reference"
        url: str = ""
        type: str = ""
        title: str = ""
        authors: List[str] = field(default_factory=list)
        journal: str = ""
        publisher: str = ""
        year: Union[int, None] = None
        issue: Union[int, None] = None
        pages: List[int] = field(default_factory=list)
        doi: str = ""
        issn: str = ""
        arxiv_id: str = ""
        pmid: Union[int, None] = None
        website: str = ""

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, type: str, title: str = "",
                 authors: Union[List[str], None] = None,
                 journal: str = "",
                 publisher: str = "",
                 year: Union[int, None] = None,
                 issue: Union[int, None] = None,
                 pages: Union[List[int], None] = None,
                 doi: str = "",
                 issn: str = "",
                 arxiv_id: str = "",
                 pmid: Union[int, None] = None,
                 website: str = "",
                 **kwargs # ignored
                 ):
        if authors is None: authors = []
        if pages is None: pages = []
        super().__init__("Reference")
        self._json_attrs = replace(self._json_attrs,
                                   type=type,
                                   title=title,
                                   authors = authors,
                                   journal = journal,
                                   publisher = publisher,
                                   year = year,
                                   issue = issue,
                                   pages = pages,
                                   doi = doi,
                                   issn = issn,
                                   arxiv_id = arxiv_id,
                                   pmid = pmid,
                                   website = website)
        self.validate()


    @property
    def type(self):
        return self._json_attrs.type

    @type.setter
    def type(self, new_type):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def title(self) -> str:
        return self._json_attrs.title
    @title.setter
    def title(self, new_title:str):
        new_attrs = replace(self._json_attrs, title=new_title)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def authors(self) -> List[str]:
        return self._json_attrs.authors.copy()
    @authors.setter
    def authors(self, new_authors:List[str]):
        new_attrs = replace(self._json_attrs, authors=new_authors)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def journal(self) -> str:
        return self._json_attrs.journal
    @journal.setter
    def journal(self, new_journal:str):
        new_attrs = replace(self._json_attrs, journal=new_journal)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def publisher(self) -> str:
        return self._json_attrs.publisher
    @publisher.setter
    def publisher(self, new_publisher:str):
        new_attrs = replace(self._json_attrs, publisher=new_publisher)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def year(self) -> int:
        return self._json_attrs.year
    @year.setter
    def year(self, new_year:int):
        new_attrs = replace(self._json_attrs, year=new_year)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def issue(self) -> str:
        return self._json_attrs.issue
    @issue.setter
    def issue(self, new_issue:str):
        new_attrs = replace(self._json_attrs, issue=new_issue)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def pages(self) -> List[int]:
        return self._json_attrs.pages
    @pages.setter
    def pages(self, new_pages:List[int]):
        new_attrs = replace(self._json_attrs, pages=new_pages)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def doi(self) -> str:
        return self._json_attrs.doi
    @doi.setter
    def doi(self, new_doi:str):
        new_attrs = replace(self._json_attrs, doi=new_doi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def issn(self) ->str:
        return self._json_attrs.issn
    @issn.setter
    def issn(self, new_issn:str):
        new_attrs = replace(self._json_attrs, issn=new_issn)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def arxiv_id(self) -> str:
        return self._json_attrs.arxiv_id

    @arxiv_id.setter
    def arxiv_id(self, new_id:str):
        new_attrs = replace(self._json_attrs, arxiv_id=new_id)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def pmid(self) -> int:
        return self._json_attrs.pmid
    @pmid.setter
    def pmid(self, new_pmid:int):
        new_attrs = replace(self._json_attrs, pmid=new_pmid)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def website(self) -> str:
        return self._json_attrs.website
    @website.setter
    def website(self, new_website:str):
        new_attrs = replace(self._json_attrs, website=new_website)
        self._update_json_attrs_if_valid(new_attrs)
