from dataclasses import dataclass, field, replace
from typing import Any, List, Optional, Union

from beartype import beartype

from cript.nodes.primary_nodes.primary_base_node import PrimaryBaseNode
from cript.nodes.util.json import UIDProxy


class Data(PrimaryBaseNode):
    """
    ## Definition
    A [Data node](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf#page=13)
     node contains the meta-data to describe raw data that is beyond a single value, (i.e. n-dimensional data).
     Each `Data` node must be linked to a single `Experiment` node.

    ## Available Sub-Objects
    * [Citation](../../subobjects/citation)

    ## Attributes
    | Attribute           | Type                                              | Example                    | Description                                                                                  | Required |
    |---------------------|---------------------------------------------------|----------------------------|----------------------------------------------------------------------------------------------|----------|
    | name                | str                                               | `"my_data_name"`           | Name of the data node                                                                        | True     |
    | type                | str                                               | `"nmr_h1"`                 | Pick from [CRIPT data type controlled vocabulary](https://app.criptapp.org/vocab/data_type/) | True     |
    | file                | List[[File](../supporting_nodes/file.md)]         | `[file_1, file_2, file_3]` | list of file nodes                                                                           | False    |
    | sample_preparation  | [Process](process.md)                             |                            |                                                                                              | False    |
    | computation         | List[[Computation](computation.md)]               |                            | data produced from this Computation method                                                   | False    |
    | computation_process | [Computational Process](./computation_process.md) |                            | data was produced from this computation process                                              | False    |
    | material            | List[[Material](./material.md)]                   |                            | materials with attributes associated with the data node                                      | False    |
    | process             | List[[Process](./process.md)]                     |                            | processes with attributes associated with the data node                                      | False    |
    | citation            | [Citation](../subobjects/citation.md)             |                            | reference to a book, paper, or scholarly work                                                | False    |
    | notes               | str                                               | "my awesome notes"         | miscellaneous information, or custom data structure                                          | False    |

    Examples
    --------
    >>> import cript
    >>> my_file = cript.File(
    ...    name="my file node name",
    ...    source="https://criptapp.org",
    ...    type="calibration",
    ...    extension=".csv",
    ...    data_dictionary="my file's data dictionary"
    ... )
    >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])

    ## JSON Representation
    ```json
    {
       "name":"my data name",
       "node":["Data"],
       "type":"afm_amp",
       "uid":"_:80b02470-73d0-416e-8d93-12fdf69e481a",
       "uuid":"80b02470-73d0-416e-8d93-12fdf69e481a"
       "file":[
          {
            "node":["File"],
            "name":"my file node name",
             "uid":"_:535779ea-0d1f-4b23-b3e8-60052f717307",
             "uuid":"535779ea-0d1f-4b23-b3e8-60052f717307"
             "type":"calibration",
             "source":"https://criptapp.org",
             "extension":".csv",
             "data_dictionary":"my file's data dictionary",
          }
       ]
    }
    ```
    """

    @dataclass(frozen=True)
    class JsonAttributes(PrimaryBaseNode.JsonAttributes):
        """
        all Data attributes
        """

        type: str = ""
        # TODO add proper typing in future, using Any for now to avoid circular import error
        file: List[Union[Any, UIDProxy]] = field(default_factory=list)
        sample_preparation: Union[Any, UIDProxy] = field(default_factory=list)
        computation: List[Union[Any, UIDProxy]] = field(default_factory=list)
        computation_process: Union[Any, UIDProxy] = field(default_factory=list)
        material: List[Union[Any, UIDProxy]] = field(default_factory=list)
        process: List[Union[Any, UIDProxy]] = field(default_factory=list)
        citation: List[Union[Any, UIDProxy]] = field(default_factory=list)

    _json_attrs: JsonAttributes = JsonAttributes()

    @beartype
    def __init__(
        self,
        name: str,
        type: str,
        file: List[Union[Any, UIDProxy]],
        sample_preparation: Union[Any, UIDProxy] = None,
        computation: Optional[List[Union[Any, UIDProxy]]] = None,
        computation_process: Optional[Union[Any, UIDProxy]] = None,
        material: Optional[List[Union[Any, UIDProxy]]] = None,
        process: Optional[List[Union[Any, UIDProxy]]] = None,
        citation: Optional[List[Union[Any, UIDProxy]]] = None,
        notes: str = "",
        **kwargs
    ) -> None:
        """
        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf",
        ...      type="calibration",
        ...      extension=".pdf",
        ... )
        >>> my_data = cript.Data(
        ...     name="my data node name",
        ...     type="afm_amp",
        ...     file=[my_file],
        ... )

        Parameters
        ----------
        name: str
            data node name
        type: str
            [data type](https://app.criptapp.org/vocab/data_type) must come from CRIPT controlled vocabulary
        file: List[File], default None
            list of CRIPT file nodes within the data node
        sample_preparation: Process, default None
            sample preparation
        computation: Optional[Computation], default None
            data was produced from this computation method
        computation_process: Optional[ComputationalProcess], default None
            data was produced from this computation process
        material: Optional[List[Material]], default None
            materials with attributes associated with the data node
        process: Optional[List[Process]], default None
            processes with attributes associated with the data node
        citation: Optional[List[Citation]], default None
            reference to a book, paper, or scholarly work
        notes: str, default ""
            miscellaneous information, or custom data structure
        kwargs
            used for deserializing JSON into Python SDK nodes

        Returns
        -------
        None
        """
        super().__init__(name=name, notes=notes, **kwargs)

        if file is None:
            file = []

        if sample_preparation is None:
            sample_preparation = []

        if computation is None:
            computation = []

        if computation_process is None:
            computation_process = []

        if material is None:
            material = []

        if process is None:
            process = []

        if citation is None:
            citation = []

        new_json_attrs = replace(
            self._json_attrs,
            type=type,
            file=file,
            sample_preparation=sample_preparation,
            computation=computation,
            computation_process=computation_process,
            material=material,
            process=process,
            citation=citation,
        )
        self._update_json_attrs_if_valid(new_json_attrs)

    @property
    @beartype
    def type(self) -> str:
        """
        The data type must come from [CRIPT data type vocabulary](https://app.criptapp.org/vocab/data_type)

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_data.type = "nmr_h1"

        Returns
        -------
        data type: str
            data type for the data node must come from CRIPT controlled vocabulary
        """
        return self._json_attrs.type

    @type.setter
    @beartype
    def type(self, new_data_type: str) -> None:
        """
        set the data type.
        The data type must come from [CRIPT data type vocabulary](https://app.criptapp.org/vocab/data_type)

        Parameters
        ----------
        new_data_type: str
            new data type to replace the current data type

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, type=new_data_type)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def file(self) -> List[Any]:
        """
        get the list of [files](../../supporting_nodes/file) for this data node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_new_file = cript.File(
        ...    name="my new file node name",
        ...    source="path/to/local/file",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data.file += [my_new_file]

        Returns
        -------
        List[File]
            list of files for this data node
        """
        return self._json_attrs.file.copy()

    @file.setter
    @beartype
    def file(self, new_file_list: List[Any]) -> None:
        """
        set the list of file for this data node

        Parameters
        ----------
        new_files_list: List[File]
            new list of file nodes to replace the current list

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, file=new_file_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def sample_preparation(self) -> Union[Any, None]:
        """
        The [sample preparation](../process) for this data node

        Examples
        --------
        >>> import cript
        >>> my_new_files = cript.File(
        ...     name="my file node name",
        ...     source="https://pubs.acs.org/doi/10.1021/acscentsci.3c00011",
        ...     type="computation_config",
        ...     extension=".pdf",
        ...     data_dictionary="my data dictionary",
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_new_files])
        >>> my_sample_preparation = cript.Process(name="my sample preparation name", type="affinity_pure")
        >>> my_data.sample_preparation = my_sample_preparation

        Returns
        -------
        sample_preparation: Process
            sample preparation for this data node
        """
        return self._json_attrs.sample_preparation

    @sample_preparation.setter
    @beartype
    def sample_preparation(self, new_sample_preparation: Union[Any, None]) -> None:
        """
        set sample_preparation

        Parameters
        ----------
        new_sample_preparation: Process
            new_sample_preparation to replace the current one for this node

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, sample_preparation=new_sample_preparation)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def computation(self) -> List[Any]:
        """
        list of [computation nodes](../computation/) for this material node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_computation = cript.Computation(name="my computation name", type="analysis")
        >>> my_data.computation = [my_computation]

        Returns
        -------
        None
            list of computation nodes
        """
        return self._json_attrs.computation.copy()

    @computation.setter
    @beartype
    def computation(self, new_computation_list: List[Any]) -> None:
        """
        set list of computation  for this data node

        Parameters
        ----------
        new_computation_list: List[Computation]
            new computation list to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation=new_computation_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def computation_process(self) -> Union[Any, None]:
        """
        The [computation_process](../computation_process) for this data node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...     name="my file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(
        ...     name="my data name",
        ...     type="afm_amp",
        ...     file=[my_file]
        ... )
        >>> my_file_for_second_data_node = cript.File(
        ...     name="my second file node name",
        ...     source="https://criptapp.org",
        ...     type="calibration",
        ...     extension=".csv",
        ...     data_dictionary="my file's data dictionary"
        ... )
        >>> my_second_data_node = cript.Data(
        ...     name="my data name",
        ...     type="afm_amp",
        ...     file=[my_file_for_second_data_node]
        ... )
        >>> my_material = cript.Material(
        ...     name="my material name",
        ...     bigsmiles = "123456"
        ... )
        >>> my_quantity = cript.Quantity(
        ...     key="mass", value=11.2, unit="kg", uncertainty=0.2, uncertainty_type="stdev"
        ... )
        >>> my_ingredient = cript.Ingredient(
        ...     material=my_material,
        ...     quantity=[my_quantity],
        ...     keyword=["catalyst"],
        ... )
        >>> my_computational_process = cript.ComputationProcess(
        ...     name="my computational process node name",
        ...     type="cross_linking",
        ...     input_data=[my_second_data_node],
        ...     ingredient=[my_ingredient],
        ... )

        Returns
        -------
        ComputationalProcess
            computational process node for this data node
        """
        return self._json_attrs.computation_process

    @computation_process.setter
    @beartype
    def computation_process(self, new_computation_process: Union[Any, None]) -> None:
        """
        set the computational process

        Parameters
        ----------
        new_computation_process: ComputationalProcess

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, computation_process=new_computation_process)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def material(self) -> List[Any]:
        """
        List of [materials](../material) for this node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_material = cript.Material(name="my material name", bigsmiles = "123456")
        >>> my_data.material = [my_material]

        Returns
        -------
        List[Material]
            list of material
        """
        return self._json_attrs.material.copy()

    @material.setter
    @beartype
    def material(self, new_material_list: List[Any]) -> None:
        """
        set the list of materials for this data node

        Parameters
        ----------
        new_material_list: List[Material]

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, material=new_material_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def process(self) -> List[Any]:
        """
        list of [Process nodes](./process.md) for this data node

        Examples
        --------
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_process = cript.Process(name="my process name", type="affinity_pure")
        >>> my_data.process = [my_process]

        Notes
        -----
        Please note that while the process attribute of the data node is currently set to `Any`
        the software still expects a Process node in the data's process attribute
        > It is currently set to `Any` to avoid the circular import error

        Returns
        -------
        List[Process]
            list of process for the data node
        """
        return self._json_attrs.process.copy()

    @process.setter
    @beartype
    def process(self, new_process_list: List[Any]) -> None:
        """
        set the list of process for this data node

        Parameters
        ----------
        new_process_list: List[Process]
            new list of Process

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, process=new_process_list)
        self._update_json_attrs_if_valid(new_attrs)

    @property
    @beartype
    def citation(self) -> List[Any]:
        """
        List of [citation](../../subobjects/citation) within the data node

        Examples
        --------
        >>> import cript
        >>> import cript
        >>> my_file = cript.File(
        ...    name="my file node name",
        ...    source="https://criptapp.org",
        ...    type="calibration",
        ...    extension=".csv",
        ...    data_dictionary="my file's data dictionary"
        ... )
        >>> my_data = cript.Data(name="my data name", type="afm_amp", file=[my_file])
        >>> my_reference = cript.Reference(type="journal_article", title="'Living' Polymers")
        >>> my_citation = cript.Citation(type="derived_from", reference=my_reference)
        >>> my_data.citation = [my_citation]

        Returns
        -------
        List[Citation]
            list of citations for this data node
        """
        return self._json_attrs.citation.copy()

    @citation.setter
    @beartype
    def citation(self, new_citation_list: List[Any]) -> None:
        """
        set the list of citation

        Parameters
        ----------
        new_citation_list: List[Citation]
            new list of citation to replace the current one

        Returns
        -------
        None
        """
        new_attrs = replace(self._json_attrs, citation=new_citation_list)
        self._update_json_attrs_if_valid(new_attrs)
