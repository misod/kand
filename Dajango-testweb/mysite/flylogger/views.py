from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import (FlightData, Glider, TowPlane)
from .tables import (LoggTable, GliderTable)

def people(request):
    table1 = LoggTable(FlightData.objects.all().select_related('glider'))
    #table2 = GliderTable(Glider.objects.all())
    RequestConfig(request).configure(table1)
    #RequestConfig(request).configure(table2)
    return render(request, 'people.html', {'table1': table1})

# Create your views here.
