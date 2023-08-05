import logging
from datetime import datetime

from django.conf import settings
from django.db import transaction, connection
from django.db.models import TextField, DateTimeField
from django.forms import model_to_dict

from events.events_manager import Event
from isc_common import StackElementNotExist, delAttr, setAttr, Stack
from isc_common.auth.models.user import User
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.common.mat_views import create_tmp_mat_view, drop_mat_view
from isc_common.datetime import DateToStr, DateTimeToStr
from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager, CommonQuerySet
from isc_common.models.base_ref import Hierarcy
from isc_common.number import DelProps
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.status_operation_types import Status_operation_types
from kaf_pas.production.models.launch_operation_material import Launch_operations_material
from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
from kaf_pas.production.models.launch_operations_item import Launch_operations_item

logger = logging.getLogger(__name__)


class Operation_executor_message():
    def __init__(self, executor, message):
        self.executor = executor
        self.message = message

    def __str__(self):
        return f'executor : {self.executor}, message: {self.message}'


class Operation_executor_messages():
    def __init__(self, executor, message):
        self.executor = executor
        self.messages = Stack([message])


class Operation_executor_stack(Stack):
    len = 0

    def push(self, item: Operation_executor_message, logger=None):
        if not isinstance(item.executor, User):
            raise Exception(f'executor mast be User instance')

        try:
            executor = self.find_one(lambda _item: _item.executor.id == item.executor.id)
            if executor.messages.push(item.message, lambda _: executor.messages.exists(lambda _item: item == item.message), logger):
                self.len += 1
        except StackElementNotExist:
            super().push(Operation_executor_messages(executor=item.executor, message=item.message))
            self.len += 1


class OperationEvent(Event):
    def send_message(self, message=None, users_array=None, progress=None, len=None):
        if isinstance(users_array, User):
            users_array = [users_array]
        super().send_message(message=message, users_array=users_array, progress=progress)

    def send_message1(self, operation_executor_stack: Operation_executor_stack, progress=None):
        for operation_executor_messages in operation_executor_stack.stack:
            for message in operation_executor_messages.messages.stack:
                super().send_message(message=message, users_array=[operation_executor_messages.executor], progress=progress)


class OperationsQuerySet(CommonQuerySet):

    @staticmethod
    def _rec_history(operation, user):
        from kaf_pas.planing.models.operation_history import Operation_history
        Operation_history.objects.create(
            creator=user,
            operation=operation,
            status=operation.status
        )

    def create(self, **kwargs):
        from isc_common.seq import get_deq_next_value
        if kwargs.get('num') == None:
            setAttr(kwargs, 'num', str(get_deq_next_value('planing_operations_id_seq')))

        res = super().create(**kwargs)
        self._rec_history(operation=res, user=kwargs.get('creator'))
        return res

    def update(self, **kwargs):
        res = super().update(**kwargs)
        self._rec_history(operation=res, user=kwargs.get('creator'))
        return res


class Route_item():

    def __init__(self, item_id, first_operation, last_operation):
        self.item_id = item_id
        self.first_operation = first_operation
        self.last_operation = last_operation

    def __str__(self):
        return f'item_id: {self.item_id}, first_operation: [{self.first_operation}], last_operation: [{self.last_operation}]'


class OperationPlanItem:
    def __init__(self, *args, **kwargs):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.resource import Resource

        class OperationsItem:
            def __init__(self, operation_item):
                operation_resources = Operation_resources.objects.get(operationitem=operation_item)

                self.operation_item = operation_item
                self.operation_resource = operation_resources
                self.resource = operation_resources.resource
                self.location_fin = operation_resources.location_fin
                if self.resource == None:
                    self.resource, _ = Resource.objects.get_or_create(location=self.operation_resource.location, code='none')
                self.operation_materials = Stack([operation_material for operation_material in Operation_material.objects.filter(operationitem=operation_item)])

            def __str__(self):
                return f'''\n\noperation_item: [\n\n{self.operation_item}] \n operation_resource: [{self.operation_resource}] \n operation_materials: [[{", ".join([operation_material for operation_material in self.operation_materials])}]]'''

        class LaunchSumValue:
            def __init__(self, sum_value, sum_value1, edizm_id, launch_id, item_id):
                from kaf_pas.production.models.launches import Launches

                self.sum_value = sum_value
                self.sum_value1 = sum_value1
                self.edizm_id = edizm_id
                self.item_id = item_id
                self.launch = Launches.objects.get(id=launch_id)

            def __str__(self):
                return f'sum: {self.sum}, launch: [{self.launch}]'

        class LaunchSumValues(Stack):
            def __init__(self, item, launch_ids):
                self.stack = []
                with connection.cursor() as cursor:
                    sql_str = f'''select sum(distinct pov.value),
                                           sum(distinct pov1.value),
                                           pol.launch_id,
                                           pov.edizm_id 
                                    from planing_operation_launches as pol
                                             join planing_operations as po on po.id = pol.operation_id
                                             join planing_operation_item as poit on po.id = poit.operation_id
                                             join planing_operation_value pov on pov.operation_id = po.id
                                             join planing_operation_value pov1 on pov1.operation_id = po.id
                                    where pol.launch_id in %s
                                      and po.opertype_id = %s
                                      and poit.item_id = %s
                                      and is_bit_on(pov.props::integer, 0) = false
                                      and is_bit_on(pov1.props::integer, 0) = true
                                    group by pol.launch_id, pov.edizm_id'''
                    cursor.execute(sql_str, [launch_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id, item.id])
                    rows = cursor.fetchall()

                    for row in rows:
                        sum_value, sum_value1, launch_id, edizm_id = row
                        l = LaunchSumValue(sum_value=sum_value, sum_value1=sum_value1, edizm_id=edizm_id, launch_id=launch_id, item_id=item.id)
                        self.push(l)

            def __str__(self):
                return '\n\n'.join([f'[{elem}]' for elem in self.stack])

        if len(kwargs) == 0:
            raise Exception(f'{self.__class__.__name__} kwargs is empty')

        for k, v in kwargs.items():
            setattr(self, k, v() if callable(v) else v)

        if isinstance(self.item_id, int):
            self.item = Item.objects.get(id=self.item_id)

        if self.item == None:
            raise Exception(f'self.item not determined')

        with connection.cursor() as cursor:

            self.operations_item = Stack([OperationsItem(operation_item) for operation_item in Operations_item.objects.filter(item=self.item).order_by('num')])
            self.resources_location_fin_arr = [(operation_item.resource, operation_item.location_fin) for operation_item in self.operations_item.stack]

            operation_item = self.operations_item.stack[0].operation_item
            resource = Operation_resources.objects.get(operationitem=operation_item)
            top_resource = OperationsManager.get_resource_workshop(resource)

            self.locations_users = [location_user for location_user in OperationsManager.get_locations_users_query(resource=top_resource)]

            sql_str = '''select sum(pov.value)
            from planing_operation_level as polv
                     join planing_operation_launches as pol on polv.operation_id = pol.operation_id
                     join planing_operations as po on po.id = pol.operation_id
                     join planing_operation_item as poit on po.id = poit.operation_id
                     join planing_operation_value pov on pov.operation_id = po.id
            where pol.launch_id in %s
              and po.opertype_id = %s
              and poit.item_id = %s
              and is_bit_on(pov.props, 0) = true'''

            cursor.execute(sql_str, [self.launch_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id, self.item.id])
            self.value1, = cursor.fetchone()

        self.launchSumValues = LaunchSumValues(item=self.item, launch_ids=self.launch_ids)

    def __str__(self):
        return f'item: {self.item} \n value_sum: {self.value}\n value_per_one: {self.value1}\n\n launchSumValues: [\n{self.launchSumValues.stack}\n] \n\n operations_item: [\n{", ".join([f"[{elem}]" for elem in self.operations_item])}]'


class OperationsManager(CommonManager):

    @staticmethod
    def check_refs_free(operation_id):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        return Operation_refs.objects.filter(child_id=operation_id).count() == 0 and Operation_refs.objects.filter(parent_id=operation_id).count() == 0

    @staticmethod
    def delete_recursive(operation, user, soft_delete=False, opertypes=None, pre_delete_function=None, lock=True):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        key = f'OperationsManager.delete_recursive_{operation.id}'
        if lock:
            settings.LOCKS.acquire(key)

        sql_text = f'''WITH RECURSIVE r AS (
                                                    SELECT cir.*, cich.opertype_id, 1 AS level
                                                    FROM planing_operation_refs cir
                                                             join planing_operations cich on cich.id = cir.child_id
                                                    WHERE cir.child_id IN ({operation.id})

                                                    union all

                                                    SELECT cir.* , cich.opertype_id , r.level + 1 AS level
                                                    FROM planing_operation_refs cir
                                                             join planing_operations cich on cich.id = cir.child_id
                                                             JOIN r ON cir.parent_id = r.child_id
                                                )

                                                    select *  from r
                                                      where opertype_id in  ({opertypes})
                                                     order by level desc'''

        count = Operation_refs.objects.get_descendants_count(id=operation.id, sql_text=sql_text if opertypes != None else None)
        operations = set()

        if count > 0:
            with managed_progress(
                    id=operation.id,
                    qty=count,
                    user=user,
                    message='Удаление связанных операций операций',
                    title='Выполнено',
                    # props=TurnBitOn(0, 0)
            ) as progress:
                # with transaction.atomic():
                for operation_refs in Operation_refs.objects.get_descendants(
                        id=operation.id,
                        sql_text=sql_text if opertypes != None else None):
                    if not soft_delete:
                        Operation_refs.objects.filter(id=operation_refs.id).delete()
                        operations.add(operation_refs.child.id)
                    else:
                        Operation_refs.objects.filter(id=operation_refs.id).soft_delete()

                    if progress.step() != 0:
                        if lock:
                            settings.LOCKS.release(key)
                        raise ProgressDroped(progress_deleted)

                if not soft_delete:
                    for operation_id in list(operations):
                        # if OperationsManager.check_refs_free(operation_id=operation_id) == True:
                        OperationsManager.delete_recursive(operation=Operations.objects.get(id=operation_id), user=user, lock=False)
                        for op in Operations.objects.filter(id=operation_id):
                            if callable(pre_delete_function):
                                pre_delete_function(operation)

                            # ExecuteStoredProc("delete_operation", [op.id])
                            for operation_refs in Operation_refs.objects.filter(parent=op):
                                try:
                                    OperationsManager.delete_recursive(operation=operation_refs.child, user=user, lock=False)
                                except Operations.DoesNotExist:
                                    pass
                            Operations.objects.filter(id=op.id).delete()

        if lock:
            settings.LOCKS.release(key)

    @staticmethod
    def set_location(location_id, operation_id, resource_id=None):
        from kaf_pas.production.models.resource import Resource
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from clndr.models.calendars import CalendarsManager

        if location_id:
            resource = None
            if resource_id == None:
                try:
                    resource = Resource.objects.get(code='none', location_id=location_id)
                except Resource.DoesNotExist:
                    resource = Resource.objects.create(code='node', name='Не определен', location_id=location_id, calendar=CalendarsManager.get_default())

            if resource == None:
                resource = Resource.objects.get(id=resource_id)
                if resource.location_id != location_id:
                    resource = Resource.objects.create(location_id=location_id, calendar=resource.calendar)

            Operation_resources.objects.update_or_create(operation_id=operation_id, resource=resource)

    @staticmethod
    def set_anothers(operation_id, item_id=None, edizm_id=None, value=None, color_id=None, old_data=dict()):
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.planing.models.operation_color import Operation_color

        if item_id:
            operation_item, created = Operation_item.objects.update_or_create(
                operation_id=operation_id,
                defaults=dict(
                    item_id=item_id,
                ))
        else:
            deleted, _ = Operation_item.objects.filter(
                operation_id=operation_id,
                item_id=old_data.get(item_id),
            ).delete()

        if edizm_id and value:
            operation_value, created = Operation_value.objects.update_or_create(
                operation_id=operation_id,
                value=old_data.get('value'),
                defaults=dict(edizm_id=edizm_id, value=value))
        else:
            deleted, _ = Operation_value.objects.filter(
                operation_id=operation_id,
                edizm_id=old_data.get('edizm_id'),
                value=old_data.get('value'),
            ).delete()

        if color_id:
            operation_color, created = Operation_color.objects.update_or_create(
                operation_id=operation_id,
                defaults=dict(color_id=color_id))
        else:
            deleted, _ = Operation_color.objects.filter(
                operation_id=operation_id,
                color_id=old_data.get('color_id'),
            ).delete()

    def createFromRequest(self, request, removed=None):
        from kaf_pas.planing.models.operation_refs import Operation_refs

        request = DSRequest(request=request)
        data = request.get_data()
        old_data = request.get_oldValues()
        _data = data.copy()
        self._remove_prop(_data, removed)

        with transaction.atomic():
            parent_id = _data.get('parent_id')
            item_id = _data.get('item_id')
            edizm_id = _data.get('edizm_id')
            value = _data.get('value')
            color_id = _data.get('color_id')
            location_id = _data.get('location_id')

            delAttr(_data, 'parent_id')
            delAttr(_data, 'item_id')
            delAttr(_data, 'edizm_id')
            delAttr(_data, 'value')
            delAttr(_data, 'color_id')
            delAttr(_data, 'location_id')

            res = super().create(**_data)

            operation_id = res.id
            Operation_refs.objects.create(parent_id=parent_id, child_id=operation_id)

            OperationsManager.set_anothers(operation_id=operation_id, item_id=item_id, edizm_id=edizm_id, color_id=color_id, value=value, old_data=old_data)
            OperationsManager.set_location(location_id=location_id, operation_id=operation_id)

            res = model_to_dict(res)
            data.update(DelProps(res))
        return data

    def updateFromRequest(self, request, removed=None, function=None):

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        old_data = request.get_oldValues()

        _data = data.copy()
        delAttr(_data, 'creator_id')
        _data.setdefault('creator_id', request.user_id)

        item_id = _data.get('item_id')
        edizm_id = _data.get('edizm_id')
        value = _data.get('value')
        color_id = _data.get('color_id')
        location_id = _data.get('location_id')
        resource_id = _data.get('resource_id')
        operation_id = _data.get('id')
        description = _data.get('description')

        delAttr(_data, 'id')
        delAttr(_data, 'creator__short_name')

        delAttr(_data, 'opertype__full_name')
        delAttr(_data, 'isFolder')

        delAttr(_data, 'status__code')
        delAttr(_data, 'status__name')

        delAttr(_data, 'color__name')
        delAttr(_data, 'color__color')

        delAttr(_data, 'location__code')
        delAttr(_data, 'location__name')
        delAttr(_data, 'location__full_name')

        delAttr(_data, 'item__STMP_1_id')
        delAttr(_data, 'item__STMP_1__value_str')

        delAttr(_data, 'item__STMP_2_id')
        delAttr(_data, 'item__STMP_2__value_str')

        delAttr(_data, 'edizm__code')
        delAttr(_data, 'edizm__name')

        with transaction.atomic():
            OperationsManager.set_anothers(operation_id=operation_id, item_id=item_id, edizm_id=edizm_id, color_id=color_id, value=value, old_data=old_data)
            OperationsManager.set_location(location_id=location_id, resource_id=resource_id, operation_id=operation_id)

            delAttr(_data, 'item_full_name')
            delAttr(_data, 'item_full_name_obj')
            delAttr(_data, 'item_item_name')
            delAttr(_data, 'value')
            delAttr(_data, 'value_start')
            delAttr(_data, 'value_made')
            delAttr(_data, 'executors')
            delAttr(_data, 'launch__date')
            delAttr(_data, 'launch__code')
            delAttr(_data, 'launch__name')
            delAttr(_data, 'color__name')
            delAttr(_data, 'color__color')
            delAttr(_data, 'edizm_id')
            delAttr(_data, 'operation_id')

            super().filter(id=operation_id).update(**_data)
        return data

    def updateFromRequest4(self, request, removed=None, function=None):
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_resources import Operation_resources

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)

        data = request.get_data()
        executors = data.get('executors')

        idx = 0
        with transaction.atomic():
            while True:
                _data = data.get(str(idx))
                if _data == None:
                    break
                idx += 1

                operation_id = _data.get('id')
                description = _data.get('description')

                Operations.objects.update_or_create(id=operation_id, defaults=dict(description=description))

                if isinstance(executors, list):
                    res, _ = Operation_executor.objects.filter(operation_id=operation_id, executor=request.user).delete()
                    for executor_id in executors:
                        operation_executor, created = Operation_executor.objects.get_or_create(operation_id=operation_id, executor_id=executor_id)

                        main_oper_production_order = Operations.objects.get(id=operation_id)
                        operation_item = Operation_item.objects.get(operation=main_oper_production_order)

                        for operation_resource in Operation_resources.objects.filter(operation_id=operation_id).distinct():
                            executor = User.objects.get(id=executor_id)

                            message = f'<h3>Размещен новый заказ на производство ' \
                                      f'№{main_oper_production_order.num} от {DateTimeToStr(main_oper_production_order.date, hours=3)}.' \
                                      '<p/>' \
                                      f'{operation_item.item.item_name}' \
                                      '<p/>' \
                                      f'{operation_resource.resource.location.full_name}' \
                                      '<p/>'

                        settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                            message=message,
                            users_array=executor,
                        )
        return data

    def deleteFromRequest(self, request, removed=None, ):

        request = DSRequest(request=request)
        res = 0

        tuple_ids = request.get_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                else:
                    for operation in super().filter(id=id):
                        OperationsManager.delete_recursive(operation=operation, user=request.user)
                        res += 1
        return res

    @staticmethod
    def make_routing(data):
        from isc_common import Stack
        from kaf_pas.planing.models.levels import Levels
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_item_add import Operation_item_add
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_level import Operation_level
        from kaf_pas.planing.models.operation_material import Operation_material
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.production.models.launches import Launches

        # logger.debug(f'data: {data}')

        launch_ids = []
        launches_head = []

        for launch_id in data.get('data'):
            l = Launches.objects.filter(parent_id=launch_id)
            if l.count() > 0:
                launch_ids.extend([item.id for item in l])
                launches_head.append(Launches.objects.get(id=launch_id))
            else:
                launch_ids.extend([item.id for item in Launches.objects.filter(id=launch_id)])

        user = data.get('user')
        if not isinstance(user, User):
            raise Exception(f'user must be User instance.')

        launch_qty = Launches.objects.filter(id__in=launch_ids).count()

        idx = 0
        launch_res = None
        for launch in Launches.objects.filter(id__in=launch_ids):
            launch_res = launch
            if launch.status.code == 'route_made':
                continue

            key = f'OperationsManager.make_routing_{launch.id}'
            settings.LOCKS.acquire(key)
            sql_str = f'''with a as (
                                        with recursive r as (
                                            select *,
                                                   1 as level
                                            from production_launch_item_refs
                                            where parent_id is null
                                               and launch_id = {launch.id}
                                               and is_bit_on(props::int,0) = true
                                            union all
                                            select production_launch_item_refs.*,
                                                   r.level + 1 as level
                                            from production_launch_item_refs
                                                     join r
                                                          on
                                                              production_launch_item_refs.parent_id = r.child_id
                                            where is_bit_on(r.props::int,0) = true
                                            and is_bit_on(production_launch_item_refs.props::int,0) = true
                                        )

                                        select r1.id,
                                               r1.parent_id,
                                               r1.child_id,
                                               r1.launch_id,
                                               r1.qty,
                                               r1.replication_factor,
                                               r1.qty_per_one,
                                               r1.edizm,
                                               r1.level,
                                               r1.item_full_name,
                                               r1.item_full_name_obj                 
                                        from (select distinct r.id,
                                                              r.parent_id,
                                                              r.child_id,
                                                              r.launch_id,
                                                              r.item_full_name,
                                                              r.item_full_name_obj,
                                                              r.qty,
                                                              r.replication_factor,
                                                              r.qty_per_one,  
                                                              (
                                                                  select plil.section
                                                                  from production_launch_item_line plil
                                                                  where plil.child_id = r.child_id
                                                                    and plil.parent_id = r.parent_id
                                                                    and plil.launch_id = r.launch_id) section,
                                                              (
                                                                  select plil.edizm_id
                                                                  from production_launch_item_line plil
                                                                  where plil.child_id = r.child_id
                                                                    and plil.parent_id = r.parent_id
                                                                    and plil.launch_id = r.launch_id) edizm,  
                                                              level
                                              from r
                                                       join ckk_item ci on ci.id = r.child_id
                                              where r.launch_id = {launch.id}
                                              order by level desc) r1
                                        where lower(r1.section) != 'документация'
                                           or r1.parent_id is null
                                    )

                                    select a.id,
                                           a.parent_id,
                                           a.child_id,
                                           a.launch_id,
                                           a.qty,
                                           a.replication_factor,
                                           a.qty_per_one,
                                           a.edizm,
                                           a.level,
                                           a.item_full_name,
                                           a.item_full_name_obj
                                    from a'''

            mat_view_name = create_tmp_mat_view(sql_str=sql_str, indexes=['parent_id', 'child_id'])
            with connection.cursor() as cursor:
                cursor.execute(f'select count(*) from {mat_view_name}')
                count, = cursor.fetchone()

            logger.debug(f'Counted: {count}')

            with managed_progress(
                    id=f'launch_{launch.id}_{user.id}',
                    qty=count * 2,
                    user=user,
                    message=f'<h3>Расчет маршрутизации внутри товарных позиций, Запуск № {launch.code} от {DateToStr(launch.date)}</h3>',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                with transaction.atomic():
                    def except_func():
                        drop_mat_view(mat_view_name)
                        settings.LOCKS.release(key)

                    progress.except_func = except_func

                    with connection.cursor() as cursor:
                        cursor.execute(f'select max(level), min(level) from {mat_view_name}')
                        rows = cursor.fetchone()
                        min_level, max_level = rows

                        cursor.execute(f'select * from {mat_view_name} order by level desc')
                        rows = cursor.fetchall()

                        routed_items = Stack()

                        for row in rows:
                            def make_oparetions(row, mode='child'):
                                id, parent_id, child_id, launch_id, qty, replication_factor, qty_per_one, edizm_id, level, item_full_name, item_full_name_obj = row

                                # Более низкий уровень в иерархии товарной позиции соответствует более высокому в маршрутизации, т.к. необходимо изготавливать ранньше
                                level = max_level - (level - min_level)
                                logger.debug(f'level: {level}')

                                if mode == 'child':
                                    cursor.execute(f'select * from {mat_view_name} where qty is null and child_id = %s', [child_id])
                                    null_rows = cursor.fetchall()
                                    if len(null_rows) > 0:
                                        nulls_array = []
                                        for null_row in null_rows:
                                            id, parent_id, child_id, launch_id, qty, qty_per_one, level, item_full_name, item_full_name_obj = null_row
                                            nulls_str = f'<b>ID: {id}: {item_full_name}</b>'
                                            nulls_array.append(nulls_str)
                                        nulls_str = f'''{blinkString(text='Не указано количество : ', color='red')}<br><div>{'<br>'.join(nulls_array)}</div>'''
                                        settings.LOCKS.release(key)
                                        raise Exception(nulls_str)

                                    cursor.execute(f'select sum(qty * replication_factor) from {mat_view_name} where child_id = %s and launch_id = %s', [child_id, launch_id])
                                    qty = cursor.fetchone()[0]
                                    logger.debug(f'qty: {qty}')
                                    # cursor.execute(f'select sum(qty) from {mat_view_name} where parent_id = %s and launch_id = %s', [child_id, launch_id])
                                    # qty1 = cursor.fetchone()[0]

                                    # if qty1 == None:
                                    #     qty1 = 0

                                    # if qty1 != 0:
                                    #     logger.debug(f'qty1: {qty1}')
                                    # qty += qty1

                                elif mode == 'parent':
                                    if parent_id != None:
                                        child_id = parent_id

                                if not routed_items.exists(lambda child_item: child_item.item_id == child_id):
                                    income_operation = None
                                    first_operation = None

                                    # Выполняем маршрутизацию внутри товарной позиции согласно порядку выплонения оперций из production
                                    cnt1 = Launch_operations_item.objects.filter(item_id=child_id, launch_id=launch_id).count()
                                    if cnt1 > 0:
                                        for launch_operations_item in Launch_operations_item.objects.filter(item_id=child_id, launch_id=launch_id).order_by('num'):

                                            outcome_operation = Operations.objects.create(
                                                date=datetime.now(),
                                                opertype=settings.OPERS_TYPES_STACK.ROUTING_TASK,
                                                status=settings.OPERS_TYPES_STACK.ROUTING_TASK_STATUSES.get('new'),
                                                creator=user
                                            )
                                            logger.debug(f'Created outcome_operation :  {outcome_operation}')

                                            operation_launches = Operation_launches.objects.create(operation=outcome_operation, launch=launch)
                                            logger.debug(f'Created operation_launches :  {operation_launches}')

                                            operation_item = Operation_item.objects.create(
                                                operation=outcome_operation,
                                                item=launch_operations_item.item,
                                            )
                                            logger.debug(f'Created operation_item :  {operation_item}')

                                            operation_item_add, created = Operation_item_add.objects.get_or_create(
                                                item=launch_operations_item.item,
                                                launch=launch_operations_item.launch,
                                                item_full_name=item_full_name,
                                                defaults=dict(item_full_name_obj=item_full_name_obj)
                                            )
                                            logger.debug(f'Created operation_item_add :  {operation_item_add}')

                                            operation_operation = Operation_operation.objects.create(
                                                operation=outcome_operation,
                                                production_operation=launch_operations_item.operation,
                                                num=launch_operations_item.num,
                                                qty=launch_operations_item.qty,
                                                ed_izm=launch_operations_item.ed_izm,
                                            )
                                            logger.debug(f'Created operation_operation :  {operation_operation}')

                                            _level, created = Levels.objects.get_or_create(
                                                code=str(level),
                                                defaults=dict(
                                                    name=str(level),
                                                    editing=False,
                                                    deliting=False
                                                ))
                                            if created:
                                                logger.debug(f'Created level :  {_level}')

                                            operation_level = Operation_level.objects.create(operation=outcome_operation, level=_level)
                                            logger.debug(f'Created operation_level :  {operation_level}')

                                            operation_value = Operation_value.objects.create(
                                                operation=outcome_operation,
                                                value=qty_per_one,
                                                edizm_id=edizm_id,
                                                props=Operation_value.props.perone
                                            )
                                            logger.debug(f'Created operation_value :  {operation_value}')

                                            operation_value = Operation_value.objects.create(
                                                operation=outcome_operation,
                                                value=qty,
                                                edizm_id=edizm_id
                                            )
                                            logger.debug(f'Created operation_value :  {operation_value}')

                                            for launch_operation_material in Launch_operations_material.objects.filter(launch_operationitem=launch_operations_item):
                                                if launch_operation_material.operation_material != None:
                                                    operation_material, _ = Operation_material.objects.get_or_create(
                                                        operation=outcome_operation,
                                                        material=launch_operation_material.material,
                                                        material_askon=launch_operation_material.material_askon,
                                                        defaults=dict(
                                                            edizm=launch_operation_material.edizm,
                                                            qty=launch_operation_material.qty,
                                                        )
                                                    )
                                                    logger.debug(f'Created operation_material :  {operation_material}')

                                            def exception_not_resource():
                                                from isc_common.common import blinkString
                                                settings.LOCKS.release(key)
                                                raise Exception(f'''<b>Для : {item_full_name}</b>  {blinkString(text='не задан ресурс.  Запустите анализатор готовности к запуску.', blink=False, color='red', bold=True)}''')

                                            if Launch_operation_resources.objects.filter(launch_operationitem=launch_operations_item).count() == 0:
                                                exception_not_resource()

                                            for launch_operation_resources in Launch_operation_resources.objects.filter(launch_operationitem=launch_operations_item):
                                                operation_resources = Operation_resources.objects.create(
                                                    operation=outcome_operation,
                                                    resource=launch_operation_resources.resource,
                                                    location_fin=launch_operation_resources.location_fin
                                                )
                                                logger.debug(f'Created operation_resources :  {operation_resources}')

                                            if income_operation == None:
                                                first_operation = outcome_operation

                                            operation_refs = Operation_refs.objects.create(
                                                parent=income_operation,
                                                parent_real=income_operation,
                                                child=outcome_operation,
                                                props=Operation_refs.props.inner_routing
                                            )
                                            logger.debug(f'Created operation_refs :  {operation_refs}')

                                            income_operation = outcome_operation
                                            cnt1 -= 1
                                            if cnt1 == 0:
                                                routed_items.push(Route_item(item_id=child_id, first_operation=first_operation, last_operation=outcome_operation), logger=logger)
                                    else:
                                        def exception_not_operations():
                                            from isc_common.common import blinkString
                                            settings.LOCKS.release(key)
                                            raise Exception(f'''<b>Для : {item_full_name}</b>  {blinkString(text='не задано ни одной операции. Запустите анализатор готовности к запуску.', blink=False, color='red', bold=True)}''')

                                        exception_not_operations()

                            make_oparetions(row=row)

                            if progress.step() != 0:
                                settings.LOCKS.release(key)
                                raise ProgressDroped(progress_deleted)

                        # Выполняем маршрутизацию между товарными позициями соединяя последнюю оперцию предыдущей товарной позиции с первой операциеей следующей
                        # товарной позиции
                        progress.setContentsLabel(f'<h3>Расчет маршрутизации между товарными позициями, Запуск № {launch.code} от {DateToStr(launch.date)}</h3>')

                        for row in rows:
                            id, parent_id, child_id, launch_id, qty, replication_factor, qty_per_one, edizm_id, level, item_full_name, item_full_name_obj = row
                            try:
                                if parent_id == None:
                                    parent_id = child_id
                                parent_item = routed_items.find_one(lambda item: item.item_id == parent_id)
                            except StackElementNotExist:
                                logger.warning(f'parent_id: {parent_id} !!!!!!!!!!!!!!!!!!Товарная позиция не обнаружена среди товарных позиций, прошедших внутреннюю маршрутизацию !!!!!!!!!!!!!!!!')
                                # Если товарная позиция не обнаружена среди товарных позиций, прошедших внутреннюю маршрутизацию

                                make_oparetions(row=row, mode='parent')
                                parent_item = routed_items.find_one(lambda item: item.item_id == parent_id)

                            cursor.execute(f'''select child_id from {mat_view_name} where parent_id = %s''', [parent_id])
                            parents_rows = cursor.fetchall()
                            for parents_row in parents_rows:
                                _child_id, = parents_row
                                _child = routed_items.find_one(lambda item: item.item_id == _child_id)

                                operation_refs, created = Operation_refs.objects.get_or_create(
                                    parent=_child.last_operation,
                                    parent_real=_child.last_operation,
                                    child=parent_item.first_operation,
                                    defaults=dict(
                                        props=Operation_refs.props.outer_routing
                                    )
                                )
                                logger.debug(f'Created operation_refs :  {operation_refs}')

                                deleted, _ = Operation_refs.objects.filter(parent__isnull=True, child=parent_item.last_operation).delete()
                            if progress.step() != 0:
                                settings.LOCKS.release(key)
                                raise ProgressDroped(progress_deleted)

                    launch.status = settings.PROD_OPERS_STACK.ROUTMADE
                    launch.save()

                    progress.sendMessage(type='refresh_launches_grid')
                    settings.EVENT_STACK.EVENTS_PRODUCTION_MAKE_ROUTING.send_message(f'<h3>Выполнен Расчет маршрутизации: Запуск № {launch.code} от {DateToStr(launch.date)}</h3><p/>')

                    settings.LOCKS.release(key)
                    drop_mat_view(mat_view_name)

                    idx += 1
                    if idx == launch_qty:
                        for launche_head in launches_head:
                            launche_head.status = settings.PROD_OPERS_STACK.ROUTMADE
                            launche_head.save()
                        # progress.setContentsLabel('Обновление предстваления planing_production_order_mview')
                        progress.sendMessage(type='refresh_launches_grid')

        # if idx == launch_qty:
        #     refresh_mat_view('planing_production_order_mview')

        return model_to_dict(launch_res)

    @staticmethod
    def clean_routing(data):
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.planing.models.operation_launches import Operation_launches

        launch_ids = []
        launches_head = []
        for launch_id in data.get('data'):
            l = Launches.objects.filter(parent_id=launch_id)
            if l.count() > 0:
                launch_ids.extend([item.id for item in l])
                launches_head.append(Launches.objects.get(id=launch_id))
            else:
                launch_ids.extend([item.id for item in Launches.objects.filter(id=launch_id)])

        _launch = None
        launch_query = Launches.objects.filter(id__in=launch_ids)
        launch_qty = launch_query.count()
        idx = 0
        for launch in launch_query:
            if launch.status.code == 'formirovanie':
                continue

            user = data.get('user')
            key = f'OperationsManager.clean_routing_{launch_id}'
            settings.LOCKS.acquire(key)
            query = Operation_launches.objects.filter(launch=launch, operation__opertype__in=[
                settings.OPERS_TYPES_STACK.ROUTING_TASK,
            ])

            cnt = query.count()
            with managed_progress(
                    id=launch.id,
                    qty=cnt,
                    user=user,
                    message=f'<h3>Удаление маршрутизации: Запуск № {launch.code} от {DateToStr(launch.date)}</h3>',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                with transaction.atomic():
                    def except_func():
                        settings.LOCKS.release(key)

                    progress.except_func = except_func

                    launch.status = launch.status = settings.PROD_OPERS_STACK.FORMIROVANIE
                    launch.save()

                    for operation_launches in query:
                        try:
                            OperationsManager.delete_recursive(operation=operation_launches.operation, user=user)
                        except Operations.DoesNotExist:
                            pass

                        if progress.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

                    if cnt > 0:
                        settings.EVENT_STACK.EVENTS_PRODUCTION_DELETE_ROUTING.send_message(f'<h3>Выполнено Удаление маршрутизации: Запуск № {launch.code} от {DateToStr(launch.date)}</h3><p/>')
                    progress.sendMessage(type='refresh_launches_grid')

                    settings.LOCKS.release(key)

                    idx += 1
                    if idx == launch_qty:
                        for launche_head in launches_head:
                            launche_head.status = settings.PROD_OPERS_STACK.FORMIROVANIE
                            launche_head.save()

                        return model_to_dict(launch)

    @staticmethod
    def get_locations_users_query(resource):
        from kaf_pas.ckk.models.locations_users import Locations_users

        locations_users_query = Locations_users.objects.filter(location=resource.location, parent__isnull=True)
        if locations_users_query.count() == 0:
            raise Exception(blinkString(text=f'Не обнаружен ответственный исполнитель для : {resource.location.full_name}', bold=True))

        return locations_users_query

    # Определить цех ресурса
    @staticmethod
    def get_resource_workshop(resource):
        from kaf_pas.ckk.models.locations import Locations

        res = None
        for location in Locations.objects_tree.get_parents(id=resource.location.id, child_id='id', include_self=False):
            if location.props.isWorkshop == True:
                res, _ = settings.OPERS_STACK.NOT_UNDEFINED_WORKSHOP(location)
                return res

        if res == None:
            raise Exception(f'Не обнаружен цех, с признаком "Уровень цеха" для : Location ID: {resource.location.id} {resource.location.full_name}, Resource ID: {resource.id}: {resource.name}')
        return res

    @staticmethod
    def rec_operations(launch, status, operationPlanItem, operation, opertype, user):
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_material import Operation_material
        from kaf_pas.planing.models.operation_operation import Operation_operation
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources

        for operations_item in operationPlanItem.operations_item:
            production_order_operation_opers = Operations.objects.create(
                date=datetime.now(),
                opertype=opertype,
                status=status,
                creator=user,
                editing=False,
                deliting=False
            )

            operation_launches = Operation_launches.objects.create(
                operation=production_order_operation_opers,
                launch=launch
            )
            logger.debug(f'Created operation_launches :  {operation_launches}')

            operation_resources = Operation_resources.objects.create(
                operation=production_order_operation_opers,
                resource=operations_item.resource,
                location_fin=operations_item.location_fin
            )
            logger.debug(f'Created operation_resources :  {operation_resources}')

            for operation_material in operations_item.operation_materials:
                operation_material = Operation_material.objects.create(
                    operation=production_order_operation_opers,
                    material=operation_material.material,
                    material_askon=operation_material.material_askon,
                    edizm=operation_material.edizm,
                    qty=operation_material.qty,
                )
                logger.debug(f'Created operation_material :  {operation_material}')

            operation_operation = Operation_operation.objects.create(
                operation=production_order_operation_opers,
                production_operation=operations_item.operation_item.operation,
                num=operations_item.operation_item.num,
                qty=operations_item.operation_item.qty,
                ed_izm=operations_item.operation_item.ed_izm
            )
            logger.debug(f'Created operation_operation :  {operation_operation}')

            operation_item, created = Operation_item.objects.get_or_create(
                operation=production_order_operation_opers,
                item_id=operationPlanItem.item_id,
            )
            if created:
                logger.debug(f'Created operation_item :  {operation_item}')

            operation_refs = Operation_refs.objects.create(
                parent=operation,
                child=production_order_operation_opers,
                props=Operation_refs.props.product_order_routing
            )
            logger.debug(f'Created operation_refs :  {operation_refs}')

    @staticmethod
    def make_production_order(data):
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.planing.models.operation_value import Operation_value
        from kaf_pas.production.models.launches import Launches

        user = data.get('user')
        if isinstance(user, int):
            user = User.objects.get(id=user)

        OperationsManager.make_routing(data=data)

        new_status_order_prod = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get('new')
        new_status_order_prod_sum = settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK_STATUSES.get('new')
        new_status_order_prod_opers = settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK_STATUSES.get('new')

        class Launch_pair:
            def __init__(self, child, parent):
                self.child = Launches.objects.get(id=child)
                self.parent = Launches.objects.get(id=parent)

            def __str(self):
                return f'child: [{self.child}], parent: [{self.parent}]'

        class Launch_pairs(Stack):
            def get_parents(self):
                res = set()
                for item in self.stack:
                    for item1 in item:
                        res.add(item1.parent)

                return list(res)

            def get_childs(self, parent):
                res = set()
                for item in self.stack:
                    res1 = [i.child for i in item if i.parent == parent]
                    for r in res1:
                        res.add(r)
                return list(res)

        launch_pairs = Launch_pairs()

        launches_head = []
        for launch_id in data.get('data'):
            l = Launches.objects.filter(parent_id=launch_id)
            if l.count() > 0:
                launch_pairs.push([Launch_pair(parent=launch_id, child=item.id) for item in l])
                launches_head.append(Launches.objects.get(id=launch_id))
            else:
                launch_pairs.push([Launch_pair(parent=item.id, child=item.id) for item in Launches.objects.filter(id=launch_id)])

        for launch_parent in launch_pairs.get_parents():
            if launch_parent.status.code == 'in_production':
                continue

            key = f'OperationsManager.make_production_order_{launch_parent.id}'
            settings.LOCKS.acquire(key)

            launch_childs = launch_pairs.get_childs(parent=launch_parent)
            Launch_childs_ids = tuple([launch.id for launch in launch_childs])

            operation_executor_stack = Operation_executor_stack()

            sql_items = '''select poit.item_id
                          from planing_operation_item as poit
                            join planing_operation_launches as pol on poit.operation_id = pol.operation_id
                            join planing_operations as po on po.id = pol.operation_id
                          where pol.launch_id in %s
                            and po.opertype_id = %s
                          group by poit.item_id'''

            sql_items_launch = '''select array_agg(poit_det.operation_id)
                                from planing_operation_item as poit_det
                                         join planing_operation_launches as pol on poit_det.operation_id = pol.operation_id
                                         join public.planing_operations as po on po.id = pol.operation_id
                                where pol.launch_id = %s
                                  and po.opertype_id = %s
                                  and poit_det.item_id = %s
                                group by pol.launch_id'''

            with connection.cursor() as cursor:
                cursor.execute(f'''select count(*)
                                    from ({sql_items}) as s''', [Launch_childs_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id])
                qty, = cursor.fetchone()
                logger.debug(f'qty: {qty}')

                message = [f'<h3>Создание заданий на производство ({qty} товарных позиций) <p/>']
                message.extend([blinkString(f'Запуск № {launch.code} от {DateToStr(launch.date)}', blink=False, bold=True, color='blue') for launch in launch_childs])
                message = '<br/>'.join(message)
                with managed_progress(
                        id=f'order_by_prod_launch_{launch_parent.id}_{user.id}',
                        qty=qty,
                        user=user,
                        message=message,
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:
                    with transaction.atomic():
                        def except_func():
                            settings.LOCKS.release(key)

                        progress.except_func = except_func

                        cursor.execute(sql_items, [Launch_childs_ids, settings.OPERS_TYPES_STACK.ROUTING_TASK.id])
                        rows = cursor.fetchall()
                        for row in rows:
                            item_id, = row

                            route_opers_lunch = []
                            for launch_childs_id in Launch_childs_ids:
                                cursor.execute(sql_items_launch, [launch_childs_id, settings.OPERS_TYPES_STACK.ROUTING_TASK.id, item_id])
                                rows_lunch = cursor.fetchall()
                                for row_lunch in rows_lunch:
                                    row_lunch, = row_lunch
                                    route_opers_lunch.append((row_lunch, launch_childs_id))

                            route_oparation_item = dict(
                                item_id=item_id,
                                launch_ids=Launch_childs_ids,
                                launch_parent_id=launch_parent.id
                            )

                            operationPlanItem = OperationPlanItem(**route_oparation_item)

                            # Головная операция заказа
                            production_order_operation = Operations.objects.create(
                                date=datetime.now(),
                                opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK,
                                status=new_status_order_prod,
                                creator=user,
                                editing=False,
                                deliting=False
                            )
                            logger.debug(f'Created operation :  {production_order_operation}')

                            operation_launches = Operation_launches.objects.create(
                                operation=production_order_operation,
                                launch=launch_parent
                            )
                            logger.debug(f'Created operation_launches :  {operation_launches}')

                            operation_item = Operation_item.objects.create(
                                operation=production_order_operation,
                                item=operationPlanItem.item,
                            )
                            logger.debug(f'Created operation_item :  {operation_item}')

                            for launch_child_id in Launch_childs_ids:
                                for route_oper_lunch in route_opers_lunch:
                                    if route_oper_lunch[1] == launch_child_id:
                                        for item_id in route_oper_lunch[0]:
                                            operation_refs = Operation_refs.objects.create(
                                                child=production_order_operation,
                                                parent_real_id=item_id,
                                                props=Operation_refs.props.product_order_routing
                                            )
                                            logger.debug(f'Created operation_refs :  {operation_refs}')

                            for resources_location_fin in operationPlanItem.resources_location_fin_arr:
                                operation_resources, created = Operation_resources.objects.get_or_create(
                                    operation=production_order_operation,
                                    resource=resources_location_fin[0],
                                    location_fin=resources_location_fin[1]
                                )
                                if created:
                                    logger.debug(f'Created operation_resources :  {operation_resources}')

                            OperationsManager.rec_operations(
                                launch=launch_parent,
                                status=new_status_order_prod_opers,
                                operationPlanItem=operationPlanItem,
                                operation=production_order_operation,
                                opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK,
                                user=user
                            )

                            for launchSumValue in operationPlanItem.launchSumValues.stack:
                                production_order_operation_launch = Operations.objects.create(
                                    date=datetime.now(),
                                    opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK,
                                    status=new_status_order_prod_sum,
                                    creator=user,
                                    editing=False,
                                    deliting=False
                                )
                                logger.debug(f'Created operation :  {production_order_operation}')

                                operation_launches = Operation_launches.objects.create(
                                    operation=production_order_operation_launch,
                                    launch=launchSumValue.launch
                                )
                                logger.debug(f'Created operation_launches :  {operation_launches}')

                                operation_value = Operation_value.objects.create(
                                    operation=production_order_operation_launch,
                                    edizm_id=launchSumValue.edizm_id,
                                    value=launchSumValue.sum_value
                                )
                                logger.debug(f'Created operation_value :  {operation_value}')

                                operation_value = Operation_value.objects.create(
                                    operation=production_order_operation_launch,
                                    edizm_id=launchSumValue.edizm_id,
                                    value=launchSumValue.sum_value1,
                                    props=Operation_value.props.perone
                                )
                                logger.debug(f'Created operation_value :  {operation_value}')

                                operation_refs = Operation_refs.objects.create(
                                    child=production_order_operation_launch,
                                    parent=production_order_operation,
                                    props=Operation_refs.props.product_order_routing
                                )
                                logger.debug(f'Created operation_refs :  {operation_refs}')

                            for location_user in operationPlanItem.locations_users:
                                operation_executor = Operation_executor.objects.create(
                                    operation=production_order_operation,
                                    executor=location_user.user,
                                )
                                logger.debug(f'Created operation_executor :  {operation_executor}')
                                message = f'<h3>Размещен новый заказ на производство ' \
                                          f'№{production_order_operation.num} от {DateTimeToStr(production_order_operation.date, hours=3)}.' \
                                          '<p/>' \
                                          f'{operation_item.item.item_name}' \
                                          '<p/>' \
                                          f'{location_user.location.full_name}' \
                                          '<p/>'

                                operation_executor_stack.push(
                                    Operation_executor_message(executor=location_user.user, message=message),
                                    logger
                                )

                            if progress.step() != 0:
                                settings.LOCKS.release(key)
                                raise ProgressDroped(progress_deleted)

                        launch_parent.status = settings.PROD_OPERS_STACK.IN_PRODUCTION
                        launch_parent.save()

                        for launch_child in launch_childs:
                            launch_child.status = settings.PROD_OPERS_STACK.IN_PRODUCTION
                            launch_child.save()

                        settings.LOCKS.release(key)

                    settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message1(
                        operation_executor_stack=operation_executor_stack,
                        progress=progress,
                    )
        # refresh_mat_view('planing_production_order_mview')
        progress.sendMessage(type='refresh_launches_grid')

    @staticmethod
    def delete_production_order(data):
        from kaf_pas.planing.models.operation_executor import Operation_executor
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.operation_resources import Operation_resources
        from kaf_pas.planing.models.operations_view import Operations_view
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_values import Production_order_valuesManager
        from kaf_pas.production.models.launches import Launches
        from kaf_pas.planing.models.operation_executor import Operation_executor

        user = data.get('user')
        launch_ids = data.get('data')

        if isinstance(user, int):
            user = User.objects.get(id=user)

        operation_executor_stack = Operation_executor_stack()

        launch_cnt = len(launch_ids)
        idx = 0;
        for parent_launch_id in launch_ids:
            parent_launch = Launches.objects.get(id=parent_launch_id)
            key = f'OperationsManager.delete_production_order_{parent_launch.id}'
            settings.LOCKS.acquire(key)

            operations_order_prod = Operations_view.objects.filter(opertype=settings.OPERS_TYPES_STACK.PRODUCTION_TASK, launch=parent_launch)
            with managed_progress(
                    id=f'delete_order_by_prod_launch_{parent_launch.id}_{user.id}',
                    qty=operations_order_prod.count(),
                    user=user,
                    message=f'<h3>Удаление заданий на производство, Запуск № {parent_launch.code} от {DateToStr(parent_launch.date)}</h3>',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                def except_func():
                    settings.LOCKS.release(key)

                progress.except_func = except_func

                with transaction.atomic():
                    logger.debug(f'Операции заданий на производство: {operations_order_prod.count()}')
                    for operation_order_prod in operations_order_prod:
                        # Операции сумм разбивки по запускам/ заказам на продажу
                        operation_sums = Operations_view.objects.filter(parent_id=operation_order_prod.id, opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_SUM_TASK)
                        logger.debug(f'Операции сумм разбивки по запускам/ заказам на продажу: {operation_sums.count()}')
                        for production_sums in operation_sums:
                            qr = Operation_refs.objects.filter(parent_id=operation_order_prod.id, child_id=production_sums.id)
                            logger.debug(f'for delete: {qr.count()}')
                            deleted, _ = qr.delete()

                            qr = Operations.objects.filter(id=production_sums.id)
                            logger.debug(f'for delete: {qr.count()}')
                            deleted, _ = qr.delete()

                        # Техннологические операции
                        operations_det = Production_order_opers.objects.filter(parent_id=operation_order_prod.id, opertype=settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK).order_by('-production_operation_num')
                        logger.debug(f'Техннологические операции: {operations_det.count()}')
                        for operation_det in operations_det:
                            # Выполнение по этим технологическим операциям
                            maked_values =  Operations_view.objects.filter(parent_id=operation_det.id, opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_TASK)
                            logger.debug(f'Выполнение по ({operation_det.production_operation_num}) : {maked_values.count()}')
                            ids = [operation.id for operation in maked_values]
                            if len(ids) > 0:
                                Production_order_valuesManager.delete_sums(ids=ids)

                            qr = Operation_refs.objects.filter(parent_id=operation_order_prod.id, child_id=operation_det.id)
                            logger.debug(f'for delete: {qr.count()}')
                            deleted, _ = qr.delete()

                            qr = Operation_refs.objects.filter(parent__isnull=True, child_id=operation_det.id)
                            logger.debug(f'for delete: {qr.count()}')
                            deleted, _ = qr.delete()

                            qr = Operations.objects.filter(id=operation_det.id)
                            logger.debug(f'for delete: {qr.count()}')
                            deleted, _ = qr.delete()


                        operation_executor_cnt = Operation_executor.objects.filter(operation_id=operation_order_prod.id, props=Operation_executor.props.relevant).count()
                        logger.debug(f'Техннологические operation_executor_cnt: {operation_executor_cnt}')

                        if operation_executor_cnt > 0:
                            user = Operation_executor.objects.filter(operation_id=operation_order_prod.id, props=Operation_executor.props.relevant)[0].executor

                            operation_item = Operation_item.objects.get(operation_id=operation_order_prod.id)
                            operation_resources = Operation_resources.objects.filter(operation_id=operation_order_prod.id).order_by('id')[0]

                            message = blinkString(
                                f'Удаление задания на производство № {operation_order_prod.num} '
                                f'от {DateTimeToStr(operation_order_prod.date, hours=3)}<p/>'
                                f'{operation_item.item.item_name}<p/>'
                                f'{operation_resources.resource.location.full_name}', bold=True, blink=False)

                            operation_executor_stack.push(
                                Operation_executor_message(
                                    executor=user,
                                    message=message
                                ),
                                logger
                            )

                        qr = Operation_refs.objects.filter(parent__isnull=True, child_id=operation_order_prod.id)
                        logger.debug(f'for delete: {qr.count()}')
                        deleted, _ = qr.delete()

                        qr = Operation_refs.objects.filter(parent_id=operation_order_prod.id, child__opertype=settings.OPERS_TYPES_STACK.LAUNCH_TASK)
                        logger.debug(f'for delete: {qr.count()}')
                        deleted, _ = qr.delete()

                        qr = Operations.objects.filter(id=operation_order_prod.id)
                        logger.debug(f'for delete: {qr.count()}')
                        qr.delete()

                        if progress.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

                    for launch in Launches.objects.filter(parent=parent_launch):
                        launch.status = settings.PROD_OPERS_STACK.ROUTMADE
                        launch.save()

                    idx += 1
                    if idx == launch_cnt:
                        Launches.objects.filter(id=parent_launch.id).update(status=settings.PROD_OPERS_STACK.ROUTMADE)
                        # progress.setContentsLabel('Обновление предстваления planing_production_order_mview')

                settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_DELETE.send_message1(
                    operation_executor_stack=operation_executor_stack,
                    progress=progress,

                )

            progress.sendMessage(type='refresh_launches_grid')
            settings.LOCKS.release(key)

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'num': record.num,
            'date': record.date,
            'opertype_id': record.opertype.id,
            'opertype__full_name': record.opertype.full_name,
            'creator__short_name': record.creator.get_short_name,
            'status_id': record.status.id if record.status else None,
            'status__code': record.status.code if record.status else None,
            'status__name': record.status.name if record.status else None,
            'description': record.description,
            'isFolder': False,
        }
        return res

    def get_queryset(self):
        return OperationsQuerySet(self.model, using=self._db)


class Operations(Hierarcy):
    num = CodeStrictField()
    date = DateTimeField()
    creator = ForeignKeyProtect(User)
    opertype = ForeignKeyProtect(Operation_types)
    status = ForeignKeyProtect(Status_operation_types, related_name='planing_Operations_status')
    description = TextField(null=True, blank=True)

    objects = OperationsManager()

    def __str__(self):
        return f"ID:{self.id}, date: {self.date}, description: {self.description},  creator: [{self.creator}], opertype: [{self.opertype}], status: [{self.status}]"

    def __repr__(self):
        return self.__str__()

    def save(self, **kwargs):
        res = super().save(**kwargs)
        OperationsQuerySet._rec_history(self, self.creator)
        return res

    class Meta:
        verbose_name = 'Опреации системные'
