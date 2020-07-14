from .enum_table import EnumTable
from .enum_type import EnumType

try:
    import alembic
except ModuleNotFoundError:
    pass  # Expected exception
else:
    from .alembic_ops import EnumInsertOp, EnumDeleteOp
    from .alembic_autogen import compare_enums
