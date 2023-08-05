import logging

from django.core.management import BaseCommand

from kaf_pas.planing.models.operations import OperationPlanItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # for item in RoutingManager.make_levels(launch_id=23):
        route_oparation_item = dict(
            item_id=3151891,
            launch_ids=(70,)
        )

        route_oparation_item = OperationPlanItem(**route_oparation_item)
        print(route_oparation_item)
