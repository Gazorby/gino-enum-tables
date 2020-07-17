import sqlalchemy.types as types


__all__ = ["EnumType"]


class EnumType(types.TypeDecorator):
    impl = types.String

    def __init__(self, enum_table=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__enum__ = enum_table

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.name

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.__enum__.__enum__[value]
