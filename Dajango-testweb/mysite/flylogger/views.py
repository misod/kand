from flylogger import models
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Person
from .tables import PersonTable

def people(request):
    return render(request, 'people.html', {'people': Person.objects.all()})
# Create your views here.
