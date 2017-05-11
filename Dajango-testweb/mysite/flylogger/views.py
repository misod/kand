from django.http import HttpResponse
import csv
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import (FlightData, Glider, TowPlane)
from .tables import (LoggTable, GliderTable)
from .admin import FlightDataResource
import datetime

def people(request):
    today = datetime.datetime.today()
    table1 = LoggTable(FlightData.objects.filter(logged_date = today ).select_related('glider'), order_by="-logged_date")
    RequestConfig(request, paginate={'per_page': 20}).configure(table1)
    return render(request, 'people.html', {'table1': table1}, )


def export(request):
    flight_resource = FlightDataResource()
    dataset = flight_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="flylog.xls"'
    return response



    #table2 = GliderTable(Glider.objects.all())
    #RequestConfig(request).configure(table1)
    #RequestConfig(request).configure(table2)
    #return render_to_response('people.html',
    #                          {'table1': table1},
    #                          context_instance=RequestContext(request))

# Create your views here.
