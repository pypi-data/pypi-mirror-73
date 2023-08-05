import logging

from django.db.models import CheckConstraint, UniqueConstraint, F, Q

from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import AuditManager, AuditModel, AuditQuerySet
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operations import Operations
from kaf_pas.production.models.resource import Resource

logger = logging.getLogger(__name__)


class Operation_resourcesQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        return super().create(**kwargs)


class Operation_resourcesManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Operation_resourcesQuerySet(self.model, using=self._db)


class Operation_resources(AuditModel):
    operation = ForeignKeyCascade(Operations, related_name='planing_operation_res')
    resource = ForeignKeyProtect(Resource, related_name='planing_resource_res')
    location_fin = ForeignKeyProtect(Locations, related_name='planing_location_fin_res', null=True, blank=True)

    objects = Operation_resourcesManager()

    def __str__(self):
        return f"ID:{self.id}, operation: [{self.operation}], resource: [{self.resource}]"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        constraints = [
            UniqueConstraint(fields=['operation', 'resource'], condition=Q(location_fin=None), name='Operation_resources_unique_constraint_01'),
            UniqueConstraint(fields=['location_fin', 'operation', 'resource'], name='Operation_resources_unique_constraint_11'),
        ]
