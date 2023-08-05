import logging

from django.db.models import PositiveIntegerField, BooleanField, DecimalField

from isc_common import delAttr
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade, ForeignKeySetNull
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps, DecimalToStr
from kaf_pas.accounting.models.buffers import BuffersManager
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item_add, Item
from kaf_pas.ckk.models.item_line import Item_line, Item_lineManager
from kaf_pas.kd.models.document_attributes import Document_attributes

logger = logging.getLogger(__name__)


class Launch_item_order_viewQuerySet(AuditQuerySet):
    def get_range_rows2(self, request, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        # launch_id = data.get('launch_id')
        # launch_id = [launch.id for launch in Launches.objects.filter(parent_id=launch_id)]
        delAttr(data, 'launch_id')
        request.set_data(data)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user
        )
        return res


class Launch_item_order_viewManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'child_id': record.child.id,
            'deliting': record.deliting,
            'editing': record.editing,
            'edizm__name': record.edizm.name if record.edizm else None,
            'edizm_id': record.edizm.id if record.edizm else None,
            'enabled': record.enabled,
            'id': record.id,
            'item_props': record.item_props,
            'lastmodified': record.lastmodified,
            'parent_id': record.parent.id,
            'qty_doc': DecimalToStr(record.qty_doc),
            'qty_exists': BuffersManager.get_buffer_oddment_value(record.qty_exists),
            'qty_per_one': DecimalToStr(record.qty_per_one) if record.section != 'Документация' else None,
            'relevant': record.relevant,
            'section': record.section,
            'section_num': Item_lineManager.section_num(record.section),
            'SPC_CLM_MARK__value_str': record.SPC_CLM_MARK.value_str if record.SPC_CLM_MARK else None,
            'SPC_CLM_MARK_id': record.SPC_CLM_MARK.id if record.SPC_CLM_MARK else None,
            'SPC_CLM_NAME__value_str': record.SPC_CLM_NAME.value_str if record.SPC_CLM_NAME else None,
            'SPC_CLM_NAME_id': record.SPC_CLM_NAME.id if record.SPC_CLM_NAME else None,
            'subsection': record.subsection,
            'where_from': record.where_from,
        }
        return DelProps(res)

    def get_queryset(self):
        return Launch_item_order_viewQuerySet(self.model, using=self._db)


class Launch_item_order_view(AuditModel):
    parent = ForeignKeyProtect(Item, verbose_name='Товарная позиция', related_name='item_parent_p')
    child = ForeignKeyCascade(Item, verbose_name='Товарная позиция', related_name='item_child_p')

    SPC_CLM_MARK = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение', related_name='SPC_CLM_MARK_p', null=True, blank=True)
    SPC_CLM_NAME = ForeignKeyProtect(Document_attributes, verbose_name='Наименование', related_name='SPC_CLM_NAME_p', null=True, blank=True)
    item = ForeignKeyProtect(Item, related_name='Item_p')
    edizm = ForeignKeyProtect(Ed_izm, verbose_name='Еденица измерения', related_name='EdIzm_p', null=True, blank=True)
    section = NameField()
    section_num = PositiveIntegerField(default=0)
    subsection = NameField()
    item_line = ForeignKeySetNull(Item_line, null=True, blank=True)

    qty_doc = DecimalField(decimal_places=4, max_digits=19)
    qty_per_one = DecimalField(decimal_places=4, max_digits=19)
    qty_exists = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)

    where_from = NameField()
    item_props = Item_add.get_prop_field()
    relevant = NameField()
    enabled = BooleanField()

    objects = Launch_item_order_viewManager()

    class Meta:
        verbose_name = 'Строка состава изделия в производственной спецификации'
        db_table = 'production_launch_item_prod_order_view'
        managed = False
        # proxy = True
