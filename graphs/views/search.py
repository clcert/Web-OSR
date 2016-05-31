import socket
from geoip import geolite2
from django.shortcuts import render
from graphs.models import Http80, Http443, Http8080, Http8000, Https
from django.http import HttpResponse
import json


def search_partial(port, ip, position):
    if port == '80':
        try:
            data = Http80.objects(ip=ip).order_by('-date')[position]
        except IndexError:
            data = None
    if port == '443':
        try:
            data = Http443.objects(ip=ip).order_by('-date')[position]
        except IndexError:
            data = None

    if port == '8000':
        try:
            data = Http8000.objects(ip=ip).order_by('-date')[position]
        except IndexError:
            data = None

    if port == '8080':
        try:
            data = Http8080.objects(ip=ip).order_by('-date')[position]
        except IndexError:
            data = None

    if port == 'https':
        try:
            data = Https.objects(ip=ip).order_by('-date')[position]
        except IndexError:
            data = None

    return {'ip': ip,
            'datePosition': position,
            'port': port,
            'data': data}


def search(request):
    ip = request.GET[u'question']
    if u'position' not in request.GET:
        date_position = 0
        print 'No se entrego position'
    else:
        date_position = int(request.GET[u'position'])
        direction = request.GET[u'direction']
        if direction == 'left':
            date_position += 1
        else:
            date_position -= 1
        if date_position < 0:
            date_position = 0

    # latest date is 0, increasing position goes back in time
    # ip = '201.220.232.16'
    try:
        reversed_dns = socket.gethostbyaddr(ip)
    except socket.herror:
        reversed_dns = 'Unknown host'

    try:
        lat, long = geolite2.lookup(ip).location
    except AttributeError:
        lat, long = None, None

    try:
        http80 = Http80.objects(ip=ip).order_by('-date')[date_position]
    except IndexError:
        http80 = None
    try:
        http443 = Http443.objects(ip=ip).order_by('-date')[date_position]
    except IndexError:
        http443 = None

    try:
        http8000 = Http8000.objects(ip=ip).order_by('-date')[date_position]
    except IndexError:
        http8000 = None

    try:
        http8080 = Http8080.objects(ip=ip).order_by('-date')[date_position]
    except IndexError:
        http8080 = None

    try:
        https = Https.objects(ip=ip).order_by('-date')[date_position]
    except IndexError:
        https = None

    return render(request, 'graphs/search.html',
                  {'ip': ip,
                   'reverse': reversed_dns[0],
                   'lat': lat,
                   'long': long,
                   'datePosition': date_position,
                   'http80': http80,
                   'http443': http443,
                   'http8000': http8000,
                   'http8080': http8080,
                   'https': https})
