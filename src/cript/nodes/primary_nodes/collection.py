from dataclasses import dataclass, replace
from typing import Any, List

# from cript import Inventory, Experiment, Citation
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Collection(PrimaryBaseNode):
    """
    ## Definition

    A
    [Collection node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=8)
    is nested inside a [Project](../project) node.

    A Collection node can be thought as a folder/bucket that can hold [experiment](../experiment)
    or [Inventories](../inventory) node.

    | attribute   | type             | example             | description                                                                    |
    |-------------|------------------|---------------------|--------------------------------------------------------------------------------|
    | experiment | list[Experiment] |                     | experiment that relate to the collection                                      |
    | inventory | list[Inventory]  |                     | inventory owned by the collection                                              |
    | doi       | str              | `10.1038/1781168a0` | DOI: digital object identifier for a published collection; CRIPT generated DOI |
    | citation   | list[Citation]   |                     | reference to a book, paper, or scholarly work                                  |


    <!-- TODO consider adding JSON of a collection -->
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        # TODO add proper typing in future, using Any for now to avoid circular import error
        experiment: List[Any] = None
        inventory: List[Any] = None
        doi: str = ""
        citation: List[Any] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, name: str, experiment: List[Any] = None, inventory: List[Any] = None, doi: str = "", citation: List[Any] = None, notes: str = "", **kwargs) -> None:
        """
        create a Collection with a name
        add list of experiment, inventory, citation, doi, and notes if available.

        Parameters
        ----------
        name: str
            name of the Collection you want to make
        experiment: List[Experiment], default=None
            list of experiment within the Collection
        inventory: List[Inventory], default=None
            list of inventories within this collection
        doi: str = "", default=""
            cript doi
        citation: List[Citation], default=None
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

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            experiment=experiment,
            inventory=inventory,
            doi=doi,
            citation=citation,
        )

        self.validate()

    # ------------------ Properties ------------------

    @property
    def experiment(self) -> List[Any]:
        """
        List of all [experiment](../experiment) within this Collection

        Examples
        --------
        ```python
        my_collection.experiment = [my_first_experiment]
        ```

        Returns
        -------
        List[Experiment]
            list of all [experiment](../experiment) within this Collection
        """
        return self._json_attrs.experiment.copy()

    @experiment.setter
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
    def inventory(self) -> List[Any]:
        """
        List of [inventory](../inventory) that belongs to this collection

        Examples
        --------
        ```python
        material_1 = cript.Material(
            name="material 1",
            identifiers=[{"alternative_names": "material 1 alternative name"}],
        )

        material_2 = cript.Material(
            name="material 2",
            identifiers=[{"alternative_names": "material 2 alternative name"}],
        )

        my_inventory = cript.Inventory(
            name="my inventory name", materials_list=[material_1, material_2]
        )

        my_collection.inventory = [my_inventory]
        ```

        Returns
        -------
        inventory: List[Inventory]
            list of inventories in this collection
        """
        return self._json_attrs.inventory.copy()

    @inventory.setter
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
    def doi(self) -> str:
        """
        The CRIPT DOI for this collection

        ```python
        my_collection.doi = "10.1038/1781168a0"
        ```

        Returns
        -------
        doi: str
            the CRIPT DOI e.g. `10.1038/1781168a0`
        """
        return self._json_attrs.doi

    @doi.setter
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
    def citation(self) -> List[Any]:
        """
        List of Citations within this Collection

        Examples
        --------
        ```python
        my_citation = cript.Citation(type="derived_from", reference=simple_reference_node)

        my_collections.citation = my_citations
        ```

        Returns
        -------
        citation: List[Citation]:
            list of Citations within this Collection
        """
        return self._json_attrs.citation.copy()

    @citation.setter
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
