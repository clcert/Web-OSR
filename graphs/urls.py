from django.conf.urls import include, url
from django.contrib import admin

from graphs import views

urlpatterns = [
    url(r'^$', views.index, name='graphs/index'),
    url(r'^web-server/all', views.http_server_all, name='graphs/server/all'),
    url(r'^web-server/all/(?P<version>\w+)', views.http_server_all, name='graphs/server/all'),
    url(r'^web-server/(?P<port>[0-9]*)/$', views.http_server, name='graphs/server'),
    url(r'^web-server/(?P<port>[0-9]*)/(?P<version>\w*)', views.http_server, name='graphs/server'),
    url(r'^operative-system/all', views.os_server_all, name='graphs/os/all'),
    url(r'^operative-system/(?P<port>[0-9]*)/$', views.os_server, name='graphs/os'),
    url(r'^device/all', views.device_type_all, name='graphs/device/all'),
    url(r'^device/(?P<port>[0-9]*)/$', views.device_type, name='graphs/device'),
]