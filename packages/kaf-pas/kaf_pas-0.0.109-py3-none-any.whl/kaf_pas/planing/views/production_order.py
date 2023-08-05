from django.conf import settings

from isc_common import dictinct_list
from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException, JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.operation_resources_view import Operation_resources_view
from kaf_pas.planing.models.production_order import Production_order, Production_orderManager
from kaf_pas.planing.models.production_order_opers import Production_order_opers, Production_order_opersManager
from kaf_pas.planing.models.production_order_opers_per_launch import Production_order_opers_per_launch
from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch


@JsonResponseWithException()
def Production_order_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'location', 'edizm', 'item').
                    filter(
                    opertype__in=opers_types,
                ).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'location', 'edizm', 'item').
                    filter(
                    opertype__in=opers_types,
                ).
                    filter(exucutors__overlap=[_request.user_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_per_launch_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_per_launch.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'location', 'edizm', 'item').
                    filter(
                    opertype__in=opers_types,
                ).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_per_launch.objects.
                    select_related('opertype', 'creator', 'status', 'launch', 'location', 'edizm', 'item').
                    filter(
                    opertype__in=opers_types,
                ).
                    filter(exucutors__overlap=[_request.user_id]).
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_FetchDetail(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK.id,
    ]

    _request = DSRequest(request=request)
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_opers.objects.
                filter(
                opertype__in=opers_types,
            ).
                get_range_rows1(
                request=request,
                function=Production_order_opersManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_per_launch_FetchDetail(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_OPERS_TASK.id,
    ]

    _request = DSRequest(request=request)
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_opers_per_launch.objects.
                filter(
                opertype__in=opers_types,
            ).
                get_range_rows1(
                request=request,
                function=Production_order_opersManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLocations(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)

    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing
                    ]
                ).
                    values('location_id', 'location__name').
                    distinct().
                    order_by('location__name').
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLocations
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(executor__in=[_request.user_id]).
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing
                    ]
                ).
                    values('location_id', 'location__name').
                    distinct().
                    order_by('location__name').
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLocations,
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLevels(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(executor__in=[_request.user_id]).
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchExecutorsLocation(request):
    from kaf_pas.ckk.models.locations_users import Locations_users
    from kaf_pas.ckk.models.locations_users import Locations_usersManager
    return JsonResponse(
        DSResponse(
            request=request,
            data=Locations_users.objects.
                filter().
                distinct().
                get_range_rows1(
                request=request,
                function=Locations_usersManager.getRecord1
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_Update4(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequest4(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_SetStartStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setStartStatus(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_getValue_made(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getValue_made(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def User_Fetch4(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getLoocationUsers(request=request), status=RPCResponseConstant.statusSuccess).response)
