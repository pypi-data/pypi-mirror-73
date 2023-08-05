import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction, connection
from django.db.models import DateTimeField, PositiveIntegerField, DecimalField

from isc_common import setAttr, Stack
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.common.functions import ExecuteStoredProc
from isc_common.datetime import DateToStr, StrToDate, DateTimeToStr
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefManager, BaseRefQuerySet
from isc_common.number import StrToNumber, DelProps
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.production.models.status_launch import Status_launch
from kaf_pas.sales.models.demand import Demand
from kaf_pas.sales.models.demand_view import Demand_view

logger = logging.getLogger(__name__)
logger_timing = logging.getLogger(f'{__name__}_timing')


class LaunchesQuerySet(BaseRefQuerySet):
    pass


class LaunchesManager(BaseRefManager):

    @staticmethod
    def props():
        return BitField(flags=(
            ('addload', 'запуск в несколько приемов'),
        ), default=0, db_index=True)

    @staticmethod
    def _getQtyChilds(records):
        from kaf_pas.ckk.models.item_qty import Item_qty

        res = 0
        if isinstance(records, list):
            with connection.cursor() as cursor:
                for record in records:
                    sql_str = f'''WITH RECURSIVE r AS (
                                                        SELECT *, 1 AS level
                                                        FROM production_launch_item_refs
                                                        WHERE parent_id IN (%s)

                                                        union all

                                                        SELECT production_launch_item_refs.*, r.level + 1 AS level
                                                        FROM production_launch_item_refs
                                                                 JOIN r
                                                                      ON production_launch_item_refs.parent_id = r.child_id)

                                                    select  count(*)
                                                    from r where launch_id = %s'''

                    cursor.execute(sql_str, [record.get('id'), record.get('launch_id')])
                    qty, = cursor.fetchone()
                    res += qty
                    Item_qty.objects.create(
                        child_id=record.get('id'),
                        parent_id=record.get('parent_id'),
                        qty=qty
                    )
        return dict(qty=res)

    def getQtyChilds(self, request):

        request = DSRequest(request=request)
        data = request.get_data()
        if isinstance(data, dict):
            records = data.get('records')
            if isinstance(records, list):
                return LaunchesManager._getQtyChilds(records=records)

    @staticmethod
    def get_count(item_line, qty, level, get_full_path, get_full_path_obj, items_refs_qty_stack):
        from kaf_pas.ckk.models.attr_type import Attr_type

        key = 'LaunchesManager.get_count'
        settings.LOCKS.acquire(key)
        SPC_CLM_COUNT_ATTR, _ = Attr_type.objects.get_or_create(code='SPC_CLM_COUNT')
        from kaf_pas.kd.models.document_attributes import Document_attributes

        res = None
        if items_refs_qty_stack.size() > 0:
            qty = items_refs_qty_stack.find_one(lambda x: x[0] == level - 1 and x[1] == get_full_path_obj[level - 1].get('id'))[2]

        if level == 1:
            res, _ = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(qty), value_int=qty)
            settings.LOCKS.release(key)
            return res

        _str = item_line.SPC_CLM_COUNT.value_str if item_line.SPC_CLM_COUNT else None
        if _str == 'null':
            _str = None

        if _str != None:
            if _str.find(',') != -1:
                try:
                    str1 = _str.replace(',', '.')
                    count = StrToNumber(str1)

                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str1)
                    if created == False:
                        SPC_CLM_COUNT.value_int = count
                        SPC_CLM_COUNT.value_str = str1
                        SPC_CLM_COUNT.save()

                    if qty > 1:
                        count *= qty
                        SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(count))
                        if created != True:
                            SPC_CLM_COUNT.value_int = count
                            SPC_CLM_COUNT.save()

                    res = SPC_CLM_COUNT
                except ValueError:
                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str='1')
                    if created == True:
                        SPC_CLM_COUNT.value_int = 1
                        SPC_CLM_COUNT.save()

            else:
                try:
                    count = StrToNumber(_str)
                    if qty > 1:
                        count *= qty
                        SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(count))
                        if created == True:
                            SPC_CLM_COUNT.value_int = count
                            SPC_CLM_COUNT.save()
                        res = SPC_CLM_COUNT
                    else:
                        res = item_line.SPC_CLM_COUNT
                except ValueError:
                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str='1')
                    if created == True:
                        SPC_CLM_COUNT.value_int = 1
                        SPC_CLM_COUNT.save()

        else:
            res = item_line.SPC_CLM_COUNT

        if res == None and item_line.section != 'Документация':
            raise Exception(blinkString(f'Для: {get_full_path} count == 0', color='red', bold=True, blink=False))

        settings.LOCKS.release(key)
        return res

    @staticmethod
    def make_launch(data, mode='add'):
        logger.debug(f'make_launch data: {data}')

        from isc_common.auth.models.user import User
        from kaf_pas.ckk.models.ed_izm import Ed_izm
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.production.models import p_id
        from kaf_pas.production.models.launch_item_line import Launch_item_line
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.production.models.launch_operation_attr import Launch_operation_attr
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item
        from kaf_pas.production.models.operation_attr import Operation_attr
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.ready_2_launch import Item_refs_Stack

        # raise Exception(f'Функция находится на разработке.')
        id = data.get('id')
        demands = data.get('demand')

        description = data.get('description')
        date = data.get('date')
        date = StrToDate(date)
        user = User.objects.get(id=data.get('user_id'))
        status = settings.PROD_OPERS_STACK.FORMIROVANIE
        status_demand_launched = settings.PROD_OPERS_STACK.DEMAND_LAUNCHED

        edizm_shtuka = Ed_izm.objects.get(code='шт')

        parentlaunch = None

        if isinstance(demands, list):
            for demand_id in demands:
                demand = Demand_view.objects.get(id=demand_id)
                # if demand.qty_for_launch == None or demand.qty_for_launch == 0:
                #     raise Exception(f'Не указано количестово для запуска заказа № {demand.code} от {DateToStr(demand.date, hours=3)}')
                # elif demand.qty_for_launch > demand.tail_qty:
                #     raise Exception(f'Затребован болшее количество ({demand.qty_for_launch}) количестово для запуска заказа № {demand.code} от {DateToStr(demand.date, hours=3)}, чем имеется в наличии ({demand.tail_qty})')

                if demand.qty > demand.tail_qty:
                    raise Exception(f'Затребовано болшее количество ({demand.qty}) имеется для запуска заказа № {demand.code} от {DateToStr(demand.date, hours=3)}, чем имеется в наличии ({demand.tail_qty})')

        # launch_item_lines = Stack()
        # launch_operations_materials = Stack()
        # launch_operation_resources = Stack()

        if isinstance(demands, list):
            for demand_id in demands:
                key = 'LaunchesManager.make_launch_{demand_id}'
                settings.LOCKS.acquire(key)
                for demand in Demand.objects.filter(id=demand_id):
                    if demand.status.code != 'otkryt':
                        demand_view = Demand_view.objects.get(id=demand.id)
                        if demand_view.launch_qty == 0:
                            demand.status = settings.PROD_OPERS_STACK.DEMAND_OTKR
                            demand.save()
                        else:
                            settings.LOCKS.release(key)
                            raise Exception(f'Заказ № {demand.code} от {DateTimeToStr(demand.date)} не может быть запущен, т.к. находится в состоянии "{demand.status.name}"')

                    if mode == 'update':
                        item_query = Launches.objects.filter(demand__precent_item__item=demand.precent_item.item, status__code='formirovanie')
                        item_count = item_query.count()
                        if item_count > 0:
                            raise Exception(f'{demand.precent_item.item.item_name} уже включен в данный запуск.')

                    cnt = Launches.objects.filter(demand=demand).count() + 1
                    child_code = f'{demand.code}/{cnt}'

                    where_clause = f'where is_bit_on(props::integer, 0) = true and is_bit_on(props::integer, 1) = true and parent_id != {p_id}'
                    cntAll = Item_refs.objects.get_descendants_count(
                        id=demand.precent_item.item.id,
                        where_clause=where_clause,
                        # fields='child_id, parent_id'
                        # distinct='distinct'
                    )

                    logger.debug(f'cntAll: {cntAll}')
                    first_step = True

                    def get_template(date):
                        return DateToStr(date, '%Y / %m')

                    if mode == 'add':
                        code = get_template(date)
                        num = len([code for code in [get_template(launch.date) for launch in Launches.objects.filter(parent__isnull=True)] if code == code]) + 1
                        code = f'''{code} / {num}'''
                    elif mode == 'update':
                        parentlaunch = Launches.objects.get(id=id)
                        code = parentlaunch.code

                    with managed_progress(
                            id=f'demand_{demand.id}_{user.id}',
                            qty=cntAll,
                            user=user.id,
                            message=blinkString(f'Формирование производственной спецификации: Запуск № {code}, Заказ № {demand.code} от {DateToStr(demand.date)} ({cntAll} товарных позиций.)', bold=True, blink=False),
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                            # props=TurnBitOn(0, 1) #Без WebSocket progressbar a
                    ) as progress:
                        with transaction.atomic():
                            def except_func():
                                settings.LOCKS.release(key)

                            progress.except_func = except_func

                            # qty = demand.qty_for_launch
                            qty = demand.qty

                            if mode == 'add':
                                if parentlaunch == None:
                                    parentlaunch = Launches.objects.create(
                                        date=date,
                                        code=code,
                                        description=description,
                                        status=status
                                    )

                            launch = Launches.objects.create(
                                parent=parentlaunch,
                                code=child_code,
                                date=date,
                                demand_id=demand_id,
                                description=description,
                                qty=qty,
                                status=status
                            )

                            items_refs_stack = Item_refs_Stack()
                            items_refs_qty_stack = Stack()
                            items_refs_stack.add_parents(id=demand.precent_item.item.id)

                            item_ref_query = Item_refs.objects.get_descendants(
                                id=demand.precent_item.item.id,
                                where_clause=where_clause
                            )

                            for item_ref in item_ref_query:
                                if ~item_ref.props.used:
                                    settings.LOCKS.release(key)
                                    continue

                                items_refs_stack.push(item_ref)

                                try:
                                    item_line = Item_line.objects.get(parent=item_ref.parent, child=item_ref.child)
                                except Item_line.DoesNotExist:
                                    settings.LOCKS.release(key)
                                    raise Exception(blinkString(text=f'Для : PARENT_ID: {item_ref.parent.id if item_ref.parent else None} CHILD_ID: {item_ref.child.id} {items_refs_stack.get_full_path} не найдена строка детализации.', bold=True, blink=False))

                                count = LaunchesManager.get_count(
                                    item_line=item_line,
                                    qty=demand.qty,
                                    level=item_ref.level,
                                    get_full_path=items_refs_stack.get_full_path,
                                    get_full_path_obj=items_refs_stack.get_full_path_obj,
                                    items_refs_qty_stack=items_refs_qty_stack
                                )

                                _count_per_one = StrToNumber(item_line.SPC_CLM_COUNT.value_str) if count and item_line.section != 'Документация' else 0
                                _count = StrToNumber(count.value_str) if count and item_line.section != 'Документация' else 0

                                if items_refs_qty_stack.exists(lambda x: x[0] == item_ref.level and x[1] == item_ref.child.id) == False:
                                    items_refs_qty_stack.push((item_ref.level, item_ref.child.id, _count))

                                # start_time = time.clock()
                                launch_item_refs, created = Launch_item_refs.objects.get_or_create(
                                    child=item_ref.child,
                                    parent=item_ref.parent if item_ref.level != 1 else None,
                                    launch=launch,
                                    qty=_count,
                                    qty_per_one=_count_per_one,
                                    defaults=dict(
                                        item_refs=item_ref,
                                        item_full_name=items_refs_stack.get_full_path,
                                        item_full_name_obj=items_refs_stack.get_full_path_obj
                                    )
                                )

                                if created:
                                    logger.debug(f'Created: {created} launch_item_refs :  {launch_item_refs}')
                                    # logger_timing.debug(f'launch_item_refs Time: {time.clock() - start_time}')
                                else:
                                    launch_item_refs.replication_factor += 1
                                    launch_item_refs.save()
                                    logger.warning(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!! Not Created: {created} launch_item_refs :  {launch_item_refs} !!!!!!!!!!!!!!!!!!!!!!!')

                                    # start_time = time.clock()

                                edizm = item_line.edizm if item_line.edizm else edizm_shtuka

                                launch_item_line, created = Launch_item_line.objects.get_or_create(
                                    child=item_line.child,
                                    parent=item_line.parent,
                                    item_line=item_line,
                                    launch=launch,

                                    SPC_CLM_FORMAT=item_line.SPC_CLM_FORMAT,
                                    SPC_CLM_ZONE=item_line.SPC_CLM_ZONE,
                                    SPC_CLM_POS=item_line.SPC_CLM_POS,
                                    SPC_CLM_MARK=item_line.SPC_CLM_MARK,
                                    SPC_CLM_NAME=item_line.SPC_CLM_NAME,
                                    SPC_CLM_COUNT=count,
                                    SPC_CLM_NOTE=item_line.SPC_CLM_NOTE,
                                    SPC_CLM_MASSA=item_line.SPC_CLM_MASSA,
                                    SPC_CLM_MATERIAL=item_line.SPC_CLM_MATERIAL,
                                    SPC_CLM_USER=item_line.SPC_CLM_USER,
                                    SPC_CLM_KOD=item_line.SPC_CLM_KOD,
                                    SPC_CLM_FACTORY=item_line.SPC_CLM_FACTORY,
                                    edizm=edizm,
                                    section=item_line.section,
                                    section_num=item_line.section_num,
                                    subsection=item_line.subsection,
                                )

                                if created:
                                    logger.debug(f'Created : launch_item_line :  {launch_item_line}')
                                else:
                                    logger.warning(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!! Not Created: {created} launch_item_line :  {launch_item_line} !!!!!!!!!!!!!!!!!!!!!!!')

                                # logger_timing.debug(f'launch_item_line Time: {time.clock() - start_time}')

                                def rec_operations_data(item, item_ref, launch_item_line, get_full_path):
                                    # start_time = time.clock()
                                    cnt = Operations_item.objects.filter(item=item).count()
                                    # logger_timing.debug(f'Operations_item.objects.filter Time: {time.clock() - start_time}')
                                    if cnt == 0:
                                        if item_line.section != 'Документация':
                                            settings.LOCKS.release(key)
                                            raise Exception(blinkString(text=f'Для : ID: {item.id} {get_full_path} не найдена операция.', bold=True, blink=False))
                                    else:
                                        section = launch_item_line.section

                                        if first_step == True and section and section == 'Документация':
                                            settings.LOCKS.release(key)
                                            raise Exception(blinkString(text=f'Изделие : ID: {item.id} {get_full_path} должно входить как сборочная еденица.', bold=True, blink=False))

                                        if section and section != 'Документация':
                                            operations_item_query = Operations_item.objects.filter(item=item)

                                            for operations_item in operations_item_query:
                                                # start_time = time.clock()
                                                launch_operations_item, created = Launch_operations_item.objects.get_or_create(
                                                    item=operations_item.item,
                                                    launch=launch,
                                                    num=operations_item.num,
                                                    operation=operations_item.operation,
                                                    defaults=dict(
                                                        description=operations_item.description,
                                                        ed_izm=operations_item.ed_izm,
                                                        operationitem=operations_item,
                                                        qty=operations_item.qty,
                                                    )
                                                )

                                                for operation_attr in Operation_attr.objects.filter(operation=operations_item.operation):
                                                    Launch_operation_attr.objects.get_or_create(
                                                        operation=launch_operations_item.operation,
                                                        launch=launch,
                                                        attr_type=operation_attr.attr_type
                                                    )

                                                if created:
                                                    logger.debug(f'Created: {created} launch_operations_item :  {launch_operations_item}')
                                                    # logger_timing.debug(f'launch_operations_item Time: {time.clock() - start_time}')

                                                    operation_material_query = Operation_material.objects.filter(operationitem=operations_item)

                                                    for operation_material in operation_material_query:
                                                        # start_time = time.clock()
                                                        # 'launch_operationitem', 'material', 'material_askon'
                                                        if operation_material.material != None or operation_material.material_askon != None:
                                                            launch_operations_material, created = Launch_operations_material.objects.get_or_create(
                                                                launch_operationitem=launch_operations_item,
                                                                material=operation_material.material,
                                                                material_askon=operation_material.material_askon,
                                                                defaults=dict(
                                                                    operation_material=operation_material,
                                                                    edizm=operation_material.edizm,
                                                                    qty=operation_material.qty,
                                                                )
                                                            )
                                                            # launch_operations_materials.push(launch_operations_material)
                                                            if created:
                                                                logger.debug(f'Created: launch_operations_material :  {launch_operations_material}')
                                                            else:
                                                                logger.warning(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!! Not Created: {created} launch_operations_material :  {launch_operations_material} !!!!!!!!!!!!!!!!!!!!!!!')
                                                                # logger_timing.debug(f'launch_operations_material Time: {time.clock() - start_time}')

                                                    def exception_not_location():
                                                        settings.LOCKS.release(key)
                                                        raise Exception(f'''<b>Для : {items_refs_stack.get_full_path}</b>  {blinkString(text='не задано местоположение. Запустите анализатор готовности к запуску.', blink=False, color='red', bold=True)}''')

                                                    operation_resources_query = Operation_resources.objects.filter(operationitem=operations_item)

                                                    if operation_resources_query.count() == 0:
                                                        exception_not_location()

                                                    for operation_resources in operation_resources_query:
                                                        if operation_resources.location == None:
                                                            exception_not_location()

                                                        if operation_resources.resource == None:
                                                            # start_time = time.clock()
                                                            operation_resources.resource, created = settings.OPERS_STACK.NOT_UNDEFINED_WORKSHOP(operation_resources.location)
                                                            # logger.debug(f'Created : {created} operation_resources.resource :  {operation_resources.resource}')
                                                            # logger_timing.debug(f'Resource.objects.get_or_create Time: {time.clock() - start_time}')

                                                        # start_time = time.clock()
                                                        # 'launch_operationitem', 'location', 'resource'
                                                        launch_operation_resource, created = Launch_operation_resources.objects.get_or_create(
                                                            launch_operationitem=launch_operations_item,
                                                            resource=operation_resources.resource,
                                                            location=operation_resources.location,
                                                            location_fin=operation_resources.location_fin,
                                                            defaults=dict(
                                                                operation_resources=operation_resources,
                                                                batch_size=operation_resources.batch_size,
                                                            )
                                                        )
                                                        # launch_operation_resources.push(launch_operation_resource)
                                                        if created:
                                                            logger.debug(f'Created: launch_operation_resources.resource :  {launch_operation_resource}')
                                                        else:
                                                            logger.warning(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!! Not Created: {created} launch_operation_resources :  {launch_operation_resource} !!!!!!!!!!!!!!!!!!!!!!!')
                                                            # logger_timing.debug(f'Launch_operation_resources.objects.get_or_create Time: {time.clock() - start_time}')
                                                else:
                                                    logger.debug(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!! Not Created: {created} launch_item_refs :  {launch_operations_item} !!!!!!!!!!!!!!!!!!!!!!!')

                                if item_ref.parent:
                                    if first_step == False:
                                        rec_operations_data(item=item_ref.parent, item_ref=item_ref, launch_item_line=launch_item_line, get_full_path=items_refs_stack.get_full_path)
                                rec_operations_data(item=item_ref.child, item_ref=item_ref, launch_item_line=launch_item_line, get_full_path=items_refs_stack.get_full_path)
                                first_step = False

                                if progress.step() != 0:
                                    settings.LOCKS.release(key)
                                    raise ProgressDroped(progress_deleted)

                            # demand.qty_for_launch = 0
                            # Launch_item_line.objects.bulk_create(launch_item_lines.stack)
                            # Launch_operations_material.objects.bulk_create(launch_operations_materials.stack)
                            # Launch_operation_resources.objects.bulk_create(launch_operation_resources)

                            demand.status = status_demand_launched
                            demand.save()
                            settings.LOCKS.release(key)
                        # end_time = time.clock()
                        # logger_timing.debug(f'End Time: {end_time}')
                        # logger_timing.debug(f'Total Time: {end_time - start_time}')

                        settings.EVENT_STACK.EVENTS_PRODUCTION_MAKE_LAUNCH.send_message(message=f'Выполнено формирование запуска  <h3>{launch.code} от {launch.date}</h3><p/>')

        return data

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'user_id', request.user_id)
        return LaunchesManager.make_launch(data)

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'user_id', request.user_id)
        return LaunchesManager.make_launch(data, 'update')

    def reCreateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'user_id', request.user_id)
        return LaunchesManager.update_launch(data)

    def deleteFromRequest(self, request, removed=None, ):
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operations import OperationsManager
        from kaf_pas.production.models.launch_item_line import Launch_item_line
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item
        import time

        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_tuple_ids()
        status_demand_otkr = settings.PROD_OPERS_STACK.DEMAND_OTKR

        for id, mode in tuple_ids:
            if mode == 'hide':
                super().filter(id=id).soft_delete()
            else:
                launches = Launches.objects.filter(parent_id=id)

                if launches.count() == 0:
                    launches = Launches.objects.filter(id=id)

                for launch in launches:
                    key = f'Delete_launch_{launch.id}'
                    settings.LOCKS.acquire(key)
                    query = Launch_operations_item.objects.filter(launch=launch.id)

                    with managed_progress(
                            id=f'launch_{id}_{request.user_id}',
                            qty=query.count(),
                            user=request.user_id,
                            message=f'<h3>Удаление запуска: № {launch.code} от {DateToStr(launch.date)}</h3>',
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                    ) as progress:
                        with transaction.atomic():
                            def except_func():
                                settings.LOCKS.release(key)

                            progress.except_func = except_func

                            qty, _ = Launch_item_refs.objects.filter(launch_id=launch.id).delete()
                            qty1, _ = Launch_item_line.objects.filter(launch_id=launch.id).delete()
                            qty += qty1

                            for launch_operations_item in query:
                                qty1, _ = Launch_operations_material.objects.filter(launch_operationitem=launch_operations_item).delete()
                                qty += qty1
                                qty1, _ = Launch_operation_resources.objects.filter(launch_operationitem=launch_operations_item).delete()
                                qty += qty1
                                launch_operations_item.delete()
                                qty += 1

                                opers_qty = Operation_launches.objects.filter(launch_id=launch.id).count()
                                if opers_qty > 0:
                                    with managed_progress(
                                            id=f'opers_launch_{launch.id}_{request.user_id}',
                                            qty=opers_qty,
                                            user=request.user_id,
                                            message=f'<h3>Удаление оперций запуска</h3>',
                                            title='Выполнено',
                                            # props=TurnBitOn(0, 0)
                                    ) as progress_opers:
                                        for operation_launches in Operation_launches.objects.filter(launch_id=launch.id):
                                            OperationsManager.delete_recursive(operation=operation_launches.operation, user=request.user)
                                            operation_launches.operation.delete()
                                            progress_opers.step()

                                if progress.step() != 0:
                                    settings.LOCKS.release(key)
                                    raise ProgressDroped(progress_deleted)

                            # qty1, _ = super().filter(id=launch.id).delete()

                            if launch.demand != None:
                                launch.demand.status = status_demand_otkr
                                launch.demand.save()

                            launch.delete()

                            if Launches.objects.filter(parent_id=id).count() == 0:
                                for operation_launches in Operation_launches.objects.filter(launch_id=id, operation__opertype_id__in=[settings.OPERS_TYPES_STACK.LAUNCH_TASK.id]):
                                    ExecuteStoredProc("delete_operation", [operation_launches.operation.id])

                                Operation_launches.objects.filter(launch_id=id).delete()
                                Launches.objects.filter(id=id).delete()

                            settings.EVENT_STACK.EVENTS_PRODUCTION_DELETE_LAUNCH.send_message(f'Выполнено удаление запуска  <h3>{launch.code} от {launch.date}</h3><p/>')
                            settings.LOCKS.release(key)
                        time.sleep(1)

                    res += qty + qty1

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'date': record.date,
            'description': record.description,
            'parent_id': record.parent.id if record.parent else None,

            'demand_id': record.demand.id,
            'demand__code': record.demand.code,
            'demand__date': record.demand.date,

            'status_id': record.status.id,
            'status__code': record.status.code,
            'status__name': record.status.name,

            'qty': record.qty,
            'priority': record.priority,
            'routing_made': record.props.routing_made,
            # 'props': record.props,

            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return LaunchesQuerySet(self.model, using=self._db)


class Launches(BaseRefHierarcy):
    # props = LaunchesManager.props()
    date = DateTimeField(db_index=True)
    demand = ForeignKeyProtect(Demand, null=True, blank=True)
    priority = PositiveIntegerField(db_index=True, default=0)
    qty = DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    status = ForeignKeyProtect(Status_launch)

    objects = LaunchesManager()

    def up_priority(self):
        Demand.objects.filter()

    def __str__(self):
        return f"ID:{self.id}, " \
               f"code: {self.code}, " \
               f"name: {self.name}, " \
               f"description: {self.description}, " \
               f"date: {self.date}, " \
               f"status: [{self.status}], " \
               f"demand: [{self.demand}], " \
               f"qty: {self.qty}"

    class Meta:
        verbose_name = 'Запуски'
