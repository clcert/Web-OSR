from django.conf.urls import include, url
from django.contrib import admin

from graphs import views

urlpatterns = [
    url(r'^http$', views.http_index, name='graphs/http-index'),
    url(r'^web-server/all/(?P<scan_date>\d+-\d+-\d+)$', views.http_server_all, name='graphs/server/all'),
    url(r'^web-server/(?P<port>[0-9]+)$', views.http_server, name='graphs/server'),
    url(r'^web-server/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.http_server, name='graphs/server'),
    url(r'^web-server/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)/(?P<product>[\w\s]+)$', views.http_server, name='graphs/server'),
    url(r'^operative-system/all/(?P<scan_date>\d+-\d+-\d+)$', views.operating_system_server_all, name='graphs/os/all'),
    url(r'^operative-system/(?P<port>[0-9]+)$', views.operating_system_server, name='graphs/os'),
    url(r'^operative-system/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.operating_system_server, name='graphs/os'),
    url(r'^device/all/(?P<scan_date>\d+-\d+-\d+)$', views.device_type_all, name='graphs/device/all'),
    url(r'^device/(?P<port>[0-9]+)$', views.device_type, name='graphs/device'),
    url(r'^device/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.device_type, name='graphs/device'),
    # url(r'^https/key-bits$', views.certificate_key_bits, name='graphs/https/key-bits'),
    # url(r'^https/validation$', views.certificate_validation, name='graphs/https/validation'),
    # url(r'^https/cipher-suite$', views.certificate_cipher_suite, name='graphs/https/cipher-suite'),
    # url(r'^https/tls_version$', views.certificate_tls_version, name='graphs/https/tls-version'),
    # url(r'^https/signature$', views.certificate_signature, name='graphs/https/signature'),
    # url(r'^search/ip', views.ip_search, name='search/ip'),
    # url(r'^search$', views.search, name='search'),
]

