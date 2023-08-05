import logging
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.db import transaction, connection
from django.db.models import DateTimeField, Min, DecimalField
from django.forms import model_to_dict

from isc_common import Stack, Wrapper, setAttr
from isc_common.auth.models.user import User
from isc_common.bit import TurnBitOn
from isc_common.common import new
from isc_common.common.functions import ExecuteStoredProc
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import Hierarcy
from isc_common.models.standard_colors import Standard_colors
from isc_common.number import DelProps, IntToDecimal, DecimalToStr
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.ed_izm import Ed_izm
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operation_value import Operation_value
from kaf_pas.planing.models.operations import OperationsManager, OperationsQuerySet, Operations
from kaf_pas.planing.operation_typesStack import MADE_OPRS_TSK, DETAIL_OPERS_PRD_TSK, RELEASE_TSK_MNS, RELEASE_TSK_PLS

logger = logging.getLogger(__name__)


class Production_orderWrapper(Wrapper):
    color_id = None


class Production_order_valuesQuerySet(OperationsQuerySet):
    pass


class Production_order_valuesManager(OperationsManager):
    def createFromRequest(self, request, removed=None):

        request = DSRequest(request=request)
        data = request.get_data()

        if not isinstance(data.get('childs'), list):
            raise Exception(f'Не выбраны производственные операции(ия).')

        if not isinstance(data.get('parent_id'), int):
            raise Exception(f'Не выбран заказ на производство.')

        if not isinstance(data.get('edizm_id'), int):
            raise Exception(f'Не указана единица измерения.')

        with transaction.atomic():
            res = Production_order_valuesManager.makeAll(
                data=data,
                user=request.user
            )

        return res

    def createBlockFromRequest(self, request, removed=None):

        request = DSRequest(request=request)
        data = request.get_data()

        res = Production_order_valuesManager.blockMakeAll(
            data=data,
            user=request.user
        )

        return res

    @staticmethod
    def blockMakeAll(data, user):
        from kaf_pas.planing.models.production_order import Production_orderQuerySet
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_opers import Production_order_opers

        _res = []
        records = data.get('records')
        if isinstance(records, list):
            with managed_progress(
                    id=f'blockMakeAll_{user.id}',
                    qty=len(records),
                    user=user,
                    message='Внесение данных по выпуску.',
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progress:
                with transaction.atomic():
                    def except_func():
                        settings.LOCKS.release(key)

                    progress.except_func = except_func

                    for record in records:
                        operation = Production_order.objects.get(id=record.get('id'))

                        key = f'''get_setStartStatus_{operation.id}'''
                        settings.LOCKS.acquire(key)
                        _data = dict(
                            id=operation.id,
                            launch_id=operation.launch.id,
                            edizm_id=operation.edizm.id
                        )
                        qty = operation.value_sum

                        if operation.status.id == settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(new).id and operation.cnt_opers == 1:
                            Production_orderQuerySet.start(
                                _data=_data,
                                qty=qty,
                                user=user,
                                lock=False
                            )

                            setAttr(record, 'childs', [model_to_dict(production_order_opers) for production_order_opers in Production_order_opers.objects.filter(parent_id=operation.id)])
                            setAttr(record, 'value', operation.value_sum)

                            res = Production_order_valuesManager.makeAll(
                                data=record,
                                user=user,
                                lock=False
                            )

                            _res.extend(res)

                        if progress.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)
            settings.LOCKS.release(key)
            return _res
        else:
            raise Exception('Не сделан выбор.')

    @staticmethod
    def makeAll(data, user, lock=True):
        from kaf_pas.planing.models.operation_color import Operation_color
        from kaf_pas.planing.models.operation_item import Operation_item
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.models.production_order import Production_order
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.planing.models.operation_resources import Operation_resources

        def rec_item_releases(parent, value, edizm_id, launch_id, warnings, enableMinus, maked_operations, resource_id, location_fin_id=None):
            # Записываем расход комплектующик
            from kaf_pas.production.models.launch_item_prod_order_view import Launch_item_order_view

            for launch_item_order_view in Launch_item_order_view.objects.filter(parent=Operation_item.objects.get(operation_id=parent.id).item).exclude(section='Документация'):
                qty_need = launch_item_order_view.qty_per_one * value
                if qty_need > launch_item_order_view.qty_exists:
                    message = f'Недостаточно комплектации по: {launch_item_order_view.item.item_name}, в наличии {DecimalToStr(launch_item_order_view.qty_exists)} а необходимо {DecimalToStr(qty_need)}'
                    if enableMinus == True:
                        warnings.push(message)
                    else:
                        raise Exception(message)

                release_item_operation = Operations.objects.create(
                    date=datetime.now(),
                    opertype=settings.OPERS_TYPES_STACK.RELEASE_TASK_MINUS,
                    status=settings.OPERS_TYPES_STACK.RELEASE_TASK_MINUS_STATUSES.get('new'),
                    creator=user,
                    editing=False,
                    deliting=False
                )
                logger.debug(f'Created release_item :  {release_item_operation}')
                res.append(model_to_dict(release_item_operation))

                operation_value = Operation_value.objects.create(
                    operation=release_item_operation,
                    value=qty_need,
                    edizm_id=edizm_id,
                    props=Operation_value.props.used_in_release
                )
                logger.debug(f'Created operation_value :  {operation_value}')

                operation_launch = Operation_launches.objects.create(
                    operation=release_item_operation,
                    launch_id=launch_id,
                )
                logger.debug(f'Created operation_launch :  {operation_launch}')

                operation_resource = Operation_resources.objects.create(
                    resource_id=resource_id,
                    location_fin_id=location_fin_id,
                    operation=release_item_operation,
                )
                logger.debug(f'Created operation_resource :  {operation_resource}')

                operation_item = Operation_item.objects.create(
                    operation=release_item_operation,
                    item=launch_item_order_view.item,
                )
                logger.debug(f'Created operation_item :  {operation_item}')

                operation_refs = Operation_refs.objects.create(
                    child=release_item_operation,
                    parent=parent,
                    props=Operation_refs.props.product_making
                )
                logger.debug(f'Created operation_refs :  {operation_refs}')

                if maked_operations.size() > 0:
                    operation_refs = Operation_refs.objects.create(
                        child=release_item_operation,
                        parent=maked_operations.stack[len(maked_operations.stack) - 1].child,
                        props=Operation_refs.props.product_making
                    )
                    logger.debug(f'Created operation_refs :  {operation_refs}')

        def rec_launch_releases(value, edizm_id, item, launch_id, resource_id, location_fin_id, parent, maked_operations, previos_color_id, color_id=None):
            launch_release_operation = Operations.objects.create(
                date=datetime.now(),
                opertype=settings.OPERS_TYPES_STACK.RELEASE_TASK_PLUS,
                status=settings.OPERS_TYPES_STACK.RELEASE_TASK_PLUS_STATUSES.get('new'),
                creator=user,
                editing=False,
                deliting=False
            )
            logger.debug(f'Created release_item :  {launch_release_operation}')
            res.append(model_to_dict(launch_release_operation))

            operation_value = Operation_value.objects.create(
                operation=launch_release_operation,
                value=value,
                edizm_id=edizm_id,
                props=Operation_value.props.used_in_release
            )
            logger.debug(f'Created operation_value :  {operation_value}')

            if launch_id != None:
                operation_launch = Operation_launches.objects.create(
                    operation=launch_release_operation,
                    launch_id=launch_id,
                )
                logger.debug(f'Created operation_launch :  {operation_launch}')

            if item != None:
                operation_item = Operation_item.objects.create(
                    operation=launch_release_operation,
                    item=item,
                )
                logger.debug(f'Created operation_item :  {operation_item}')

            if resource_id:
                operation_resource = Operation_resources.objects.create(
                    resource_id=resource_id,
                    location_fin_id=location_fin_id,
                    operation=launch_release_operation,
                )
                logger.debug(f'Created operation_resource :  {operation_resource}')

            if color_id != None:
                operation_color = Operation_color.objects.create(
                    operation=launch_release_operation,
                    color_id=color_id,
                )
                logger.debug(f'Created operation_color :  {operation_color}')
            else:
                if previos_color_id != None:
                    raise Exception(f'Не указан цвет, который приcутствует в предыдущей операции.')

            if parent != None:
                operation_refs = Operation_refs.objects.create(
                    child=launch_release_operation,
                    parent=parent,
                    props=Operation_refs.props.product_making
                )
                logger.debug(f'Created operation_refs :  {operation_refs}')

            # todo проверяем на полность выполненность
            parent_po = Production_order.objects.get(id=parent.id)
            if parent_po.value_odd == 0:
                parent.status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get('doing')
                parent.save()

            if maked_operations.size() > 0:
                operation_refs = Operation_refs.objects.create(
                    child=launch_release_operation,
                    parent=maked_operations.stack[len(maked_operations.stack) - 1].child,
                    props=Operation_refs.props.product_making
                )
                logger.debug(f'Created operation_refs :  {operation_refs}')

        def rec_operation_made(value, parent, edizm_id, prev_child, color_id=None):
            launch_release_operation = Operations.objects.create(
                date=datetime.now(),
                opertype=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_TASK,
                status=settings.OPERS_TYPES_STACK.MADE_OPERATIONS_STATUSES.get('new'),
                creator=user,
                editing=False,
                deliting=False
            )
            logger.debug(f'Created release_item :  {launch_release_operation}')
            res.append(model_to_dict(launch_release_operation))

            operation_value = Operation_value.objects.create(
                operation=launch_release_operation,
                value=value,
                edizm_id=edizm_id,
                props=Operation_value.props.used_in_release
            )
            logger.debug(f'Created operation_value :  {operation_value}')

            if color_id != None:
                operation_color = Operation_color.objects.create(
                    operation=launch_release_operation,
                    color_id=color_id,
                )
                logger.debug(f'Created operation_color :  {operation_color}')

            operation_refs = Operation_refs.objects.create(
                child=launch_release_operation,
                parent_id=parent.id,
                props=Operation_refs.props.product_making
            )
            logger.debug(f'Created operation_refs :  {operation_refs}')

            if prev_child:
                prev_operation_refs = Operation_refs.objects.create(
                    child=launch_release_operation,
                    parent=prev_child.child if isinstance(prev_child, Operation_refs) else prev_child,
                    props=Operation_refs.props.product_making
                )
                logger.debug(f'Created operation_refs :  {prev_operation_refs}')
            return operation_refs

        # raise Exception('Функция находится в разработке.')

        res = []
        data = Production_orderWrapper(**data)
        if isinstance(data.value, int):
            value = IntToDecimal(data.value)
        elif isinstance(data.value, Decimal):
            value = data.value
        else:
            raise Exception(f'value mast be int or Decimal type.')
        edizm_id = data.edizm_id
        color_id = data.color_id

        operations = [Production_orderWrapper(**child) for child in sorted(data.childs, key=lambda x: x['production_operation_num'])]

        parent = Operations.objects.get(id=Production_order_opers.objects.filter(
            id__in=[child.id for child in operations],
        ).order_by('num')[0].parent_id)

        parent_launch = Operation_launches.objects.get(operation=parent).launch

        item = Operation_item.objects.get(operation=parent).item
        production_order_opers = Production_order_opers.objects.filter(parent_id=parent.id).order_by('-operation_operation_num')[0]
        resource = production_order_opers.resource
        location_fin = production_order_opers.location_fin

        key = f'Production_order_valuesManager.makeAll_{parent.id}'
        if lock:
            settings.LOCKS.acquire(key)
        warnings = Stack()
        enableMinus = settings.ENABLE_MINUS_ODD

        try:
            all_operation_ids = [operation.id for operation in Production_order_opers.objects.filter(parent_id=parent.id)]
            previos_operation = Production_order_values.objects.filter(parent_id__in=all_operation_ids).order_by('-id')
            previos_operation = Operations.objects.get(id=previos_operation[0].id) if previos_operation.count() > 0 else None

            color_query = Operation_color.objects.filter(operation=previos_operation)
            previos_color_id = color_query[0].color.id if color_query.count() > 0 else None

            operation_ids = [operation.id for operation in operations]
            # ========================================Проверяем заполнение предыдущей операции===================================================
            for operation in operations:
                if operation.production_operation_num != 1:
                    value_previos = ExecuteStoredProc('get_previos_operation_value', [parent.id, operation.production_operation_num - 1])
                    value_curent = ExecuteStoredProc('get_previos_operation_value', [parent.id, operation.production_operation_num])
                    value_enabled = value_previos - value_curent
                    if value_enabled < value:
                        if lock:
                            settings.LOCKS.release(key)
                        raise Exception(f'Не достаточно выпуска в предыдущей операции. Возможное количество {DecimalToStr(value_enabled)}')
                break
            # ===================================================================================================================================

            # ========================================Проверяем на выбор сплошного сегмента операций===================================================
            old_num = None
            for operation in operations:
                if old_num != None:
                    if old_num != operation.production_operation_num - 1:
                        if lock:
                            settings.LOCKS.release(key)
                        raise Exception(f'Выбран не сплошной сегмент операций.')
                old_num = operation.production_operation_num
            # ===================================================================================================================================

            # ===============================Проверяем остатки по всем выбраным операциям  чтобы были не меньше вводимой величины==============
            min_value_made = Production_order_opers.objects.filter(parent_id=parent.id, id__in=operation_ids).aggregate(Min('value_odd')).get('value_odd__min')
            if min_value_made < value:
                if lock:
                    settings.LOCKS.release(key)
                raise Exception(f'Превышение количества. Максимально возможное: {DecimalToStr(min_value_made)}')
            else:
                min_value_made = value
            # ===================================================================================================================================

            # ===============================Записываем выполнение выбранных операций =================================================================
            maked_operations = Stack()
            for operation in operations:
                previos_operation = rec_operation_made(
                    parent=operation,
                    color_id=color_id,
                    edizm_id=edizm_id,
                    prev_child=previos_operation,
                    value=min_value_made,
                )
                maked_operations.push(previos_operation)
            # ===================================================================================================================================

            # ==================== Проверяем возможность выпуска релиза ========================================================================
            # min_value_made > 0 можно релизить это количество

            min_value_made = Production_order_opers.objects.filter(parent_id=parent.id).aggregate(Min('value_made')).get('value_made__min')

            value_made = Production_order.objects.filter(id=parent.id).values('value_made').distinct()
            if value_made.count() > 0:
                min_value_made -= value_made[0]

            if min_value_made > 0:

                # ===============================Делаем релизы по операциям уже с учетом вновь занесенных =================================================================
                # ===============================Сначала пробуем если осталось , что зарелизить по заказам на продажу ===============================
                qty_released = 0
                # launch_id = operation.launch_id

                with connection.cursor() as cursor:
                    cursor.execute('''select distinct prdl.id, prdl.priority, sd.date_sign, sd.date
                                        from sales_demand as sd
                                                 join production_launches prdl on sd.id = prdl.demand_id
                                                 join planing_operation_launches polc on prdl.id = polc.launch_id
                                                join planing_operation_item poit on poit.operation_id = polc.operation_id
                                        where prdl.parent_id = %s
                                        and poit.item_id = %s
                                        order by prdl.priority, sd.date_sign, sd.date''', [parent_launch.id, item.id])
                    rows = cursor.fetchall()
                    for row in rows:
                        id, _, _, _ = row

                        value_odd = Production_order_per_launch.objects.get(id=parent.id, launch_id=id).value_odd

                        if value_odd > 0:
                            if min_value_made > value_odd:
                                value = value_odd
                                min_value_made -= value_odd
                            else:
                                value = min_value_made
                                min_value_made = 0

                            rec_launch_releases(
                                color_id=color_id,
                                edizm_id=edizm_id,
                                item=item,
                                launch_id=id,
                                parent=parent,
                                resource_id=resource.id,
                                location_fin_id=location_fin.id if location_fin else None,
                                value=value,
                                previos_color_id=previos_color_id,
                                maked_operations=maked_operations,
                            )

                            qty_released += value

                            if min_value_made == 0:
                                break

                if min_value_made > 0:
                    rec_launch_releases(
                        color_id=color_id,
                        edizm_id=edizm_id,
                        item=item,
                        launch_id=parent_launch.id,
                        resource_id=resource.id,
                        location_fin_id=location_fin.id if location_fin else None,
                        parent=parent,
                        value=min_value_made,
                        previos_color_id=previos_color_id,
                        maked_operations=maked_operations,
                    )

                    qty_released += min_value_made

                if qty_released > 0:

                    # ===== Связываем операции которые учавствовали в образовании релиза, чтобы потом если удалять то все сразу и релиз в том числе
                    main_opers = maked_operations.stack[maked_operations.size() - 1]
                    for operation in maked_operations.stack:
                        if operation.child.id == main_opers.child.id:
                            break
                        operation_refs = Operation_refs.objects.create(
                            child_id=operation.child.id,
                            parent_id=main_opers.child.id,
                            props=Operation_refs.props.product_making_block
                        )
                        logger.debug(f'Created operation_refs :  {operation_refs}')

                    rec_item_releases(
                        edizm_id=edizm_id,
                        enableMinus=enableMinus,
                        launch_id=parent_launch.id,
                        resource_id=resource.id,
                        # location_fin_id=location_fin.id if location_fin else None,
                        parent=parent,
                        value=qty_released,
                        warnings=warnings,
                        maked_operations=maked_operations,
                    )

                    if warnings.size() > 0:
                        if not enableMinus:
                            raise Exception('\n'.join(warnings.stack))
                        else:
                            WebSocket.send_warning_message(
                                host=settings.WS_HOST,
                                port=settings.WS_PORT,
                                channel=f'common_{user.username}',
                                message='<br/><br/>'.join(warnings.stack),
                                logger=logger
                            )

                # TODO Отмечаем блоковый заказ и дочерние заказы если все операции в них выполнены
                # for to_close_Launches in Launches_view.objects.filter(parent_id=launch_id).exclude(status=settings.PROD_OPERS_STACK.CLOSED):
                #     qty_made = ExecuteStoredProc('get_operations_launch_sum', [parent.id, 'RELEASE_TSK_PLS', 'is_bit_on(planing_operation_value.props, 0) = false', to_close_Launches.id])
                #     if to_close_Launches.qty - qty_made == 0:
                #         Launches.objects.filter(id=to_close_Launches.id).update(status=settings.PROD_OPERS_STACK.CLOSED)
                #
                # if Launches_view.objects.filter(parent_id=launch_id).exclude(status=settings.PROD_OPERS_STACK.CLOSED).count() == 0:
                #     Launches.objects.filter(id=parent.id).update(status=settings.PROD_OPERS_STACK.CLOSED)
        except Exception as ex:
            if lock:
                settings.LOCKS.release(key)
            raise ex

        if lock:
            settings.LOCKS.release(key)
        return res

    @staticmethod
    def delete_sums(ids):
        from kaf_pas.planing.models.operations import Operations
        from kaf_pas.planing.models.operation_refs import Operation_refs
        res = 0

        if not isinstance(ids, list):
            raise Exception(f'ids must be list.')

        for operation in Operations.objects.select_for_update().filter(id__in=ids).order_by('id'):
            for id in ids:

                release_query = Operation_refs.objects.filter(parent_id=id, child__opertype__code__in=[RELEASE_TSK_PLS, RELEASE_TSK_MNS])
                if release_query.count() == 0:
                    res, _ = Operation_refs.objects.filter(child_id=id, parent__opertype__code__in=[MADE_OPRS_TSK, DETAIL_OPERS_PRD_TSK]).delete()
                else:
                    # Удаляем релизы если они есть
                    for operation_refs in release_query:
                        child = operation_refs.child
                        for item in Operation_refs.objects.filter(child=child):
                            logger.debug(item)
                            deleted, _ = item.delete()
                        logger.debug(child)
                        res, _ = child.delete()

                    # Удаляем блок учавствующий в релизе
                    for operation_refs in Operation_refs.objects.filter(parent_id=id, props=Operation_refs.props.product_making_block, parent__opertype__code=MADE_OPRS_TSK):
                        op = operation_refs.child
                        logger.debug(op)
                        for otrf in Operation_refs.objects.filter(child=op):
                            logger.debug(otrf)
                            otrf.delete()
                        for otrf in Operation_refs.objects.filter(parent=op):
                            logger.debug(otrf)
                            otrf.delete()
                        op.delete()

                    for otrf in Operation_refs.objects.filter(child_id=id):
                        logger.debug(otrf)
                        otrf.delete()

                    for otrf in Operation_refs.objects.filter(parent_id=id):
                        logger.debug(otrf)
                        otrf.delete()

                res, _ = Operations.objects.filter(id=id).delete()

    def deleteFromRequest(self, request, removed=None):

        request = DSRequest(request=request)
        res = 0

        data = request.get_data()
        _transaction = data.get('transaction')
        ids = []
        if _transaction != None:
            operations = _transaction.get('operations')
            ids = [item.get('data').get('id') for item in operations]
        else:
            ids.append(data.get('id'))

        with transaction.atomic():
            Production_order_valuesManager.delete_sums(ids=ids)

        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'color__color': record.color.color if record.color else None,
            'color__name': record.color.name if record.color else None,
            'color_id': record.color.id if record.color else None,
            'creator__short_name': record.creator.get_short_name,
            'creator_id': record.creator.id,
            'date': record.date,
            'edizm__name': record.edizm.name,
            'edizm_id': record.edizm.id,
            'value': DecimalToStr(record.value),
        }
        return DelProps(res)

    def get_queryset(self):
        return Production_order_valuesQuerySet(self.model, using=self._db)


class Production_order_values(Hierarcy):
    color = ForeignKeyProtect(Standard_colors, null=True, blank=True)
    opertype = ForeignKeyProtect(Operation_types)
    creator = ForeignKeyProtect(User, default=None)
    edizm = ForeignKeyProtect(Ed_izm, default=None)
    date = DateTimeField(default=None)
    value = DecimalField(decimal_places=4, max_digits=19)

    objects = Production_order_valuesManager()

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'planing_operations_values_view'
        verbose_name = 'Списания'
