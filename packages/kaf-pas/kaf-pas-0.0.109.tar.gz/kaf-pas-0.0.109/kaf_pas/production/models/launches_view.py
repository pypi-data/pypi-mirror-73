import logging

from django.db.models import DateTimeField, BooleanField, DecimalField, PositiveIntegerField

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefManager, BaseRefQuerySet
from isc_common.number import DelProps, DecimalToStr
from kaf_pas.ckk.models.item import Item
from kaf_pas.production.models.status_launch import Status_launch
from kaf_pas.sales.models.demand import Demand

logger = logging.getLogger(__name__)


class Launches_viewQuerySet(BaseRefQuerySet):
    pass


class Launches_viewManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'date': record.date,
            'description': record.description,
            'parent_id': record.parent.id if record.parent else None,

            'demand_id': record.demand.id if record.demand else None,
            'demand__code': record.demand.code if record.demand else None,
            'demand__date': record.demand.date if record.demand else None,

            'item_id': record.item.id if record.item else None,
            'parent_item_id': record.parent_item.id if record.parent_item else None,
            'item__STMP_1_id': record.item.STMP_1.id if record.item and record.item.STMP_1 else None,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item and record.item.STMP_1 else None,
            'item__STMP_2_id': record.item.STMP_2.id if record.item and record.item.STMP_2 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item and record.item.STMP_2 else None,

            'status_id': record.status.id,
            'status__code': record.status.code,
            'status__name': record.status.name,

            'qty': DecimalToStr(record.qty),
            'qty_made': record.qty_made,
            'value_made': record.value_made,
            'value_sum': record.value_sum,
            # 'qty_need': record.qty_need,
            'isFolder': record.isFolder,
            'priority': record.priority if record.parent else '',
            # 'props': record.props,

            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return Launches_viewQuerySet(self.model, using=self._db)


class Launches_view(BaseRefHierarcy):
    # props = LaunchesManager.props()
    date = DateTimeField()
    demand = ForeignKeyProtect(Demand, null=True, blank=True)
    isFolder = BooleanField()
    item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Launches_view_item')
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Launches_view_parent_item')
    priority = PositiveIntegerField(db_index=True, default=0)
    qty = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    status = ForeignKeyProtect(Status_launch)
    value_made = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)

    objects = Launches_viewManager()

    @property
    def qty_made(self):
        # get_operations_values_sum(po.id, 'DETAIL_SUM_PRD_TSK', 'is_bit_on(planing_operation_value.props, 0) = false', polch.launch_id) as value_sum,
        # ExecuteStoredProc('get_operations_values_sum', [parent.id, 'RELEASE_TSK_PLS', None, launch_id])
        # res = ExecuteStoredProc('get_operations_values_sum', ['RELEASE_TSK_PLS', None, self.id])
        res = 0
        logger.debug(f'qty_made: {res}')
        return res

    @property
    def qty_need(self):
        res = self.qty - self.qty_made if self.qty else 0
        logger.debug(f'qty_need: {res}')
        return res

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = 'Запуски'
        db_table = 'production_launches_view'
        managed = False
