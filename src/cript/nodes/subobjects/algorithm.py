from dataclasses import dataclass, field, replace
from typing import List, Optional, Union

from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.parameter import Parameter
from cript.nodes.util.json import UIDProxy
from cript.nodes.uuid_base import UUIDBaseNode


class Algorithm(UUIDBaseNode):
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

    ## Can be Added To
    * [SoftwareConfiguration](../software_configuration)

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
    class JsonAttributes(UUIDBaseNode.JsonAttributes):
        key: str = ""
        type: str = ""

        parameter: List[Union[Parameter, UIDProxy]] = field(default_factory=list)
        citation: List[Union[Citation, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    def __init__(self, key: str, type: str, parameter: Optional[List[Union[Parameter, UIDProxy]]] = None, citation: Optional[List[Union[Citation, UIDProxy]]] = None, **kwargs):  # ignored
        """
        Create algorithm sub-object

        Parameters
        ----------
        key : str
            algorithm key must come from
            [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/algorithm_key)
        type : str
            algorithm type must come from
            [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/algorithm_type)
        parameter : List[Parameter], optional
            parameter sub-object, by default None
        citation : List[Citation], optional
            citation sub-object, by default None

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")

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
        new_json_attrs = replace(self._json_attrs, key=key, type=type, parameter=parameter)
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    def key(self) -> str:
        """
        Algorithm key

        Algorithm key must come from [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/algorithm_key)

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        >>> my_algorithm.key = "amorphous_cell_module"

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

        > Algorithm key must come from
        [CRIPT Controlled Vocabulary](https://app.criptapp.org/vocab/algorithm_key)

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

        > Algorithm type must come from
        [CRIPT controlled vocabulary](https://app.criptapp.org/vocab/algorithm_type)

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        >>> my_algorithm.type = "integration"

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
    def parameter(self) -> List[Union[Parameter, UIDProxy]]:
        """
        list of [Parameter](../parameter) sub-objects for the algorithm sub-object

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        >>> my_parameters = [
        ...     cript.Parameter("update_frequency", 1000.0, "1/second"),
        ...     cript.Parameter("damping_time", 1.0, "second"),
        ... ]
        >>> my_algorithm.parameter = my_parameters

        Returns
        -------
        List[Parameter]
            list of parameters for the algorithm sub-object
        """
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter: List[Union[Parameter, UIDProxy]]) -> None:
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
    def citation(self) -> List[Union[Citation, UIDProxy]]:
        """
        [citation](../citation) subobject for algorithm subobject

        Examples
        --------
        >>> import cript
        >>> my_algorithm = cript.Algorithm(key="mc_barostat", type="barostat")
        >>> title = (
        ...     "Multi-architecture Monte-Carlo (MC) simulation of soft coarse-grained polymeric materials: "
        ...     "Soft coarse grained Monte-Carlo Acceleration (SOMA)"
        ... )
        >>> my_reference = cript.Reference(
        ...     type="journal_article",
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
        >>> my_algorithm.citation = [my_citation]


        Returns
        -------
        citation node: Citation
            get the algorithm citation node
        """
        return self._json_attrs.citation.copy()  # type: ignore

    @citation.setter
    def citation(self, new_citation: List[Union[Citation, UIDProxy]]) -> None:
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
