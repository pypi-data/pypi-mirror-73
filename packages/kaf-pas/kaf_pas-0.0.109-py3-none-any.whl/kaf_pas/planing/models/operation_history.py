import logging

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import AuditManager, AuditModel, AuditQuerySet
from kaf_pas.planing.models.operations import Operations
from kaf_pas.planing.models.status_operation_types import Status_operation_types

logger = logging.getLogger(__name__)


class Operation_historyQuerySet(AuditQuerySet):
    pass

class Operation_historyManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operation_historyQuerySet(self.model, using=self._db)


class Operation_history(AuditModel):
    creator = ForeignKeyProtect(User)
    operation = ForeignKeyCascade(Operations)
    status = ForeignKeyProtect(Status_operation_types)

    objects = Operation_historyManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'История операций'
