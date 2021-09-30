from enum import IntEnum

from sqlalchemy.types import Enum, TypeDecorator


class Degree(IntEnum):
    Bsc = 1
    Dsc = 2
    Msc = 3


class Gender(IntEnum):
    Male = 1
    Female = 2


class State(IntEnum):
    Amman = 1
    Zarqa = 2
    Irbid = 3
    Ajloun = 4
    Jerash = 5
    Mafraq = 6
    Balqa = 7
    Madaba = 8
    Karak = 9
    Tafila = 10
    Maan = 11
    Aqaba = 12


def all_enum_to_str(cls):
    return ', '.join([f'{e.name}: {e.value}' for e in cls])


class IntEnum(TypeDecorator):

    def __init__(self, enum) -> None:
        self.__enum = enum
        self.impl = Enum(
            enum,
            name=enum.__name__)

    def process_bind_param(self, value: int, dialect) -> IntEnum:
        return self.__enum(value).name if value is not None else value

    def process_result_value(self, value: IntEnum, dialect) -> int:
        return value.value if value is not None else value
