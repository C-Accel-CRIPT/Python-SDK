import pytest

import cript


def test_create_simple_computational_process() -> None:
    """
    create a simple computational_process node with required arguments
    """
    my_computational_process_type = "cross_linking"

    # input data
    my_data_files = cript.File(
        source="https://criptapp.org", type="calibration", extension=".csv",
        data_dictionary="my file's data dictionary"
    )

    input_data = cript.Data(type="afm_amp", files=[my_data_files])

    # ingredients with Material and Quantity node
    my_material = cript.Material(name="my material",
                                 identifiers=[{"alternative_names": "my material alternative name"}])

    my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")

    ingredients = cript.Ingredient(
        material=my_material,
        quantities=[my_quantity],
    )

    my_computational_process = cript.ComputationalProcess(
        type=my_computational_process_type, input_data=[input_data], ingredients=[ingredients]
    )

    # assertions
    assert isinstance(my_computational_process, cript.ComputationalProcess)
    assert my_computational_process.type == my_computational_process_type
    assert my_computational_process.input_data == [input_data]
    assert my_computational_process.ingredients == [ingredients]


def test_create_complex_computational_process() -> None:
    """
    create a complex computational process with all possible arguments
    """

    # # all computational_process attributes
    #
    # my_computational_process_type = "cross_linking"
    #
    # # input data
    # input_data_files = cript.File(
    #     source="https://criptapp.org", type="calibration", extension=".csv",
    #     data_dictionary="my file's data dictionary"
    # )
    #
    # input_data = cript.Data(type="afm_amp", files=[input_data_files])
    #
    # # output data
    # output_data_files = cript.File(
    #     source="https://criptscripts.org", type="calibration", extension=".csv",
    #     data_dictionary="my file's data dictionary"
    # )
    #
    # output_data = cript.Data(type="afm_amp", files=[output_data_files])
    #
    # # ingredients with Material and Quantity node
    # my_material = cript.Material(name="my material",
    #                              identifiers=[{"alternative_names": "my material alternative name"}])
    #
    # my_quantity = cript.Quantity(key="mass", value=1.23, unit="gram")
    #
    # ingredients = cript.Ingredient(
    #     material=my_material,
    #     quantities=[my_quantity],
    # )
    #
    # # software_configuration
    # # TODO left off at software
    # software_config = cript.SoftwareConfiguration(software=)
    pass
