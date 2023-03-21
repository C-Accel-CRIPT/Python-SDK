from dataclasses import dataclass, replace
from typing import List

from cript import Inventory, Experiment, Citation
from cript.nodes.core import BaseNode
from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode


class Collection(PrimaryBaseNode):
    """
    Collection class
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        """
        all Collection attributes
        """

        node: str = "Collection"
        name: str = ""
        experiments: List[Experiment] = None
        inventories: List[Inventory] = None
        cript_doi: str = ""
        citations: List[Citation] = None

    def __init__(
        self,
        name: str,
        experiments: List[Experiment] = None,
        inventories: List[Inventory] = None,
        crip_doi: str = "",
        citations: List[Citation] = None,
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

        crip_doi: str = "", default=""
            cript doi

        citations: List[Citation], default=None
            List of citations for this collection

        Returns
        -------
        None
        """
        super().__init__(node="Collection")

        self._json_attrs = replace(
            self._json_attrs,
            name=name,
            experiments=experiments,
            inventories=inventories,
            crip_doi=crip_doi,
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
    def name(self) -> str:
        """
        get the name of the collection

        Returns
        -------
        str
            collection name
        """
        return self._json_attrs.name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        sets the collection name to new name

        Parameters
        ----------
        new_name: str
            new name for the collection

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, name=new_name)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def experiments(self) -> List[Experiment]:
        """
        get a list of all Experiments in this Collection

        Returns
        -------
        List[Experiment]
            list of all Experiments within this Collection
        """
        return self._json_attrs.experiments

    @experiments.setter
    def experiments(self, new_experiment: List[Experiment]) -> None:
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
        new_attrs = replace(self._json_attrs, experiment=new_experiment)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def inventories(self) -> List[Inventory]:
        """
        gets a list of the inventories within this Collection

        Returns
        -------
        List[Inventory]
            list of inventories in this collection
        """
        return self._json_attrs.inventories

    @inventories.setter
    def inventories(self, new_inventory: List[Inventory]) -> None:
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
        gets the CRIPT DOI

        Returns
        -------
        cript_doi: str
            the CRIPT DOI
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
    def citations(self) -> List[Citation]:
        """
        List of Citations within this Collection

        Returns
        -------
        List[Citation]:
            list of Citations within this Collection
        """
        return self._json_attrs.citations

    @citations.setter
    def citations(self, new_citations: List[Citation]) -> None:
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
        new_attrs = replace(self._json_attrs, ciations=new_citations)
        self._update_json_attrs_if_valid(new_attrs)
