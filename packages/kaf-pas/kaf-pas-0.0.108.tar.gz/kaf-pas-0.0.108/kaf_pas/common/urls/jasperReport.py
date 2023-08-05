from django.urls import path

from kaf_pas.common.views import calendarGraph, jasperReport

urlpatterns = [

    path('JasperReport/Fetch/', jasperReport.JasperReports_Fetch),

]
