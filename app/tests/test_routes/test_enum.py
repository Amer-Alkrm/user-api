from enums import Degree, IntEnum


def test_enum_methods() -> None:
    Degree_enum = IntEnum(Degree)
    Degree_DSC = Degree_enum.process_bind_param(2, None)
    Degree_Int = Degree_enum.process_result_value(Degree(2), None)
    assert Degree_DSC == 'Dsc'
    assert Degree_Int == 2
