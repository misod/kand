from django.http import HttpResponse
import csv
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import (FlightData, Glider, TowPlane)
from .tables import (LoggTable, GliderTable)

def people(request):
    table1 = LoggTable(FlightData.objects.all().select_related('glider'))
    RequestConfig(request).configure(table1)
    return render(request, 'people.html', {'table1': table1})



    #table2 = GliderTable(Glider.objects.all())
    #RequestConfig(request).configure(table1)
    #RequestConfig(request).configure(table2)
    #return render_to_response('people.html',
    #                          {'table1': table1},
    #                          context_instance=RequestContext(request))

# Create your views here.
