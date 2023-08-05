import logging

from django.db.models import Model, DecimalField

from isc_common.common import blinkString
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Manager
from isc_common.models.standard_colors import Standard_colors
from isc_common.number import DelProps, DecimalToStr
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.production.models.launches import Launches
from kaf_pas.production.models.resource import Resource
from kaf_pas.sales.models.demand import Demand

logger = logging.getLogger(__name__)


class BuffersManager(Manager):
    @staticmethod
    def get_buffer_oddment_value(value):
        if value == None or value == 0:
            return ''
        return blinkString(text=DecimalToStr(value), blink=True if value < 0 else False, bold=True, color='green' if value > 0 else 'red')

    @staticmethod
    def getValue(item, color=None):
        try:
            buffer = Buffers.objects.get(item=item)
            return buffer.value if buffer.value else 0
        except Buffers.DoesNotExist:
            return None

    @staticmethod
    def getRecord(record):
        res = {
            'location_id': record.location.id if record.location else None,
            'resource_id': record.resource.id if record.resource else None,
            'location__code': record.location.code if record.location else None,
            'location__name': record.location.name if record.location else None,
            'location__full_name': record.location.full_name if record.location else None,
            'item_id': record.item.id,
            'value': BuffersManager.get_buffer_oddment_value(record.value),
            'demand_id': record.demand.id if record.demand else None,
            'demand__code': record.demand.code if record.demand else None,
            'demand__date': record.demand.date if record.demand else None,
            'launch_id': record.launch.id if record.launch else None,
            'launch__code': record.launch.code if record.launch else None,
            'launch__date': record.launch.date if record.launch else None,
            'color_id': record.color.id if record.color else None,
            'color__color': record.color.color if record.color else None,
            'color__name': record.color.name if record.color else None,
            'item__STMP_1_id': record.item.STMP_1.id if record.item.STMP_1 else None,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item.STMP_1 else None,
            'item__STMP_2_id': record.item.STMP_2.id if record.item.STMP_2 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item.STMP_2 else None,
            'edizm_id': record.edizm.id,
            'edizm__code': record.edizm.code,
            'edizm__name': record.edizm.name,
        }
        return DelProps(res)


class Buffers(Model):
    color = ForeignKeyProtect(Standard_colors, null=True, blank=True)
    demand = ForeignKeyProtect(Demand, null=True, blank=True)
    edizm = ForeignKeyProtect(Ed_izm)
    item = ForeignKeyProtect(Item)
    launch = ForeignKeyProtect(Launches, null=True, blank=True)
    location = ForeignKeyProtect(Locations, null=True, blank=True)
    resource = ForeignKeyProtect(Resource, null=True, blank=True)
    value = DecimalField(decimal_places=4, max_digits=19)

    objects = BuffersManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Буферы'
        managed = False
        db_table = 'accounting_buffers_view'
