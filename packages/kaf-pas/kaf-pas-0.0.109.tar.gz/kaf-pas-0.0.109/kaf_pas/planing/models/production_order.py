import copy
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import transaction
from django.db.models import DecimalField, DateTimeField, TextField, BooleanField, BigIntegerField, PositiveIntegerField
from django.forms import model_to_dict

from isc_common import setAttr, delAttr, NotImplementation
from isc_common.auth.models.user import User
from isc_common.common import blinkString, red, restarted, new
from isc_common.common.functions import ExecuteStoredProc
from isc_common.datetime import DateTimeToStr
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import Hierarcy
from isc_common.number import DecimalToStr, ToDecimal
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operation_item_view import Operation_item_view
from kaf_pas.planing.models.operation_launches import Operation_launches
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operations import OperationsManager, OperationsQuerySet
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class Production_orderQuerySet(OperationsQuerySet):

    def get_info(self, request, *args):
        request = DSRequest(request=request)
        data = request.get_data()
        launch_id = data.get('launch_id')
        json_all = dict()
        executor = None

        if not request.is_admin and not request.is_develop:
            executor = request.user

        if launch_id:
            launch = Launches.objects.get(id=launch_id)
            if launch.parent != None:
                items = [operation_item_view.item for operation_item_view in Operation_item_view.objects.filter(opertype_id=settings.OPERS_TYPES_STACK.ROUTING_TASK.id, launch=launch).distinct()]
                setAttr(request.json.get('data'), 'launch_id', launch.parent.id)
                setAttr(request.json.get('data'), 'item', items)

                json_all = copy.deepcopy(request.json)
                delAttr(json_all.get('data'), 'location_id')

        criteria = self.get_criteria(json=request.json)
        criteria_all = self.get_criteria(json=json_all)
        if executor != None:
            cnt = super().filter(exucutors__overlap=[executor.id]).filter(*args, criteria).count()
            cnt_all = super().filter(exucutors__overlap=[executor.id]).filter(*args, criteria_all).count()
        else:
            cnt = super().filter(*args, criteria).count()
            cnt_all = super().filter(*args, criteria_all).count()

        return dict(qty_rows=cnt, all_rows=cnt_all)

    @staticmethod
    def start(qty, _data, user, lock=True):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.planing.models.operations import Operations
        _res = []
        key = f'''get_setStartStatus_{_data.get('id')}'''
        if lock:
            settings.LOCKS.acquire(key)
        try:
            value_made = ExecuteStoredProc('get_value_made', [_data.get('id'), _data.get('launch_id')])

            if value_made > qty:
                if lock:
                    settings.LOCKS.release(key)
                raise Exception('Количество выпуска больше введенной суммы.')

            parent = Operations.objects.get(id=_data.get('id'))

            operation_refs = Operation_refs.objects.filter(
                parent=parent,
                child__opertype__code='LAUNCH_TSK'
            )

            if operation_refs.count() > 0:
                if qty == 0:
                    Operation_value.objects.filter(operation=operation_refs[0].child).delete()
                    Operation_launches.objects.filter(operation=operation_refs[0].child).delete()
                    parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(new)
                    operation_refs.delete()

                else:
                    Operation_value.objects.update_or_create(operation=operation_refs[0].child, defaults=dict(value=qty))
                    Operation_launches.objects.get_or_create(operation=operation_refs[0].child, launch=operation_refs[0].child.launch)
                    parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(restarted)

                parent.creator = user
                parent.save()

                if qty != 0:
                    res = model_to_dict(operation_refs[0].parent)
                    _data.update(res)
                    _res.append(_data)

                setAttr(_data, 'value_start', qty)

            else:
                if qty == 0:
                    if lock:
                        settings.LOCKS.release(key)
                    return _res

                res = Operations.objects.create(
                    opertype=settings.OPERS_TYPES_STACK.LAUNCH_TASK,
                    date=datetime.now(),
                    status=settings.OPERS_TYPES_STACK.LAUNCH_TASK_STATUSES.get('new'),
                    creator=user
                )

                parent = Operations.objects.get(id=_data.get('id'))
                parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get('started')
                parent.creator = user
                parent.save()

                Operation_refs.objects.create(parent=parent, child=res)
                Operation_value.objects.create(operation=res, edizm_id=_data.get('edizm_id'), value=qty)
                Operation_launches.objects.get_or_create(operation=res, launch_id=_data.get('launch_id'))

                res = model_to_dict(res)
                _data.update(res)
                setAttr(_data, 'value_start', qty)
                _res.append(_data)

            if lock:
                settings.LOCKS.release(key)
            return _res
        except Exception as ex:
            if lock:
                settings.LOCKS.release(key)
            raise ex

    def get_setStartStatus(self, request):

        request = DSRequest(request=request)

        data = request.get_data()
        qty = data.get('qty')
        if qty == None:
            raise Exception('Не введено количество.')

        idx = 0
        _res = []

        with transaction.atomic():
            while True:
                _data = data.get(str(idx))
                if _data == None:
                    break
                idx += 1

                _res = Production_orderQuerySet.start(
                    _data=_data,
                    qty=qty,
                    user=request.user
                )

        return _res

    def getLoocationUsers(self, request):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from isc_common.auth.managers.user_manager import UserManager

        request = DSRequest(request=request)
        data = request.get_data()
        location_sector_id = data.get('location_sector_id')
        location_id = data.get('location_id')

        parent_query = Locations_users.objects.filter(location_id=location_sector_id, user=request.user)
        parent = None
        if parent_query.count() > 0:
            parent = parent_query[0]

        if parent == None:
            parent_query = Locations_users.objects.filter(location_id=location_id, user=request.user)
            if parent_query.count() > 0:
                parent = parent_query[0]

        res = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id=location_id, parent=parent)]
        res1 = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id=location_sector_id)]

        res2 = list(set(res).intersection(res1))
        return [UserManager.getRecord1(User.objects.get(id=id)) for id in res2]


class Production_orderManager(OperationsManager):
    def createFromRequest(self, request):
        from kaf_pas.planing.models.launch_items import Launch_itemsManager
        from kaf_pas.production.models.launch_item_view import Launch_item_viewManager

        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        # NotImplementation()
        with transaction.atomic():

            launch = Launches.objects.get(id=_data.get('launch_id'))
            item = Item.objects.get(id=_data.get('item_id'))
            launch_items = Launch_itemsManager.find_item(parent_launch=launch, item=item)

            if len(launch_items) > 0:
                launch_items_str = '\n'.join([Locations.objects.get(id=launch.get('location_id')).full_name for launch in launch_items])
                raise Exception(blinkString(text=f'''{item.item_name} уже запущен на:\n<pre>{launch_items_str}</pre>''', blink=False, color=red, bold=True))

            parent_id = _data.get('parent_id')
            edizm_id = _data.get('edizm_id')
            value = _data.get('value_qty')
            color_id = _data.get('color_id')
            location_id = _data.get('location_id')
            description = _data.get('description')

            launches_query = Launches.objects.filter(parent=launch.id) if launch.parent == None else Launches.objects.filter(id=launch.id)

            launch_items = None
            for launch in launches_query:
                launch_items = Launch_item_viewManager.find_item(item=item, launch=launch)
                if len(launch_items) > 0:
                    break

            if len(launch_items) == 0:
                raise Exception(blinkString(text=f'''{item.item_name} не включена ни в одну производственную спецификвцию данного запуска.''', blink=False, color=red, bold=True))

            raise NotImplementation()

            # route_oparation_item = dict(
            #     item_id=item_id,
            #     launch_ids=[launch.id],
            #     launch_parent_id=launch.parent.id
            # )
            #
            # operationPlanItem = OperationPlanItem(**route_oparation_item)
            #
            # # Головная операция заказа
            # production_order_operation = Operations.objects.create(
            #     date=datetime.now(),
            #     opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK,
            #     status=settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get('new_man'),
            #     creator=request.user,
            #     editing=False,
            #     deliting=False
            # )
            # logger.debug(f'Created operation :  {production_order_operation}')
            #
            # operation_launches = Operation_launches.objects.create(
            #     operation=production_order_operation,
            #     launch=launch.parent
            # )
            # logger.debug(f'Created operation_launches :  {operation_launches}')
            #
            # operation_item = Operation_item.objects.create(
            #     operation=production_order_operation,
            #     item=operationPlanItem.item,
            # )
            # logger.debug(f'Created operation_item :  {operation_item}')
            #
            # for resource in operationPlanItem.resources:
            #     operation_resources, created = Operation_resources.objects.get_or_create(
            #         operation=production_order_operation,
            #         resource=resource
            #     )
            #     if created:
            #         logger.debug(f'Created operation_resources :  {operation_resources}')
            #
            # OperationsManager.rec_operations(
            #     launch=launch,
            #     status=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK_STATUSES.get('new'),
            #     operationPlanItem=operationPlanItem,
            #     operation=production_order_operation,
            #     opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK,
            #     user=request.user
            # )
            #
            # res = model_to_dict(production_order_operation)
        return data

    @staticmethod
    def get_resource_workshop(location_id):
        from kaf_pas.ckk.models.locations import Locations

        res = None
        for location in Locations.objects_tree.get_parents(id=location_id, child_id='id', include_self=False):
            if location.props.isWorkshop == True:
                res = dict(id=location.id, title=location.name, prompt=location.full_name)
                break

        if res == None:
            raise Exception(f'Не обнаружен цех, с признаком "Уровень цеха" для : {Locations.objects.get(id=location_id).full_name}')
        return res

    @staticmethod
    def getRecordLocations(record):
        return Production_orderManager.get_resource_workshop(record.get('location_id'))

    @staticmethod
    def getRecordLevels(record):
        return dict(id=record.get('level_id'), title=record.get('level__name'))

    def get_queryset(self):
        return Production_orderQuerySet(self.model, using=self._db)

    @staticmethod
    def getRecord(record):

        percents = round(ToDecimal(record.value_made) * 100 / ToDecimal(record.value_sum), 2)
        percents_str = "%.2f" % percents

        res = {
            'creator__short_name': record.creator.get_short_name,
            'date': record.date,
            'description': record.description,
            'edizm_id': record.edizm.id,
            'edizm__name': record.edizm.name,
            'id': record.id,
            'item_id': record.item.id,
            'parent_item_id': record.parent_item.id if record.parent_item else None,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item.STMP_1 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item.STMP_2 else None,
            'launch_id': record.launch.id,
            'launch__code': record.launch.code,
            'launch__date': record.launch.date,
            'location_id': record.location.id,
            'location__name': record.location.name,
            'location_sector_full_name': record.location_sector_full_name,
            'location_sector_id': record.location_sector_id,
            'num': record.num,
            'isFolder': record.isFolder,
            'cnt_opers': record.cnt_opers,
            'value_sum': DecimalToStr(record.value_sum),
            'value1_sum': DecimalToStr(record.value1_sum),
            'value_made': DecimalToStr(record.value_made),
            'value_made_str': f'''{blinkString(DecimalToStr(record.value_made), blink=True if percents >= 100 else False, color="blue", bold=True)}({percents_str}%)''',
            'value_start': DecimalToStr(record.value_start),
            'value_odd': DecimalToStr(record.value_odd),
            'opertype__full_name': record.opertype.full_name,
            'opertype_id': record.opertype.id,
            'parent_id': record.parent.id if record.parent else None,
            'status__code': record.status.code,
            'status__name': blinkString(text=record.status.name, blink=False, color=record.status.color, bold=False),
            'status_id': record.status.id,
        }
        return res


class Production_order(Hierarcy):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    date = DateTimeField(default=None)
    isFolder = BooleanField(default=None)
    num = CodeField()

    description = TextField(null=True, blank=True)

    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_opertype')
    creator = ForeignKeyProtect(User, related_name='Production_order_creator')
    exucutors = ArrayField(BigIntegerField(), default=list)
    status = ForeignKeyProtect(Status_operation_types)
    launch = ForeignKeyProtect(Launches)
    location = ForeignKeyProtect(Locations)
    edizm = ForeignKeyProtect(Ed_izm)
    item = ForeignKeyProtect(Item, related_name='Production_order_item')
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_parent_item')

    location_sector_full_name = TextField()
    location_sector_id = BigIntegerField()
    cnt_opers = PositiveIntegerField()

    value_sum = DecimalField(decimal_places=4, max_digits=19)
    value1_sum = DecimalField(decimal_places=4, max_digits=19)
    value_start = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_made = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(decimal_places=4, max_digits=19)

    props = Operation_refsManager.props()

    objects = Production_orderManager()

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
        db_table = 'planing_production_order_view'
