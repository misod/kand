from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from . import views
from django_tables2 import RequestConfig
from flylogger.models import Person
from django.contrib import admin
from django.views import static

urlpatterns = [url(r'^$', views.people, name='people'),
            url(r'^export', views.export, name = 'export'),
                                                         ]

#url(r'^$', views.people, name='people')
