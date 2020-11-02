from enum import Enum


class StringEnum(str, Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
