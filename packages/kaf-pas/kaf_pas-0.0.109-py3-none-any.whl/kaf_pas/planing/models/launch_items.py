import logging

from django.db.models import Manager, QuerySet, Model, F

from isc_common.fields.related import ForeignKeyProtect
from kaf_pas.ckk.models.item import Item, ItemManager
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Launch_itemsQuerySet(QuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Launch_itemsManager(Manager):
    @staticmethod
    def find_item(parent_launch, item, launch=None):

        if not isinstance(parent_launch, Launches):
            raise Exception(f'parent_launch must be Launches instance.')

        if launch and not isinstance(parent_launch, Launches):
            raise Exception(f'launch must be Launches instance.')

        items = ItemManager.find_item(item)
        if launch:
            launch_items = Launch_items.objects.filter(parent_launch=parent_launch, launch=launch, item__in=items).values('wlocation_id', 'location_id').exclude(location=F('wlocation')).distinct()
        else:
            launch_items = Launch_items.objects.filter(parent_launch=parent_launch, item__in=items).values('wlocation_id', 'location_id').exclude(location=F('wlocation')).distinct()

        return list(launch_items)

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
        }
        return res

    def get_queryset(self):
        return Launch_itemsQuerySet(self.model, using=self._db)


class Launch_items(Model):
    item = ForeignKeyProtect(Item)
    launch = ForeignKeyProtect(Launches, related_name='Launch_items_launch')
    parent_launch = ForeignKeyProtect(Launches, related_name='Launch_items_parent_launch')
    location = ForeignKeyProtect(Locations, related_name='Launch_items_parent_location')
    wlocation = ForeignKeyProtect(Locations, related_name='Launch_items_parent_wlocation')

    objects = Launch_itemsManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        verbose_name = 'Товарные позиции в данном запуске'
        db_table = 'planing_launch_items_view'
