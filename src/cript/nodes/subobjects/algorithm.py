from dataclasses import dataclass, field, replace
from typing import List

from cript.nodes.core import BaseNode
from cript.nodes.subobjects.citation import Citation
from cript.nodes.subobjects.parameter import Parameter


class Algorithm(BaseNode):
    """ 
    ## Definition
    [algorithm node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=25)

    
    ## Attributes
      
    | Keys      | Type            | Example                                      | Description                                            | Required | Vocab |
    |-----------|-----------------|----------------------------------------------|--------------------------------------------------------|----------|-------|
    | key       | str             | ensemble, thermo-barostat                    | system configuration, algorithms used in a computation | True     | True  |
    | type      | str             | NPT for ensemble, Nose-Hoover for thermostat | specific type of configuration, algorithm              | True     |       |
    | parameter | list[Parameter] |                                              | setup associated parameters                            |          |       |
    | citation  | list[Citation]  |                                              | reference to a book, paper, or scholarly work          |          |       |
    

    ## Available Subobjects


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
        create algorithm subobject

        Parameters
        ----------
        key : str
            algorithm key must come from [CRIPT controlled vocabulary]()
        type : str
            algorithm type must come from [CRIPT controlled vocabulary]()
        parameter : List[Parameter], optional
            parameter subobject, by default None
        citation : List[Citation], optional
            citation subobject, by default None

        Examples
        --------
        ```python
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
        get or set algorithm key. Algorithm key must come from [CRIPT controlled vocabulary]()

        Examples
        --------
        ```python

        ```

        Returns
        -------
        str
            algorithm key
        """
        return self._json_attrs.key

    @key.setter
    def key(self, new_key: str):
        new_attrs = replace(self._json_attrs, key=new_key)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def type(self) -> str:
        """
        get or set algorithm type. Algorithm type must come from [CRIPT controlled vocabulary]()

        Returns
        -------
        str
            algorithm type
        """
        return self._json_attrs.type

    @type.setter
    def type(self, new_type: str):
        new_attrs = replace(self._json_attrs, type=new_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def parameter(self) -> List[Parameter]:
        """

        Examples
        --------
        ```python

        ```

        Returns
        -------
        List[Parameter]
            _description_
        """
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter: List[Parameter]):
        new_attrs = replace(self._json_attrs, parameter=new_parameter)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    def citation(self):
        """
        get or set citation subobject for algorithm node

        Examples
        --------
        ```python

        ```

        Returns
        -------
        _type_
            _description_
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    def citation(self, new_citation):
        new_attrs = replace(self._json_attrs, citation=new_citation)
        self._update_json_attrs_if_valid(new_attrs)
