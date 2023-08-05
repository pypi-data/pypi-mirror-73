from django.urls import path

from kaf_pas.planing.views import production_order

urlpatterns = [

    path('Production_order/Fetch/', production_order.Production_order_Fetch),
    path('Production_order_per_launch/Fetch/', production_order.Production_order_per_launch_Fetch),
    path('Production_order/Fetch4/', production_order.User_Fetch4),
    path('Production_order/FetchDetail/', production_order.Production_order_FetchDetail),
    path('Production_order_per_launch/FetchDetail/', production_order.Production_order_per_launch_FetchDetail),
    path('Production_order/FetchLocations/', production_order.Production_order_FetchLocations),
    path('Production_order/FetchLevels/', production_order.Production_order_FetchLevels),
    path('Production_order/FetchExecutorsLocation/', production_order.Production_order_FetchExecutorsLocation),
    path('Production_order/Add', production_order.Production_order_Add),
    path('Production_order/Update', production_order.Production_order_Update),
    path('Production_order/Update4', production_order.Production_order_Update4),
    path('Production_order/Remove', production_order.Production_order_Remove),
    path('Production_order/Lookup/', production_order.Production_order_Lookup),
    path('Production_order/Info/', production_order.Production_order_Info),
    path('Production_order/Copy', production_order.Production_order_Copy),
    path('Production_order/SetStartStatus', production_order.Production_order_SetStartStatus),
    path('Production_order/getValue_made/', production_order.Production_order_getValue_made),

]
