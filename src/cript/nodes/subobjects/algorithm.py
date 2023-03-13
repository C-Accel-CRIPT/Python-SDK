from typing import List
from dataclasses import dataclass, replace, field
from cript.nodes.core import BaseNode
from cript.nodes.subobjects.parameter import Parameter
from cript.nodes.subobjects.citation import Citation

class Algorithm(BaseNode):
    """The <a href="../algorithm" target="_blank">`Algorithm`</a>
    object represents an algorithm that can be used as part of a
    <a href="/../nodes/computation" target="_blank">`Computation`</a> object. For example,
    the computation might consist of a clustering algorithm or sorting a algorithm.

    Args:
        key (str): Algorithm key
        type (str): Algorithm type
        parameters (list[Union[Parameter, dict]], optional): List of parameters linked to this algorithm
        citations (list[Union[Citation, dict]], optional): List of citations linked to this algorithm

    ``` py title="Example"
    algorithm = Algorithm(
        key="mc_barostat",
        type="barostat",
        parameters=[],
        citations=[],
    )
    ```
    """
    @dataclass(frozen=True)
    class JsonAttributes(BaseNode.JsonAttributes):
        node:str = "Algorithm"
        key: str = ""
        type: str = ""

        parameter: List[Parameter] = field(default_factory=list)
        citation: List[Citation] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()
    def __init__(self, key:str, type:str, parameter:List[Parameter]=None, citation:List[Citation]=None):
        if parameter is None: parameter = []
        if citation is None: citation = []
        super().__init__(node="Algorithm")
        self._json_attrs = replace(self._json_attrs, key=key, type=type, parameter=parameter)


    @property
    def key(self) -> str:
        return self._json_attrs.key
    @key.setter
    def key(self, new_key:str):
        self._json_attrs = replace(self._json_attrs, key=new_key)

    @property
    def type(self) -> str:
        return self._json_attrs.type
    @type.setter
    def type(self, new_type:str):
        self._json_attrs = replace(self._json_attrs, type=new_type)

    @property
    def parameter(self) -> List[Parameter]:
        return self._json_attrs.parameter.copy()

    @parameter.setter
    def parameter(self, new_parameter:List[Parameter]):
        self._json_attrs = replace(self._json_attrs, parameter=new_parameter)

    @property
    def citation(self):
        return self._json_attrs.citation.copy()
    @citation.setter
    def citation(self, new_citation):
        self._json_attrs = replace(self._json_attrs, citation=new_citation)
