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
    url(r'^https/key-bits/(?P<port>[0-9]+)$', views.key_bits, name='graphs/https/key-bits'),
    url(r'^https/key-bits/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.key_bits, name='graphs/https/key-bits'),
    url(r'^https/validation/(?P<port>[0-9]+)$', views.validation, name='graphs/https/validation'),
    url(r'^https/validation/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.validation, name='graphs/https/validation'),
    url(r'^https/signature/(?P<port>[0-9]+)$', views.signature, name='graphs/https/signature'),
    url(r'^https/signature/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.signature, name='graphs/https/signature'),
    url(r'^https/cipher-suite/(?P<port>[0-9]+)$', views.cipher_suite, name='graphs/https/cipher-suite'),
    url(r'^https/cipher-suite/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.cipher_suite, name='graphs/https/cipher-suite'),
    url(r'^https/tls_version/(?P<port>[0-9]+)$', views.tls_version, name='graphs/https/tls-version'),
    url(r'^https/tls_version/(?P<port>[0-9]+)/(?P<scan_date>\d+-\d+-\d+)$', views.tls_version, name='graphs/https/tls-version'),
    # url(r'^search/(?P<port>[0-9]+)/(?P<ip>([0-9]{1,3}\.){3}[0-9]{1,3})/(?P<date>[\w\-]+)/(?P<direction>[\w]+)$', views.search_partial, name='search/partial'),
    # url(r'^search/cert/(?P<ip>([0-9]{1,3}\.){3}[0-9]{1,3})/(?P<date>[\w\-]+)/(?P<direction>[\w]+)$',
    #     views.search_partial_cert, name='search/cert/partial'),
    # url(r'^search/ip', views.ip_search, name='search/ip'),
    url(r'^search$', views.search, name='search'),
    # url(r'^asn$', views.asn, name='graphs/asn'),
]

