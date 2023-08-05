import logging

from django.db import ProgrammingError

from isc_common.common import blue, green, new, new_man, started, restarted, transferred, doing, closed, made

logger = logging.getLogger(__name__)

CLC_TSK = 'CLC_TSK'
DETAIL_CLC_MINUS_TSK = 'DETAIL_CLC_MINUS_TSK'
DETAIL_CLC_PLUS_TSK = 'DETAIL_CLC_PLUS_TSK'
DETAIL_OPERS_PRD_TSK = 'DETAIL_OPERS_PRD_TSK'
DETAIL_SUM_PRD_TSK = 'DETAIL_SUM_PRD_TSK'
LAUNCH_TSK = 'LAUNCH_TSK'
MADE_OPRS_TSK = 'MADE_OPRS_TSK'
PRD_TSK = 'PRD_TSK'
PST_EQV_TSK = 'PST_EQV_TSK'
PST_TSK = 'PST_TSK'
RELEASE_TSK_MNS = 'RELEASE_TSK_MNS'
RELEASE_TSK_PLS = 'RELEASE_TSK_PLS'
RT_TSK = 'RT_TSK'
WRT_OFF_TSK = 'WRT_OFF_TSK'


class Operation_typesStack:

    def __init__(self):
        from kaf_pas.planing.models.operation_types import Operation_types
        from kaf_pas.planing.models.status_operation_types import Status_operation_typesManager

        try:
            self.PRODUCTION_TASK, _ = Operation_types.objects.update_or_create(code=PRD_TSK, defaults=dict(
                props=0,
                name='Задание на производство',
                editing=False,
                deliting=False,
            ))

            self.PRODUCTION_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.PRODUCTION_TASK,
                status_map=[
                    dict(code=new, name='Новый (с)', color=blue),
                    dict(code=new_man, name='Новый (р)', color=blue),
                    dict(code=started, name='Запущен', color=green),
                    dict(code=restarted, name='Запущен (повторно)', color=green),
                    dict(code=transferred, name='Назначенный'),
                    dict(code=doing, name='Выполнен'),
                    dict(code=closed, name='Закрыт'),
                ]
            )

            self.PRODUCTION_DETAIL_OPERS_TASK, _ = Operation_types.objects.update_or_create(code=DETAIL_OPERS_PRD_TSK, defaults=dict(
                props=0,
                name='Детализация Задания на производство по операциям',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.PRODUCTION_DETAIL_OPERS_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.PRODUCTION_DETAIL_OPERS_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.PRODUCTION_DETAIL_SUM_TASK, _ = Operation_types.objects.update_or_create(code=DETAIL_SUM_PRD_TSK, defaults=dict(
                props=0,
                name='Детализация Задания на производство (суммы)',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.PRODUCTION_DETAIL_SUM_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.PRODUCTION_DETAIL_SUM_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.LAUNCH_TASK, _ = Operation_types.objects.update_or_create(code=LAUNCH_TSK, defaults=dict(
                props=0,
                name='Запуск задания на производство',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.LAUNCH_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.LAUNCH_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                    dict(code=made, name='Выполнен'),
                ]
            )

            self.MADE_OPERATIONS_TASK, _ = Operation_types.objects.update_or_create(code=MADE_OPRS_TSK, defaults=dict(
                props=0,
                name='Выполнение производственной операции',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.MADE_OPERATIONS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.MADE_OPERATIONS_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.RELEASE_TASK_PLUS, _ = Operation_types.objects.update_or_create(code=RELEASE_TSK_PLS, defaults=dict(
                props=Operation_types.props.plus | Operation_types.props.accounting,
                name='Выпуск изделий',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.RELEASE_TASK_PLUS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.RELEASE_TASK_PLUS,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.RELEASE_TASK_MINUS, _ = Operation_types.objects.update_or_create(code=RELEASE_TSK_MNS, defaults=dict(
                props=Operation_types.props.minus | Operation_types.props.accounting,
                name='Расходование изделий',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            ))

            self.RELEASE_TASK_MINUS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.RELEASE_TASK_MINUS,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.CALC_TASKS, _ = Operation_types.objects.update_or_create(code=CLC_TSK, defaults=dict(
                props=0,
                name='Учет',
                editing=False,
                deliting=False,
            ))

            self.CALC_TASKS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.CALC_TASKS,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.CALC_DETAIL_PLUS_TASK, _ = Operation_types.objects.update_or_create(code=DETAIL_CLC_PLUS_TSK, defaults=dict(
                props=Operation_types.props.plus | Operation_types.props.accounting,
                name='Детализация Учет приход',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            ))

            self.CALC_DETAIL_PLUS_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.CALC_DETAIL_PLUS_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.CALC_DETAIL_MINUS_TASK, _ = Operation_types.objects.update_or_create(code=DETAIL_CLC_MINUS_TSK, defaults=dict(
                props=Operation_types.props.minus | Operation_types.props.accounting,
                name='Детализация Учет расход',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            ))

            self.CALC_DETAIL_MINUS_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.CALC_DETAIL_MINUS_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.POSTING_TASK, _ = Operation_types.objects.update_or_create(code=PST_TSK, defaults=dict(
                props=0,
                name='Оприходование',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            ))

            self.POSTING_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.POSTING_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.POSTING_EQV_TASK, _ = Operation_types.objects.update_or_create(code=PST_EQV_TSK, defaults=dict(
                props=0,
                name='Оприходование по минусам (выравнивание остатков)',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            ))

            self.POSTING_EQV_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.POSTING_EQV_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.WRITE_OFF_TASK, _ = Operation_types.objects.update_or_create(code=WRT_OFF_TSK, defaults=dict(
                props=0,
                name='Списание',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            ))

            self.WRITE_OFF_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.WRITE_OFF_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )

            self.ROUTING_TASK, _ = Operation_types.objects.update_or_create(code=RT_TSK, defaults=dict(
                props=0,
                name='Маршрутизация',
                editing=False,
                deliting=False,
            ))

            self.ROUTING_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.ROUTING_TASK,
                status_map=[
                    dict(code=new, name='Новый'),
                ]
            )


        except ProgrammingError as ex:
            logger.warning(ex)
