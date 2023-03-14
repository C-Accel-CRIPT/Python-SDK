import copy
from typing import Union, List
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from dataclasses import dataclass, replace, field


class Reference(PrimaryBaseNode):
    """
    Reference node
    """
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        node: str = "Reference"
        type: str = ""
        title: str = ""
        authors: List[str] = field(default_factory=list)
        journal: Union[str, None] = None
        publisher: Union[str, None] = None
        year: Union[int, None] = None
        issue: Union[int, None] = None
        pages: Union[List[int], None] = None
        doi: Union[str, None] = None
        issn: Union[str, None] = None
        arxiv_id: Union[str, None] = None
        pmid: Union[int, None] = None
        website: Union[str, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, type: str, title: str = "",
                 authors: Union[List[str], None] = None,
                 journal: Union[str, None] = None,
                 publisher: Union[str, None] = None,
                 year: Union[int, None] = None,
                 issue: Union[int, None] = None,
                 pages: Union[List[int], None] = None,
                 doi: Union[str, None] = None,
                 issn: Union[str, None] = None,
                 arxiv_id: Union[str, None] = None,
                 pmid: Union[int, None] = None,
                 website: Union[str, None] = None
                 ):
        if authors is None: authors = []
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
    def type(self) -> str:
        return self._json_attrs.type
    @type.setter
    def type(self, new_type:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, type=new_type)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, type=new_type)
        self.validate()

    @property
    def title(self) -> str:
        return self._json_attrs.title
    @title.setter
    def title(self, new_title:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, title=new_title)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, title=new_title)
        self.validate()

    @property
    def authors(self) -> List[str]:
        return self._json_attrs.authors.copy()
    @authors.setter
    def authors(self, new_authors:List[str]):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, authors=new_authors)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, authors=new_authors)
        self.validate()

    @property
    def journal(self) -> str:
        return self._json_attrs.journal
    @journal.setter
    def journal(self, new_journal:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, journal=new_journal)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, journal=new_journal)
        self.validate()

    @property
    def publisher(self) -> str:
        return self._json_attrs.publisher
    @publisher.setter
    def publisher(self, new_publisher:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, publisher=new_publisher)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, publisher=new_publisher)
        self.validate()

    @property
    def year(self) -> int:
        return self._json_attrs.year
    @year.setter
    def year(self, new_year:int):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, year=new_year)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, year=new_year)
        self.validate()

    @property
    def issue(self) -> str:
        return self._json_attrs.issue
    @issue.setter
    def issue(self, new_issue:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, issue=new_issue)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, issue=new_issue)
        self.validate()

    @property
    def pages(self) -> List[int]:
        return self._json_attrs.pages
    @pages.setter
    def pages(self, new_pages:List[int]):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, pages=new_pages)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, pages=new_pages)
        self.validate()

    @property
    def doi(self) -> str:
        return self._json_attrs.doi
    @doi.setter
    def doi(self, new_doi:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, doi=new_doi)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, doi=new_doi)
        self.validate()

    @property
    def issn(self) ->str:
        return self._json_attrs.issn
    @issn.setter
    def issn(self, new_issn:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, issn=new_issn)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, issn=new_issn)
        self.validate()

    @property
    def arxiv_id(self) -> str:
        return self._json_attrs.arxiv_id

    @arxiv_id.setter
    def arxiv_id(self, new_id:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, arxiv_id=new_id)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, arxiv_id=new_id)
        self.validate()

    @property
    def pmid(self) -> int:
        return self._json_attrs.pmid
    @pmid.setter
    def pmid(self, new_pmid:int):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, pmid=new_pmid)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, pmid=new_pmid)
        self.validate()

    @property
    def website(self) -> str:
        return self._json_attrs.website
    @website.setter
    def website(self, new_website:str):
        tmp = copy(self)
        tmp._json_attrs = replace(tmp._json_attrs, website=new_website)
        tmp.validate()
        self._json_attrs = replace(self._json_attrs, website=new_website)
        self.validate()
