import logging

from bitfield import BitField

from isc_common.bit import IsBitOn
from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRefHierarcy
from isc_common.number import DelProps
from kaf_pas.system.models.contants import Contants

logger = logging.getLogger(__name__)


class Operation_typesQuerySet(BaseRefQuerySet):
    def update_or_create(self, defaults=None, **kwargs):
        res = super().update_or_create(**kwargs, defaults=defaults)
        if IsBitOn(defaults.get('props'), 2):
            logger.debug(f'Accountiing operations')
            Contants.objects.update_or_create(code=f'ACOUNTING', value=res[0].id)
        return res


class Operation_typesManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        from kaf_pas.planing.models.status_operation_types import Status_operation_typesManager
        from kaf_pas.planing.models.status_operation_types import Status_operation_types
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'full_name': record.full_name,
            'description': record.description,
            'parent_id': record.parent.id if record.parent else None,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
            'plus': record.props.plus,
            'minus': record.props.minus,
            'statuses': [Status_operation_typesManager.getRecord(statuses) for statuses in Status_operation_types.objects.filter(opertype_id=record.id)]
        }
        return DelProps(res)

    def get_queryset(self):
        return Operation_typesQuerySet(self.model, using=self._db)


class Operation_types(BaseRefHierarcy):
    props = BitField(flags=(
        ('plus', 'Приходная операция'),  # 1
        ('minus', 'Расходная операция'),  # 2
        ('accounting', 'Операция учета (для подсчета остатков в буферах)')  # 4
    ), default=0, db_index=True)

    objects = Operation_typesManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, full_name: {self.full_name}, parent_id: [{self.parent}], props: {self.props}, description: {self.description}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Типы системных операций'
