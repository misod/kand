from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import FlightData
from .tables import LoggTable

def people(request):
    table = LoggTable(FlightData.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'people.html', {'table': table})

# Create your views here.
