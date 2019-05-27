
from alembic.operations import Operations, MigrateOperation
import alembic.autogenerate.render
from sqlalchemy import sql

__all__ = ["InsertOp", "DeleteOp"]

@Operations.register_operation("insert")
class InsertOp(MigrateOperation):

	def __init__(self, klass, data = []):
		self.klass = klass
		self.data = data

	@classmethod
	def insert(cls, operations, klass, data = []):
		op = cls(klass, data)
		return operations.invoke(op)

	def reverse(self):
		return DeleteOp(self.klass, self.data)

@Operations.register_operation("delete")
class DeleteOp(MigrateOperation):

	def __init__(self, klass, data = []):
		self.klass = klass
		self.data = data

	@classmethod
	def delete(cls, operations, klass, data = []):
		op = cls(klass, data)
		return operations.invoke(op)

	def reverse(self):
		return InsertOp(self.klass, self.data)

@Operations.implementation_for(InsertOp)
def insert(operations, operation):
	for item in operation.data:
		items = item.items()
		columns = ', '.join(i[0] for i in items)
		values = [i[1] for i in items]
		txt = sql.text('INSERT INTO {tn} ({cn}) VALUES ({vl});'.format(tn = operation.klass.__tablename__, cn = columns, vl = ', '.join(':' + i[0] for i in items)))
		operations.execute(txt.bindparams(**item))

@Operations.implementation_for(DeleteOp)
def delete(operations, operation):
	for item in operation.data:
		items = item.items()
		columns = ', '.join(i[0] for i in items)
		values = [i[1] for i in items]
		txt = sql.text('DELETE FROM {tn} WHERE 1=1 AND {fl};'.format(tn = operation.klass.__tablename__, fl = ' AND '.join(i[0] + ' = :' + i[0] for i in items) ))
		operations.execute(txt.bindparams(**item))

@alembic.autogenerate.render.renderers.dispatch_for(InsertOp)
def render_sync_enum_value_op(autogen_context, op):
	return 'op.insert({}, {!r})'.format(op.klass.__name__, op.data)

@alembic.autogenerate.render.renderers.dispatch_for(DeleteOp)
def render_sync_enum_value_op(autogen_context, op):
	return 'op.delete({}, {!r})'.format(op.klass.__name__, op.data)