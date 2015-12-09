from django.conf.urls import include, url
from django.contrib import admin

from graphs import views

urlpatterns = [
    url(r'^$', views.index, name='graphs/index'),
    url(r'^web-server/all/(?P<scan>\d+-\d+-\d+)$', views.http_server_all, name='graphs/server/all'),
    url(r'^web-server/(?P<port>[0-9]+)/(?P<scan>\d+-\d+-\d+)$', views.http_server, name='graphs/server'),
    url(r'^web-server/(?P<port>[0-9]+)/(?P<scan>\d+-\d+-\d+)/(?P<version>[\w\s]+)$', views.http_server, name='graphs/server'),
    url(r'^operative-system/all/(?P<scan>\d+-\d+-\d+)$', views.os_server_all, name='graphs/os/all'),
    url(r'^operative-system/(?P<port>[0-9]+)/(?P<scan>\d+-\d+-\d+)$', views.os_server, name='graphs/os'),
    url(r'^device/all', views.device_type_all, name='graphs/device/all'),
    url(r'^device/(?P<port>[0-9]+)/$', views.device_type, name='graphs/device')
]