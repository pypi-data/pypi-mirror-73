import logging

from django.contrib.postgres.fields import JSONField
from django.db.models import TextField

from isc_common import delAttr
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Operation_item_addQuerySet(AuditQuerySet):
    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None):
        request = DSRequest(request=request)
        data = request.get_data()

        delAttr(request.json.get('data'), 'level_id')

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(start=request.startRow, end=request.endRow, function=function, distinct_field_names=distinct_field_names, json=request.json, criteria=request.get_criteria())
        return res

class Operation_item_addManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
            'item_full_name': record.item_full_name,
        }
        return res

    def get_queryset(self):
        return Operation_item_addQuerySet(self.model, using=self._db)


class Operation_item_add(AuditModel):
    item = ForeignKeyCascade(Item)
    launch = ForeignKeyCascade(Launches)
    item_full_name = TextField(db_index=True)
    item_full_name_obj = JSONField(default=dict)

    objects = Operation_item_addManager()

    def __str__(self):
        return f"ID:{self.id}, item: [{self.item}], launch: [{self.launch}], item_full_name: {self.item_full_name}, item_full_name_obj: {self.item_full_name_obj}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('item', 'item_full_name', 'launch'),)
