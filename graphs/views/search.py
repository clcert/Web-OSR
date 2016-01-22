import socket
from geoip import geolite2

from django.shortcuts import render

from graphs.models import Http80, Http443


def search(request):
    ip = '192.80.24.6'
    reversed_dns = socket.gethostbyaddr(ip)
    lat, long = geolite2.lookup(ip).location

    http80 = Http80.objects(ip=ip).order_by('-date').first()
    http443 = Http443.objects(ip=ip).order_by('-date').first()
    return render(request, 'graphs/search.html',
                  { 'ip': ip,
                    'reverse': reversed_dns[0],
                    'lat': lat,
                    'long': long,
                    'http80': http80,
                    'http443': http443})