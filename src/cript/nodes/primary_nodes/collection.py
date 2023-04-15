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
    A Collection node can be thought as a folder/bucket that can hold either an Experiment or Inventory node.

    | attribute   | type             | example             | description                                                                    |
    |-------------|------------------|---------------------|--------------------------------------------------------------------------------|
    | experiments | list[Experiment] |                     | experiments that relate to the collection                                      |
    | inventories | list[Inventory]  |                     | inventory owned by the collection                                              |
    | cript_doi   | str              | `10.1038/1781168a0` | DOI: digital object identifier for a published collection; CRIPT generated DOI |
    | citations   | list[Citation]   |                     | reference to a book, paper, or scholarly work                                  |


    <!-- TODO consider adding JSON of a collection -->
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        # TODO add proper typing in future, using Any for now to avoid circular import error
        experiments: List[Any] = None
        inventories: List[Any] = None
        cript_doi: str = ""
        citations: List[Any] = None

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(
        self,
        name: str,
        experiments: List[Any] = None,
        inventories: List[Any] = None,
        cript_doi: str = "",
        citations: List[Any] = None,
        notes: str = "",
        **kwargs
    ) -> None:
        """
        create a collection with a name
        add list of experiments, inventories, citations, and cript_doi if available

        update the _json_attributes
        call validate to be sure the node is still valid

        Parameters
        ----------
        name: str
            name of the Collection you want to make

        experiments: List[Experiment], default=None
            list of experiments within the Collection

        inventories: List[Inventory], default=None
            list of inventories within this collection

        cript_doi: str = "", default=""
            cript doi

        citations: List[Citation], default=None
            List of citations for this collection

        Returns
        -------
        None
        """
        super().__init__(node="Collection", name=name, notes=notes)

        if experiments is None:
            experiments = []

        if inventories is None:
            inventories = []

        if citations is None:
            citations = []

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            experiments=experiments,
            inventories=inventories,
            cript_doi=cript_doi,
            citations=citations,
        )

        self.validate()

    def validate(self) -> None:
        """
        validates project node

        Returns
        -------
        None

        Raises
        ------
        CRIPTNodeSchemaError
        """
        pass

    # ------------------ Properties ------------------

    @property
    def experiments(self) -> List[Any]:
        """
        get a list of all Experiments in this Collection

        Returns
        -------
        List[Experiment]
            list of all Experiments within this Collection
        """
        return self._json_attrs.experiments.copy()

    @experiments.setter
    def experiments(self, new_experiment: List[Any]) -> None:
        """
        sets the Experiment list within this collection

        Parameters
        ----------
        new_experiment: List[Experiment]
            list of Experiments

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, experiments=new_experiment)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def inventories(self) -> List[Any]:
        """
        List of [inventories](../inventory) that belongs to this collection

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

        my_collection.inventories = [my_inventory]
        ```

        Returns
        -------
        List[Inventory]
            list of inventories in this collection
        """
        return self._json_attrs.inventories.copy()

    @inventories.setter
    def inventories(self, new_inventory: List[Any]) -> None:
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
        new_attrs = replace(self._json_attrs, inventories=new_inventory)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def cript_doi(self) -> str:
        """
        The CRIPT DOI for this collection

        ```python
        my_collection.cript_doi = "10.1038/1781168a0"
        ```

        Returns
        -------
        cript_doi: str
            the CRIPT DOI e.g. `10.1038/1781168a0`
        """
        return self._json_attrs.cript_doi

    @cript_doi.setter
    def cript_doi(self, new_cript_doi: str) -> None:
        """
        set the CRIPT DOI for this collection to new CRIPT DOI

        Parameters
        ----------
        new_cript_doi: str

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, cript_doi=new_cript_doi)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citations(self) -> List[Any]:
        """
        List of Citations within this Collection

        Examples
        --------
        ```python
        my_citation = cript.Citation(type="derived_from", reference=simple_reference_node)

        my_collections.citations = my_citations
        ```

        Returns
        -------
        List[Citation]:
            list of Citations within this Collection
        """
        return self._json_attrs.citations.copy()

    @citations.setter
    def citations(self, new_citations: List[Any]) -> None:
        """
        set the list of citations for this Collection

        Parameters
        ----------
        new_citations: List[Citation]
            set the list of citations for this Collection

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citations=new_citations)
        self._update_json_attrs_if_valid(new_attrs)
