import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from django.db.models import TextField
from django.forms import model_to_dict

from isc_common import delAttr, setAttr, Stack
from isc_common.auth.models.user import User
from isc_common.bit import IsBitOn, TurnBitOn
from isc_common.datetime import DateToStr, manth_name
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps
from isc_common.progress import managed_progress, ProgressDroped, progress_deleted
from kaf_pas.ckk.models.item_line import Item_line
from kaf_pas.ckk.models.item_refs import Item_refs
from kaf_pas.production.models import p_id
from kaf_pas.production.models.operation_material import Operation_material
from kaf_pas.production.models.operation_resources import Operation_resources
from kaf_pas.production.models.operations_item import Operations_item
from kaf_pas.sales.models.demand import Demand

logger = logging.getLogger(__name__)


class Ready_2_launchQuerySet(AuditQuerySet):
    pass

    def get_info(self, request, *args):
        request = DSRequest(request=request)
        request = Ready_2_launchManager._del_options(request)
        criteria = self.get_criteria(json=request.json)
        cnt = super().filter(*args, criteria).count()
        cnt_all = super().filter().count()
        return dict(qty_rows=cnt, all_rows=cnt_all)

    def get_range_rows1(self, request, function=None, distinct_field_names=None):
        request = DSRequest(request=request)
        request = Ready_2_launchManager._del_options(request)
        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(start=request.startRow, end=request.endRow, function=function, distinct_field_names=distinct_field_names, json=request.json)
        return res


class Item_refs_Stack(Stack):
    def add_parents(self, id, launch_id=None):

        if launch_id == None:
            for item_ref in Item_refs.objects.raw(f'''WITH RECURSIVE r AS (
                                                        SELECT *, 1 AS level
                                                        FROM ckk_item_refs
                                                        WHERE child_id IN (%s)
                                                        and parent_id != %s
    
                                                        union all
    
                                                        SELECT ckk_item_refs.*, r.level + 1 AS level
                                                        FROM ckk_item_refs
                                                                 JOIN r
                                                                      ON ckk_item_refs.child_id = r.parent_id)
    
                                                    select  *
                                                    from r
                                                    where child_id != %s order by level desc''', [
                id,
                p_id,
                p_id
            ]):
                self.push(item_ref)
        else:
            for item_ref in Item_refs.objects.raw(f'''WITH RECURSIVE r AS (
                                                        SELECT *, 1 AS level
                                                        FROM production_launch_item_refs
                                                        WHERE child_id IN (%s)

                                                        union all

                                                        SELECT production_launch_item_refs.*, r.level + 1 AS level
                                                        FROM production_launch_item_refs
                                                                 JOIN r
                                                                      ON production_launch_item_refs.child_id = r.parent_id)

                                                    select  *
                                                    from r
                                                    where launch_id = %s order by level desc''', [
                id,
                launch_id
            ]):
                self.push(item_ref)

    @property
    def _get_full_path_obj(self):
        arr = []
        last = self.top()
        if last:
            arr.append(last)
        while True:
            if last.parent != None:
                last = [item for item in self.stack if item.child.id == last.parent.id]
                if len(last) > 0:
                    last = last[0]
                    arr.append(last)
                else:
                    break
            else:
                # arr.append(last)
                break

        arr = [item for item in reversed(arr)]
        return arr

    @property
    def get_full_path_obj(self):
        from kaf_pas.ckk.models.item_operations_view import Item_operations_view
        from kaf_pas.ckk.models.item_operations_view import Item_operations_viewManager
        arr = [Item_operations_viewManager.getRecord(Item_operations_view.objects.get(refs_id=item.id)) for item in self._get_full_path_obj]
        return arr

    @property
    def get_full_path(self):
        arr = self._get_full_path_obj
        # arr = [item for item in arr if arr.parent != None]
        res = ' / '.join([item.child.item_name for item in arr])
        return '/ ' + res


class Ready_2_launchManager(AuditManager):

    @staticmethod
    def _del_options(request):
        delAttr(request.json.get('data'), 'full_name')
        delAttr(request.json.get('data'), 'check_qty')
        delAttr(request.json.get('data'), 'check_material')
        delAttr(request.json.get('data'), 'check_resources')
        delAttr(request.json.get('data'), 'check_edizm')
        delAttr(request.json.get('data'), 'check_operation')
        delAttr(request.json.get('data'), 'check_colvo')
        return request

    # ('check_qty', 'Проверять длительность'),  # 1
    # ('check_num', 'Проверять № п/п'),  # 2
    # ('check_material', 'Проверять материалы'),  # 4
    # ('check_resources', 'Проверять ресурсы'),  # 8
    # ('check_edizm', 'Проверять еденицу измерения'),  # 16
    # ('check_operation', 'Проверять операцию'),  # 32
    # ('check_colvo', 'Проверять количество'),  # 64
    @staticmethod
    def make(demand_id, user, ready_2_launch=None, props=32):
        from kaf_pas.production.models.ready_2_launch_detail import Ready_2_launch_detail

        if not isinstance(demand_id, int):
            raise Exception(f'demand must be int')

        if isinstance(user, int):
            user = User.objects.get(id=user)
        elif not isinstance(user, User):
            raise Exception(f'user must be a User instance or int')

        for demand in Demand.objects.filter(id=demand_id):
            cnt = 0
            cnt_not = 0

            all_notes = Stack()
            options = Stack()

            if IsBitOn(props, 0):
                options.push('Включена опция проверки наличия у операции длительности выполнения.')

            if IsBitOn(props, 1):
                options.push('Включена опция проверки наличия у операции № п/п.')

            if IsBitOn(props, 2):
                options.push('Включена опция проверки наличия у операции материалов или стандартных изделий.')

            if IsBitOn(props, 3):
                options.push('Включена опция проверки наличия у операции ресурса либо места выполнения.')

            if IsBitOn(props, 4):
                options.push('Включена опция проверки наличия у операции единицы измерения.')

            if IsBitOn(props, 5):
                options.push('Включена опция проверки наличия операций.')

            if IsBitOn(props, 6):
                options.push('Включена опция проверки количества.')

            demand_str = f'<h3>Оценка готовности к запуску: Заказ № {demand.code} от {DateToStr(demand.date)}</h3>'

            key=f'Ready_2_launchManager.make_{demand.id}'
            settings.LOCKS.acquire(key)
            qty = Item_refs.objects.get_descendants_count(
                id=demand.precent_item.item.id,
            )
            logger.debug(f'Counted: {qty}')
            with managed_progress(
                    id=f'demand_{demand.id}_{ready_2_launch.props}_{user.id}',
                    qty=qty,
                    user=user,
                    message=demand_str,
                    title='Выполнено',
                    props=TurnBitOn(0, 0)

            ) as progress:
                with transaction.atomic():
                    def except_func():
                        settings.LOCKS.release(key)

                    progress.except_func = except_func

                    if not ready_2_launch:
                        ready_2_launch, _ = Ready_2_launch.objects.get_or_create(demand=demand.id)

                    items_refs_stack = Item_refs_Stack()
                    items_refs_stack.add_parents(demand.precent_item.item.id)

                    for item_ref in Item_refs.objects.get_descendants(
                            id=demand.precent_item.item.id,
                    ):

                        if item_ref.parent and item_ref.parent.id == p_id:
                            continue

                        notes = Stack()

                        # items_refs_stack.push(item_ref, lambda stack, item: len([it for it in stack if it.id != item_ref.id]) == 0)
                        items_refs_stack.push(item_ref)

                        operations_cnt = Operations_item.objects.filter(item=item_ref.child).count()
                        section = None
                        item_full_name = None
                        item_full_name_obj = None
                        cnt_not1 = 0

                        try:
                            item_line = Item_line.objects.get(parent=item_ref.parent, child=item_ref.child)
                            section = item_line.section

                            if section and section != 'Документация':
                                if item_ref.props.used.is_set == False:
                                    notes.push(f'Позиция не используется.')
                                    if not item_full_name:
                                        item_full_name_obj = items_refs_stack.get_full_path_obj
                                        item_full_name = items_refs_stack.get_full_path

                                elif IsBitOn(props, 6) and not item_line.qty:
                                    cnt_not1 += 1
                                    notes.push(f'Не указано количество.')
                                    if not item_full_name:
                                        item_full_name_obj = items_refs_stack.get_full_path_obj
                                        item_full_name = items_refs_stack.get_full_path

                        except Item_line.DoesNotExist:
                            cnt_not += 1
                            notes.push(f'Не входит в детализацию.')
                            if not item_full_name:
                                item_full_name_obj = items_refs_stack.get_full_path_obj
                                item_full_name = items_refs_stack.get_full_path

                        if item_ref.props.used.is_set == True:
                            if section and section != 'Документация':
                                if operations_cnt == 0:
                                    if IsBitOn(props, 5):
                                        cnt_not += 1
                                        notes.push(f'Не указаны операции.')
                                        item_full_name_obj = items_refs_stack.get_full_path_obj
                                        item_full_name = items_refs_stack.get_full_path
                                else:
                                    for operation in Operations_item.objects.filter(item=item_ref.child):
                                        if IsBitOn(props, 0) and not operation.qty:
                                            cnt_not1 = 1
                                            notes.push(f'Операция: {operation.operation.full_name} не указана длительность.')
                                            if not item_full_name:
                                                item_full_name_obj = items_refs_stack.get_full_path_obj
                                                item_full_name = items_refs_stack.get_full_path

                                        if IsBitOn(props, 1) and not operation.num:
                                            cnt_not1 = 1
                                            notes.push(f'Операция: {operation.operation.full_name} не указан № п/п.')
                                            if not item_full_name:
                                                item_full_name_obj = items_refs_stack.get_full_path_obj
                                                item_full_name = items_refs_stack.get_full_path

                                        if IsBitOn(props, 2):
                                            operation_material_cnt = Operation_material.objects.filter(operationitem=operation).count()
                                            if operation_material_cnt == 0:
                                                cnt_not1 = 1
                                                notes.push(f'Операция: {operation.operation.full_name} не указаны материалы или стандартные изделия.')
                                                if not item_full_name:
                                                    item_full_name_obj = items_refs_stack.get_full_path_obj
                                                    item_full_name = items_refs_stack.get_full_path

                                        if IsBitOn(props, 3):
                                            operation_resources_cnt = Operation_resources.objects.filter(operationitem=operation).count()
                                            if operation_resources_cnt == 0:
                                                cnt_not1 = 1
                                                notes.push(f'Операция: {operation.operation.full_name} не указан ресурс либо место выполнения.')
                                                if not item_full_name:
                                                    item_full_name_obj = items_refs_stack.get_full_path_obj
                                                    item_full_name = items_refs_stack.get_full_path

                                        if IsBitOn(props, 4) and not operation.ed_izm:
                                            cnt_not1 = 1
                                            notes.push(f'Операция: {operation.operation.full_name} не указана единица измерения.')
                                            if not item_full_name:
                                                item_full_name_obj = items_refs_stack.get_full_path_obj
                                                item_full_name = items_refs_stack.get_full_path

                        if notes.size() > 0:
                            notes_str = "\n".join(notes)
                            Ready_2_launch_detail.objects.get_or_create(
                                ready=ready_2_launch,
                                notes=notes_str,
                                item_full_name=item_full_name,
                                item_full_name_obj=item_full_name_obj,
                            )
                        cnt_not += cnt_not1
                        cnt += 1
                        if progress.step() != 0:
                            settings.LOCKS.release(key)
                            raise ProgressDroped(progress_deleted)

                    ready = round(100 - cnt_not / cnt * 100, 2)
                    all_notes.push(f'{ready}%')
                    notes_str = "\n".join(all_notes)
                    ready_2_launch.notes = f'<pre>{notes_str}</pre>'
                    ready_2_launch.save()

                    options_str = "\n" + "\n".join(options)
                    settings.EVENT_STACK.EVENTS_PRODUCTION_READY_2_LAUNCH.send_message(f'Выполнена {demand_str} <h3>готовность: {ready} </h3>{options_str}<p/>')
            settings.LOCKS.release(key)

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        demand_ids = _data.get('demand')

        delAttr(_data, 'demand__date')
        delAttr(_data, 'demand__name')
        delAttr(_data, 'demand__code')
        delAttr(_data, 'demand__description')
        delAttr(_data, 'demand__precent_item__STMP_1__value_str')
        delAttr(_data, 'demand__precent_item__STMP_2__value_str')
        delAttr(_data, 'demand__precent_item__STMP_1_id')
        delAttr(_data, 'demand__precent_item__STMP_2_id')
        delAttr(_data, 'demand__precent_item_id')

        props = 0
        if _data.get('check_qty'):
            props = TurnBitOn(props, 0)
        delAttr(_data, 'check_qty')

        if _data.get('check_num'):
            props = TurnBitOn(props, 1)
        delAttr(_data, 'check_num')

        if _data.get('check_material'):
            props = TurnBitOn(props, 2)
        delAttr(_data, 'check_material')

        if _data.get('check_resources'):
            props = TurnBitOn(props, 3)
        delAttr(_data, 'check_resources')

        if _data.get('check_edizm'):
            props = TurnBitOn(props, 4)
        delAttr(_data, 'check_edizm')

        if _data.get('check_operation'):
            props = TurnBitOn(props, 5)
        delAttr(_data, 'check_operation')

        if _data.get('check_colvo'):
            props = TurnBitOn(props, 6)
        delAttr(_data, 'check_colvo')

        setAttr(_data, 'props', props)

        delAttr(_data, 'date')
        for demand_id in demand_ids:
            delAttr(_data, 'demand')
            setAttr(_data, 'demand_id', demand_id)
            res = super().create(**_data)
            Ready_2_launchManager.make(
                demand_id=demand_id,
                user=request.user_id,
                ready_2_launch=res,
                props=props
            )

            res = Ready_2_launchManager.getRecord(res)
        data.update(DelProps(res))
        return data

    def reculcFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        ready_launtch_ids = data.get('data')

        for ready_launtch_id in ready_launtch_ids:
            _data = model_to_dict(Ready_2_launch.objects.get(id=ready_launtch_id))
            delAttr(_data, 'id')
            delAttr(_data, 'notes')
            setAttr(_data, 'demand_id', _data.get('demand'))
            delAttr(_data, 'demand')
            setAttr(_data, 'props', _data.get('props')._value)
            res = super().create(**_data)
            Ready_2_launchManager.make(
                demand_id=res.demand_id,
                user=request.user_id,
                ready_2_launch=res,
                props=_data.get('props')
            )

            res = Ready_2_launchManager.getRecord(res)
            res = DelProps(res)
        return res

    def updateFromRequest(self, request, removed=None, function=None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()
        return data

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'lastmodified': record.lastmodified,
            'demand__year': DateToStr(record.lastmodified, mask='%Y'),
            'demand__month': DateToStr(record.lastmodified, mask='%m'),
            'demand__month_name': manth_name(DateToStr(record.lastmodified, mask='%m')),
            'demand_id': record.demand.id,
            'demand__date': record.demand.date,
            'demand__code': record.demand.code,
            'demand__name': record.demand.name,
            'check_qty': record.props.check_qty,
            'check_num': record.props.check_num,
            'check_material': record.props.check_material,
            'check_resources': record.props.check_resources,
            'check_edizm': record.props.check_edizm,
            'check_operation': record.props.check_operation,
            'check_colvo': record.props.check_colvo,
            'demand__description': record.demand.description,
            'demand__precent_item_id': record.demand.precent_item.id,
            'demand__precent_item__STMP_1_id': record.demand.precent_item.item.STMP_1.id if record.demand.precent_item.item.STMP_1 else None,
            'demand__precent_item__STMP_1__value_str': record.demand.precent_item.item.STMP_1.value_str if record.demand.precent_item.item.STMP_1 else None,
            'demand__precent_item__STMP_2_id': record.demand.precent_item.item.STMP_2.id if record.demand.precent_item.item.STMP_2 else None,
            'demand__precent_item__STMP_2__value_str': record.demand.precent_item.item.STMP_2.value_str if record.demand.precent_item.item.STMP_2 else None,
            'notes': record.notes,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return Ready_2_launchQuerySet(self.model, using=self._db)


class Ready_2_launch(AuditModel):
    demand = ForeignKeyCascade(Demand)
    notes = TextField(null=True, blank=True)
    props = BitField(flags=(
        ('check_qty', 'Проверять длительность'),  # 1
        ('check_num', 'Проверять № п/п'),  # 2
        ('check_material', 'Проверять материалы'),  # 4
        ('check_resources', 'Проверять ресурсы'),  # 8
        ('check_edizm', 'Проверять еденицу измерения'),  # 16
        ('check_operation', 'Проверять операцию'),  # 32
        ('check_colvo', 'Проверять количество'),  # 64
    ), default=0, db_index=True)

    objects = Ready_2_launchManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = 'Готовность к запуску'
