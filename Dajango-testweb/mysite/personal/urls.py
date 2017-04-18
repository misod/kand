from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^webapp/', include('webapp.urls')),
    url(r'^contact', views.contact, name = 'contact'),
]
