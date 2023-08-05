import logging

from django.contrib.postgres.fields import ArrayField
from django.db.models import DecimalField, BigIntegerField, TextField, BooleanField, DateTimeField, PositiveIntegerField

from isc_common.auth.models.user import User
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.base_ref import Hierarcy
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.production_order import Production_orderManager
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Production_order_per_launch(Hierarcy):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    date = DateTimeField(default=None)
    isFolder = BooleanField(default=None)
    num = CodeField()

    description = TextField(null=True, blank=True)

    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_per_launch_opertype')
    creator = ForeignKeyProtect(User, related_name='Production_order_per_launch_creator')
    exucutors = ArrayField(BigIntegerField(), default=list)
    status = ForeignKeyProtect(Status_operation_types)
    launch = ForeignKeyProtect(Launches)
    location = ForeignKeyProtect(Locations)
    edizm = ForeignKeyProtect(Ed_izm)
    cnt_opers = PositiveIntegerField()

    item = ForeignKeyProtect(Item, related_name='Production_order_per_launch_item')
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_per_launch_parent_item')

    location_sector_full_name = TextField()
    location_sector_id = BigIntegerField()

    value_sum = DecimalField(decimal_places=4, max_digits=19)
    value1_sum = DecimalField(decimal_places=4, max_digits=19)
    value_start = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_made = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(decimal_places=4, max_digits=19)

    props = Operation_refsManager.props()

    objects = Production_orderManager()

    started_partly = Status_operation_types.objects.get(code='started_partly')
    started = Status_operation_types.objects.get(code='started')

    def __str__(self):
        return f'id: {self.id}, ' \
               f'date: {DateTimeToStr(self.date)}, ' \
               f'num: {self.num}, ' \
               f'description: {self.description}, ' \
               f'opertype: [{self.opertype}], ' \
               f'creator: [{self.creator}], ' \
               f'exucutors: [{self.exucutors}], ' \
               f'status: [{self.status}], ' \
               f'launch: [{self.launch}], ' \
               f'location: [{self.location}], ' \
               f'edizm: [{self.edizm}], ' \
               f'item: [{self.item}], ' \
               f'parent_item: [{self.parent_item}], ' \
               f'location_sector_full_name: {self.location_sector_full_name}, ' \
               f'location_sector_id: {self.location_sector_id}, ' \
               f'cnt_opers: {self.cnt_opers}, ' \
               f'value_sum: {self.value_sum},' \
               f'value1_sum: {self.value1_sum},' \
               f'value_start: {self.value_start},' \
               f'value_made: {self.value_made},' \
               f'value_odd: {self.value_odd}, ' \
               f'props: {self.props},'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Заказы на производство'
        managed = False
        db_table = 'planing_production_order_per_launch_view'
