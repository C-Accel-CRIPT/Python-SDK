from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.parameter import Parameter


class Algorithm(BaseNode):
    """
    ## Definition

    An [algorithm sub-object](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=25)
    is a set of instructions that define a computational process.
    An algorithm consists of parameters that are used in the computation and the computational process itself.


    ## Attributes

    | Keys      | Type            | Example                                      | Description                                            | Required | Vocab |
    |-----------|-----------------|----------------------------------------------|--------------------------------------------------------|----------|-------|
    | key       | str             | ensemble, thermo-barostat                    | system configuration, algorithms used in a computation | True     | True  |
    | type      | str             | NPT for ensemble, Nose-Hoover for thermostat | specific type of configuration, algorithm              | True     |       |
    | parameter | list[Parameter] |                                              | setup associated parameters                            |          |       |
    | citation  | Citation        |                                              | reference to a book, paper, or scholarly work          |          |       |


    ## Available sub-objects
    * [Parameter](../parameter)
    * [Citation](../citation)

    ## JSON Representation
    ```json
    {
        "node": ["Algorithm"],
        "key": "mc_barostat",
        "type": "barostat",
        "parameter": {
            "node": ["Parameter"],
            "key": "update_frequency",
            "value": 1000.0,
            "unit": "1/second"
        },
        "citation": {
            "node": ["Citation"],
            "type": "reference"
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
        },
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        key: str = ""
        type: str = ""

        parameter: List[Parameter] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, type: str, parameter: List[Parameter] = None, citation: List[Citation] = None, **kwargs):  # ignored
        """
        create algorithm sub-object

        Parameters
        ----------
        key : str
            algorithm key must come from [CRIPT controlled vocabulary]()
        type : str
            algorithm type must come from [CRIPT controlled vocabulary]()
        parameter : List[Parameter], optional
            parameter sub-object, by default None
        citation : List[Citation], optional
            citation sub-object, by default None

        Examples
        --------
        ```python
        # create algorithm sub-object
        algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        ```

        Returns
        -------
        None
            instantiate an algorithm node
        """
        if parameter is None:
            parameter = []
        if citation is None:
            citation = []
        super().__init__(**kwargs)
        self._json_attrs = replace(self._json_attrs, key=key, type=type, parameter=parameter)
        self.validate()

    @property
    def key(self) -> str:
        """
        Algorithm key

        > Algorithm key must come from [CRIPT controlled vocabulary]()

        Examples
        --------
        ```python
        algorithm.key = "amorphous_cell_module"
        ```

        Returns
        -------
        str
            algorithm key
        """
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str) -> None:
        """
        set the algorithm key

        > Algorithm key must come from [CRIPT Controlled Vocabulary]()

        Parameters
        ----------
        new_key : str
            algorithm key
        """
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def type(self) -> str:
        """
        Algorithm type

        > Algorithm type must come from [CRIPT controlled vocabulary]()

        Returns
        -------
        str
            algorithm type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str) -> None:
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def parameter(self) -> List[Parameter]:
        """
        list of [Parameter](../parameter) sub-objects for the algorithm sub-object

        Examples
        --------
        ```python
        # create parameter sub-object
        my_parameter = [
            cript.Parameter("update_frequency", 1000.0, "1/second")
            cript.Parameter("damping_time", 1.0, "second")
        ]

        # add parameter sub-object to algorithm sub-object
        algorithm.parameter = my_parameter
        ```

        Returns
        -------
        List[Parameter]
            list of parameters for the algorithm sub-object
        """
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter: List[Parameter]) -> None:
        """
        set a list of cript.Parameter sub-objects

        Parameters
        ----------
        new_parameter : List[Parameter]
            list of Parameter sub-objects for the algorithm sub-object

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, parameter=new_parameter)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self) -> Citation:
        """
        [citation](../citation) subobject for algorithm subobject

        Examples
        --------
        ```python
        title = "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        title += "SOft coarse grained Monte-Carlo Acceleration (SOMA)"

        # create reference node
        my_reference = cript.Reference(
            type="journal_article",
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

        # create citation sub-object and add reference to it
        my_citation = cript.Citation(type="reference, reference==my_reference)

        # add citation to algorithm node
        algorithm.citation = my_citation
        ```

        Returns
        -------
        citation node: Citation
            get the algorithm citation node
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation: Citation) -> None:
        """
        set the algorithm citation subobject

        Parameters
        ----------
        new_citation : Citation
            new citation subobject to replace the current

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
