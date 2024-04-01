from dataclasses import dataclass, field, replace
from typing import Any, List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.supporting_nodes import User
from cript.nodes.util.json import UIDProxy


class Collection(PrimaryBaseNode):
    """
    ## Definition

    A
    [Collection node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=8)
    is nested inside a [Project](../project) node.

    A Collection node can be thought as a folder/bucket that can hold [experiment](../experiment)
    or [Inventories](../inventory) node.

    | attribute  | type             | example             | description                                                                    |
    |------------|------------------|---------------------|--------------------------------------------------------------------------------|
    | experiment | list[Experiment] |                     | experiment that relate to the collection                                       |
    | inventory  | list[Inventory]  |                     | inventory owned by the collection                                              |
    | doi        | str              | `10.1038/1781168a0` | DOI: digital object identifier for a published collection; CRIPT generated DOI |
    | citation   | list[Citation]   |                     | reference to a book, paper, or scholarly work                                  |
    | notes      | str              | "my awesome notes"  | miscellaneous information, or custom data structure                            |


    ## JSON Representation
    ```json
    {
    "name": "my collection JSON",
     "node":["Collection"],
     "uid":"_:fccd3549-07cb-4e23-ba79-323597ec9bfd",
     "uuid":"fccd3549-07cb-4e23-ba79-323597ec9bfd"

     "experiment":[
        {
           "name":"my experiment name",
           "node":["Experiment"],
           "uid":"_:8256b75b-1f4e-4f69-9fe6-3bcb2298e470",
           "uuid":"8256b75b-1f4e-4f69-9fe6-3bcb2298e470"
        }
     ],
     "inventory":[],
     "citation":[],
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        # TODO add proper typing in future, using Any for now to avoid circular import error
        member: List[Union[User, UIDProxy]] = field(default_factory=list)
        admin: List[Union[User, UIDProxy]] = field(default_factory=list)
        experiment: List[Union[Any, UIDProxy]] = field(default_factory=list)
        inventory: List[Union[Any, UIDProxy]] = field(default_factory=list)
        doi: str = ""
        citation: List[Union[Any, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self, name: str, experiment: Optional[List[Union[Any, UIDProxy]]] = None, inventory: Optional[List[Union[Any, UIDProxy]]] = None, doi: str = "", citation: Optional[List[Union[Any, UIDProxy]]] = None, notes: str = "", **kwargs
    ) -> None:
        """
        create a Collection with a name
        add list of experiment, inventory, citation, doi, and notes if available.

        Examples
        --------
        >>> import cript
        >>> my_collection = cript.Collection(name="my collection name")

        Parameters
        ----------
        name: str
            name of the Collection you want to make
        experiment: Optional[List[Experiment]], default=None
            list of experiment within the Collection
        inventory: Optional[List[Inventory]], default=None
            list of inventories within this collection
        doi: str = "", default=""
            cript doi
        citation: Optional[List[Citation]], default=None
            List of citations for this collection

        Returns
        -------
        None
            Instantiates a Collection node
        """
        super().__init__(name=name, notes=notes, **kwargs)

        if experiment is None:
            experiment = []

        if inventory is None:
            inventory = []

        if citation is None:
            citation = []

        new_json_attrs = replace(
            self._json_attrs,
            name=name,
            experiment=experiment,
            inventory=inventory,
            doi=doi,
            citation=citation,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def member(self) -> List[Union[User, UIDProxy]]:
        return self._json_attrs.member.copy()

    @property
    @beartype
    def admin(self) -> List[Union[User, UIDProxy]]:
        return self._json_attrs.admin

    @property
    @beartype
    def experiment(self) -> List[Any]:
        """
        List of all [experiment](../experiment) within this Collection

        Examples
        --------
        >>> import cript
        >>> my_collection = cript.Collection(name="my collection name")
        >>> my_experiment = cript.Experiment(name="my experiment name")
        >>> my_collection.experiment = [my_experiment]

        Returns
        -------
        List[Experiment]
            list of all [experiment](../experiment) within this Collection
        """
        return self._json_attrs.experiment.copy()  # type: ignore

    @experiment.setter
    @beartype
    def experiment(self, new_experiment: List[Any]) -> None:
        """
        sets the Experiment list within this collection

        Parameters
        ----------
        new_experiment: List[Experiment]
            list of experiment

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, experiment=new_experiment)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def inventory(self) -> List[Any]:
        """
        List of [inventory](../inventory) that belongs to this collection

        Examples
        --------
        >>> import cript
        >>> my_collection = cript.Collection(name="my collection name")
        >>> material_1 = cript.Material(
        ...     name="material 1",
        ...     bigsmiles = "material 1 bigsmiles",
        ... )
        >>> material_2 = cript.Material(
        ...     name="material 2",
        ...     bigsmiles = "material 2 bigsmiles",
        ... )
        >>> my_inventory = cript.Inventory(
        ...     name="my inventory name", material=[material_1, material_2]
        ... )
        >>> my_collection.inventory = [my_inventory]

        Returns
        -------
        inventory: List[Inventory]
            list of inventories in this collection
        """
        return self._json_attrs.inventory.copy()  # type: ignore

    @inventory.setter
    @beartype
    def inventory(self, new_inventory: List[Any]) -> None:
        """
        Sets the List of inventories within this collection to a new list

        Parameters
        ----------
        new_inventory: List[Inventory]
            new list of inventories for the collection to overwrite the current list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, inventory=new_inventory)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def doi(self) -> str:
        """
        The CRIPT DOI for this collection

        Examples
        --------
        >>> import cript
        >>> my_collection = cript.Collection(name="my collection name")
        >>> my_collection.doi = "10.1038/1781168a0"

        Returns
        -------
        doi: str
            the CRIPT DOI e.g. `10.1038/1781168a0`
        """
        return self._json_attrs.doi

    @doi.setter
    @beartype
    def doi(self, new_doi: str) -> None:
        """
        set the CRIPT DOI for this collection to new CRIPT DOI

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
    @beartype
    def citation(self) -> List[Any]:
        """
        List of Citations within this Collection

        Examples
        --------
        >>> import cript
        >>> my_collection = cript.Collection(name="my collection name")
        >>> my_reference = cript.Reference(
        ...     type="journal_article",
        ...     title="title",
        ...     author=["Ludwig Schneider", "Marcus Müller"],
        ...     journal="Computer Physics Communications",
        ...     publisher="Elsevier",
        ...     year=2019,
        ...     pages=[463, 476],
        ...     doi="10.1016/j.cpc.2018.08.011",
        ...     issn="0010-4655",
        ...     website="https://www.sciencedirect.com/science/article/pii/S0010465518303072",
        ... )
        >>> my_citation = cript.Citation(type="derived_from", reference=my_reference)
        >>> my_collection.citation = [my_citation]

        Returns
        -------
        citation: List[Citation]:
            list of Citations within this Collection
        """
        return self._json_attrs.citation.copy()  # type: ignore

    @citation.setter
    @beartype
    def citation(self, new_citation: List[Any]) -> None:
        """
        set the list of citations for this Collection

        Parameters
        ----------
        new_citation: List[Citation]
            set the list of citations for this Collection

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
