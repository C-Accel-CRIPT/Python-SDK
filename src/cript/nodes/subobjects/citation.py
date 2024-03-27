from dataclasses import dataclass, replace
from typing import Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.reference import Reference
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Citation(UUIDBaseNode):
    """
    ## Definition
    The [Citation sub-object](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=26)
    essentially houses [Reference nodes](../../primary_nodes/reference). The citation subobject can then be added to CRIPT Primary nodes.

    ## Attributes
    | attribute | type      | example      | description                                   | required | vocab |
    |-----------|-----------|--------------|-----------------------------------------------|----------|-------|
    | type      | str       | derived_from | key for identifier                            | True     | True  |
    | reference | Reference |              | reference to a book, paper, or scholarly work | True     |       |

    ## Can Be Added To
    * [Collection node](../../primary_nodes/collection)
    * [Computation node](../../primary_nodes/computation)
    * [Computation Process Node](../../primary_nodes/computation_process)
    * [Data node](../../primary_nodes/data)

    * [Computational Forcefield subobjects](../computational_forcefield)
    * [Property subobject](../property)
    * [Algorithm subobject](../algorithm)
    * [Equipment subobject](../equipment)

    ---

    ## Available Subobjects
    * `None`

    ## JSON Representation
    ```json
    "citation": {
            "node": ["Citation"],
            "type": "reference",
            "reference": {
                    "node": ["Reference"],
                    "type": "journal_article",
                    "title": "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: SOft coarse grained Monte-Carlo Acceleration (SOMA)",
                    "author": ["Ludwig Schneider", "Marcus Müller"],
                    "journal": "Computer Physics Communications",
                    "publisher": "Elsevier",
                    "year": 2019,
                    "pages": [463, 476],
                    "doi": "10.1016/j.cpc.2018.08.011",
                    "issn": "0010-4655",
                    "website": "https://www.sciencedirect.com/science/article/pii/S0010465518303072",
            },
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        type: str = ""
        reference: Optional[Union[Reference, UIDProxy]] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(self, type: str, reference: Union[Reference, UIDProxy], **kwargs):
        """
        create a Citation subobject

        Parameters
        ----------
        type : citation type
            citation type must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/citation_type)
        reference : Reference
            Reference node

        Examples
        -------
        >>> import cript
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     "journal_article",
        ...     title=title,
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="reference", reference=my_reference)


        Returns
        -------
        None
            Instantiate citation subobject
        """
        super().__init__(**kwargs)
        new_json_attrs = replace(self._json_attrs, type=type, reference=reference)
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        Citation type subobject

        Citation type must come from [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/citation_type)

        Examples
        --------
        >>> import cript
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     "journal_article",
        ...     title=title,
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="reference", reference=my_reference)
        >>> my_citation.type = "extracted_by_algorithm"

        Returns
        -------
        str
            Citation type
        """
        return self._json_attrs.type

    @type.setter
    @beartype
    def type(self, new_type: str) -> None:
        """
        set the citation sub-object type

        Parameters
        ----------
        new_type : str
            citation type

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def reference(self) -> Union[Reference, None, UIDProxy]:
        """
        citation reference node

        Examples
        --------
        >>> import cript
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     "journal_article",
        ...     title=title,
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="reference", reference=my_reference)
        >>> my_new_reference = cript.Reference(
        ...     type="journal_article",
        ...     title="'Living' Polymers",
        ...     author=["Dylan J. Walsh", "Bradley D. Olsen"],
        ...     journal="Nature",
        ...     publisher="Springer",
        ...     year=2019,
        ...     volume=3,
        ...     issue=5,
        ...     pages=[123, 456, 789],
        ...     doi="10.1038/1781168a0",
        ...     issn="1476-4687",
        ...     arxiv_id="1501",
        ...     pmid=12345678,
        ...     website="https://criptapp.org",
        ... )
        >>> my_citation.reference = my_new_reference

        Returns
        -------
        Reference
            Reference node
        """
        return self._json_attrs.reference

    @reference.setter
    @beartype
    def reference(self, new_reference: Reference) -> None:
        """
        replace the current Reference node for the citation subobject

        Parameters
        ----------
        new_reference : Reference

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, reference=new_reference)
        self._update_json_attrs_if_valid(new_attrs)
