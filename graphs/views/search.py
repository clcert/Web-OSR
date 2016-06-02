import socket
from geoip import geolite2
from django.shortcuts import render
from graphs.models import Http80, Http443, Http8080, Http8000, Https
from django.http import HttpResponse, JsonResponse
import json


def search_partial(request, port, ip, date, direction=None):
    if port == '80':
        http_model = Http80

    if port == '443':
        http_model = Http443

    if port == '8000':
        http_model = Http8000

    if port == '8080':
        http_model = Http8080

    params = {'ip': ip}
    if direction == 'left':
        direction = '-date'
        params['date__lt'] = date
    else:
        direction = 'date'
        params['date__gt'] = date
    try:
        data = http_model.objects(**params).order_by(direction).first()
    except IndexError:
        data = {}
    if data is None:
        return JsonResponse({})
    return HttpResponse(data.to_json(), content_type="application/json")


def search(request):
    ip = request.GET[u'question']
    if u'position' not in request.GET:
        date_position = 0
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
