import logging

from django.contrib.postgres.fields import ArrayField
from django.db.models import DecimalField, DateTimeField, TextField, PositiveIntegerField

from isc_common.auth.models.user import User
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeySetNull
from isc_common.models.base_ref import Hierarcy
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operation_operation import Operation_operation
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.production_order_opers import Production_order_opersManager
from kaf_pas.production.models.launches import Launches
from kaf_pas.production.models.resource import Resource

logger = logging.getLogger(__name__)

class Production_order_opers_per_launch(Hierarcy):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    date = DateTimeField(default=None)
    description = TextField(null=True, blank=True)
    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_opers_per_launch_opertype')
    creator = ForeignKeyProtect(User, related_name='Production_order_opers_per_launch_creator')
    status = ForeignKeyProtect(Status_operation_types)
    operation_operation = ForeignKeySetNull(Operation_operation, null=True, blank=True)
    num = CodeField()
    operation_operation_num = PositiveIntegerField()
    production_operation_num = PositiveIntegerField()
    production_operation_attrs = ArrayField(CodeField(null=True, blank=True))

    launch = ForeignKeyProtect(Launches)
    location = ForeignKeyProtect(Locations, related_name='Production_order_opers_per_launch_location')
    location_fin = ForeignKeySetNull(Locations, related_name='Production_order_opers_per_launch_location_fib', null=True, blank=True)

    resource = ForeignKeyProtect(Resource)
    edizm = ForeignKeyProtect(Ed_izm)
    value_sum = DecimalField(decimal_places=4, max_digits=19)
    value1_sum = DecimalField(decimal_places=4, max_digits=19)
    value_made = DecimalField(decimal_places=4, max_digits=19, null= True, blank=True)
    value_start = DecimalField(decimal_places=4, max_digits=19, null= True, blank=True)
    value_odd = DecimalField(decimal_places=4, max_digits=19)

    props = Operation_refsManager.props()

    objects = Production_order_opersManager()

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'planing_production_order_opers_per_launch_view'
        verbose_name = 'Операции Заказа на производство'
