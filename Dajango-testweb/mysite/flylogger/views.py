from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Person
from .tables import PersonTable

def people(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'people.html', {'table': table})

# Create your views here.
