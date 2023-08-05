import logging

from django.forms import model_to_dict

from isc_common.http.DSRequest import DSRequest
from kaf_pas.ckk.models.locations import Locations
from kaf_pas.planing.models.operation_level_view import Operation_level_view
from kaf_pas.planing.models.operation_location_view import Operation_location_view
from kaf_pas.planing.models.operation_resources_view import Operation_resources_view
from kaf_pas.planing.models.operations_rout_view import Operations_rout_viewManager
from kaf_pas.planing.models.operations_view import Operations_view, Operations_viewManager, Operations_viewQuerySet

logger = logging.getLogger(__name__)


class RoutingQuerySet(Operations_viewQuerySet):
    def raw(self, raw_query=None, params=None, translations=None, using=None, function=None):
        if raw_query == None:
            raw_query = '''select *
                            from (with r as (select          pr."id",
                                                             pr."child_id",
                                                             null::bigint "parent_id",
                                                             pr."num",
                                                             pr."date",
                                                             pr."deleted_at",
                                                             pr."editing",
                                                             pr."deliting",
                                                             pr."lastmodified",
                                                             pr."opertype_id",
                                                             pr."STMP_1_id",
                                                             pr."item__STMP_1_value_str",
                                                             pr."STMP_2_id",
                                                             pr."item__STMP_2_value_str",
                                                             pr."status_id",
                                                             pr."description",
                                                             pr."creator_id",
                                                             pr."resource_id",
                                                             pr."item_id",
                                                             pr."level_id",
                                                             pr."launch_id",
                                                             pr."location_id",
                                                             0 as         "props",
                                                             pr."production_operation_id",
                                                             pr."production_operation_ed_izm_id",
                                                             pr."production_operation_num",
                                                             pr."production_operation_qty",
                                                             pr."mark"
                                             from planing_operation_rout_view pr
                                             where pr.item_id = %s      --0
                                               and pr.resource_id = %s --1
                                               and pr.launch_id = %s    --2
                                               and pr.props = 1
                            )

                                  select distinct pr."id",
                                                  pr."child_id",
                                                  null::bigint as "parent_id",
                                                  pr."num",
                                                  pr."date",
                                                  pr."deleted_at",
                                                  pr."editing",
                                                  pr."deliting",
                                                  pr."lastmodified",
                                                  pr."opertype_id",
                                                  pr."STMP_1_id",
                                                  pr."item__STMP_1_value_str",
                                                  pr."STMP_2_id",
                                                  pr."item__STMP_2_value_str",
                                                  pr."status_id",
                                                  pr."description",
                                                  pr."creator_id",
                                                  pr."resource_id",
                                                  pr."item_id",
                                                  pr."level_id",
                                                  pr."launch_id",
                                                  pr."location_id",
                                                  pr."props",
                                                  pr."production_operation_id",
                                                  pr."production_operation_ed_izm_id",
                                                  pr."production_operation_num",
                                                  pr."production_operation_qty",
                                                  'income'     as mark
                                  from planing_operation_rout_view pr
                                  where pr.child_id = (select distinct poi.id
                                                       from planing_operation_rout_view poi
                                                       where poi.item_id = %s     --3
                                                         and poi.opertype_id = %s --4
                                                         and poi.launch_id = %s   --5
                                                         and poi.production_operation_num = (select min(production_operation_num)
                                                                                             from planing_operation_rout_view poi
                                                                                             where poi.item_id = %s     --6
                                                                                               and poi.resource_id = %s --7
                                                                                               and poi.opertype_id = %s --8
                                                                                               and poi.launch_id = %s --9
                                                       ))
                                    and pr.props = 2
                                  union
                                  select pr."id",
                                         pr."child_id",
                                         pr."parent_id",
                                         pr."num",
                                         pr."date",
                                         pr."deleted_at",
                                         pr."editing",
                                         pr."deliting",
                                         pr."lastmodified",
                                         pr."opertype_id",
                                         pr."STMP_1_id",
                                         pr."item__STMP_1_value_str",
                                         pr."STMP_2_id",
                                         pr."item__STMP_2_value_str",
                                         pr."status_id",
                                         pr."description",
                                         pr."creator_id",
                                         pr."resource_id",
                                         pr."item_id",
                                         pr."level_id",
                                         pr."launch_id",
                                         pr."location_id",
                                         pr."props",
                                         pr."production_operation_id",
                                         pr."production_operation_ed_izm_id",
                                         pr."production_operation_num",
                                         pr."production_operation_qty",
                                         'local' as mark
                                  from r pr
                                  union
                                  select pr."id",
                                         pr."child_id",
                                         null      as "parent_id",
                                         pr."num",
                                         pr."date",
                                         pr."deleted_at",
                                         pr."editing",
                                         pr."deliting",
                                         pr."lastmodified",
                                         pr."opertype_id",
                                         pr."STMP_1_id",
                                         pr."item__STMP_1_value_str",
                                         pr."STMP_2_id",
                                         pr."item__STMP_2_value_str",
                                         pr."status_id",
                                         pr."description",
                                         pr."creator_id",
                                         pr."resource_id",
                                         pr."item_id",
                                         pr."level_id",
                                         pr."launch_id",
                                         pr."location_id",
                                         pr."props",
                                         pr."production_operation_id",
                                         pr."production_operation_ed_izm_id",
                                         pr."production_operation_num",
                                         pr."production_operation_qty",
                                         'outcome' as mark
                                  from planing_operation_rout_view pr
                                  where pr.item_id = %s     --10
                                    and pr.resource_id = %s --11
                                    and pr.opertype_id = %s --12
                                    and pr.launch_id = %s --13
                                    and parent_id = (select distinct poo.operation_id
                                                     from planing_operation_item poi
                                                              join planing_operation_operation poo on poi.operation_id = poo.operation_id
                                                              join planing_operation_rout_view op on poi.operation_id = op.id
                                                     where poi.item_id = %s    --14
                                                       and op.opertype_id = %s --15
                                                       and op.launch_id = %s   --16
                                                       and poo.num = (select max(production_operation_num)
                                                                      from planing_operation_rout_view poi
                                                                      where poi.item_id = %s     --17
                                                                        and poi.resource_id = %s --18
                                                                        and poi.opertype_id = %s --19
                                                                        and poi.launch_id = %s --20
                                                     ))
                                    and pr.props = 2) as a
                                    '''

        queryResult = super().raw(raw_query=raw_query, params=params, translations=translations, using=using)
        if function:
            res = [function(record) for record in queryResult]
        else:
            res = [model_to_dict(record) for record in queryResult]
        return res


class RoutingManager(Operations_viewManager):

    @staticmethod
    def getRecord(record):
        return Operations_rout_viewManager.getRecord(record)

    def get_queryset(self):
        return RoutingQuerySet(self.model, using=self._db)

    def fetchLevelsFromRequest(self, request):
        request = DSRequest(request=request)

        launch_id = request.get_data().get('launch_id')
        levels = RoutingManager.make_levels(launch_id=launch_id)
        return levels

    @staticmethod
    def make_levels(launch_id):
        res = [
            dict(
                id=operation.get('level_id'),
                title=operation.get('level__name'),
                prompt=f'''ID: {operation.get('level_id')}, {operation.get('level__code')} : {operation.get('level__name')}'''
            )
            for operation in Operation_level_view.objects.
                filter(
                launch_id=launch_id,
                opers_refs_props__in=[
                    Operations_view.props.inner_routing,
                    Operations_view.props.outer_routing,
                ]
            ).
                order_by('level__code').
                values('level_id', 'level__name', 'level__code').
                distinct()
        ]
        return res

    def fetchLocationsLevelFromRequest(self, request):
        request = DSRequest(request=request)

        launch_id = request.get_data().get('launch_id')
        level_id = request.get_data().get('level_id')
        levels = RoutingManager.make_locationsLevel(launch_id=launch_id, level_id=level_id)
        return levels

    @staticmethod
    def make_locationsLevel(launch_id, level_id):
        res = sorted([
            dict(
                id=operation.get('location_id'),
                title=Locations.objects.get(id=operation.get('location_id')).full_name,
                prompt=f'''ID: {operation.get('location_id')}''',
            )
            for operation in Operation_location_view.objects.
                filter(
                launch_id=launch_id,
                opers_refs_props__in=[
                    Operations_view.props.inner_routing,
                    Operations_view.props.outer_routing,
                ],
                level_id=level_id
            ).
                values('location_id', 'location__name').
                distinct()
        ],
            key=lambda x: x['title'])

        return res

    def fetchResourcesLevelFromRequest(self, request):
        request = DSRequest(request=request)

        launch_id = request.get_data().get('launch_id')
        level_id = request.get_data().get('level_id')
        location_id = request.get_data().get('location_id')
        levels = RoutingManager.make_resourcesLevel(launch_id=launch_id, level_id=level_id, location_id=location_id)
        return levels

    @staticmethod
    def make_resourcesLevel(launch_id, level_id, location_id):
        res = sorted([
            dict(
                id=operation.get('resource_id'),
                title=operation.get('resource__name'),
                prompt=f'''ID: {operation.get('resource_id')}, {operation.get('resource__description')}''',
            )
            for operation in Operation_resources_view.objects.
                filter(
                launch_id=launch_id,
                level_id=level_id,
                location_id=location_id,
                props__in=[
                    Operations_view.props.inner_routing,
                    Operations_view.props.outer_routing,
                ],
            ).
                values('resource_id', 'resource__name', 'resource__description').
                distinct()
        ],
            key=lambda x: x['title'])

        return res


class Routing(Operations_view):
    objects = RoutingManager()

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Маршрутизация'
        proxy = True
