from dataclasses import dataclass, replace
from typing import Union

from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.reference import Reference


class Citation(BaseNode):
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
    ### Primary Nodes
    * [Collection node](../../primary_nodes/collection)
    * [Computation node](../../primary_nodes/computation)
    * [Computation Process Node](../../primary_nodes/computation_process)
    * [Data node](../../primary_nodes/data)

    ### Subobjects
    * [Computational Forecefield subobjects](../computational_forcefield)
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
    class JsonAttributes(BaseNode.JsonAttributes):
        type: str = ""
        reference: Union[Reference, None] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, type: str, reference: Reference, **kwargs):
        """
        create a Citation subobject

        Parameters
        ----------
        type : citation type
            citation type must come from [CRIPT Controlled Vocabulary]()
        reference : Reference
            Reference node

        Examples
        -------
        ```python
        title = "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        title += "SOft coarse grained Monte-Carlo Acceleration (SOMA)"

        # create a Reference node for the Citation subobject
        my_reference = Reference(
            "journal_article",
            title=title,
            author=["Ludwig Schneider", "Marcus Müller"],
            journal="Computer Physics Communications",
            publisher="Elsevier",
            year=2019,
            pages=[463, 476],
            doi="10.1016/j.cpc.2018.08.011",
            issn="0010-4655",
            website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        )

        # create Citation subobject
        my_citation = cript.Citation("reference", my_reference)
        ```

        Returns
        -------
        None
            Instantiate citation subobject
        """
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, type=type, reference=reference)
        self.validate()

    @property
    def type(self) -> str:
        """
        Citation type subobject

        > Note: Citation type must come from [CRIPT Controlled Vocabulary]()

        Examples
        --------
        ```python
        my_citation.type = "extracted_by_algorithm"
        ```

        Returns
        -------
        str
            Citation type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str) -> None:
        """
        set the citation subobject type

        > Note: citation subobject must come from [CRIPT Controlled Vocabulary]()

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
    def reference(self) -> Reference:
        """
        citation reference node

        Examples
        --------
        ```python
        # create a Reference node for the Citation subobject
        my_reference = Reference(
            "journal_article",
            title="my title",
            author=["Ludwig Schneider", "Marcus Müller"],
            journal="Computer Physics Communications",
            publisher="Elsevier",
            year=2019,
            pages=[463, 476],
            doi="10.1016/j.cpc.2018.08.011",
            issn="0010-4655",
            website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        )

        my_citation.reference = my_reference
        ```

        Returns
        -------
        Reference
            Reference node
        """
        return self._json_attrs.reference

    @reference.setter
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
