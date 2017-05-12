from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView
from log.models import Post


urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^webapp/', include('webapp.urls')),
    url(r'^contact', views.contact, name = 'contact'),
    url(r'^information', views.information, name = 'information'),
    url(r'^signup', views.signup, name = 'signup'),
    #url(r'^$', flylogger.views.flylogger, template_name = "flylogger/flylogger.html"),
    #url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-date")[:25],
                                #                template_name="log/log.html")),
                    #url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post,
                                                    #         template_name='log/post.html'))
]
