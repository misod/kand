from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from log.models import Post

urlpatterns = [url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-date")[:25],
                                            template_name="log/log.html")),
                url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-date")[:25],
                                            template_name="log/home.html")),
                url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Post,
                                                         template_name='log/post.html'))
                                                         ]
