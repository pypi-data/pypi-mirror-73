import logging

from django.db import ProgrammingError

logger = logging.getLogger(__name__)


class Operation_Stack:
    def __init__(self):
        from kaf_pas.production.models.resource import Resource
        from kaf_pas.production.models.operations import Operations
        from kaf_pas.ckk.models.locations import Locations

        try:

            self.NOOP, _ = Operations.objects.update_or_create(code='00', defaults=dict(
                name='Пустая операция',
                editing=False,
                deliting=False,
            ))

            self.NO_WORKSHOP, _ = Locations.objects.update_or_create(code='00', defaults=dict(
                name='Фиктивный цех',
                editing=False,
                deliting=False,
            ))

            self.NOT_UNDEFINED_WORKSHOP = lambda location: Resource.objects.get_or_create(
                location=location,
                code='none',
                defaults=dict(
                    name='Не определен'
                )
            )


        except ProgrammingError as ex:
            logger.warning(ex)
