
from alembic.operations import Operations, MigrateOperation
from sqlalchemy.orm.session import Session

@Operations.register_operation("insert")
class InsertOp(MigrateOperation):

    def __init__(self, klass, data = []):
        self.klass = klass
        self.data = data

    @classmethod
    def insert(cls, operations, klass, data = []):
        op = InsertOp(sequence_name, **kw)
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
        op = DeleteOp(sequence_name, **kw)
        return operations.invoke(op)

    def reverse(self):
        return InsertOp(self.klass, self.data)

@Operations.implementation_for(InsertOp)
def insert(operations, operation):
	sess = Session(bind=operations.get_bind())
    sess.add_all(operation.klass(**item) for item in operation.data)


@Operations.implementation_for(DeleteOp)
def delete(operations, operation):
	sess = Session(bind=operations.get_bind())
	for item in operation.data:
		sess.query(operation.klass).filter_by(**item).delete()
