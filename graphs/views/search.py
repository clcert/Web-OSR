import socket
from geoip import geolite2
from django.shortcuts import render
from graphs.models import HTTP80, HTTP443, HTTP8000, HTTP8080, HTTP_PORT
from graphs.models.util import HTTP

from django.http import HttpResponse, JsonResponse


def search_partial(request, port, ip, date, direction=None):

    if direction == 'left':
        data = HTTP(HTTP_PORT[port].objects.filter(ip=ip, date__lt=date).order_by('-date').first().data)
    else:
        data = HTTP(HTTP_PORT[port].objects.filter(ip=ip, date__gt=date).order_by('date').first().data)

    if data is None:
        return JsonResponse({})
    return HttpResponse(data.to_json(), content_type="application/json")
#
#
# def search_partial_cert(request, ip, date, direction=None):
#     http_model = Https
#
#     params = {'ip': ip}
#     if direction == 'left':
#         direction = '-date'
#         #params['date__lt'] = date
#     else:
#         direction = 'date'
#         #params['date__gt'] = date
#     try:
#         data = http_model.objects(**params).order_by(direction).first()
#     except IndexError:
#         data = {}
#     if data is None:
#         return JsonResponse({})
#     return HttpResponse(data.to_json(), content_type="application/json")


def search(request):
    ip = request.GET['question']

    if 'position' not in request.GET:
        date_position = 0
    else:
        date_position = int(request.GET['position'])

        if date_position < 0:
            date_position = 0

    try:
        reversed_dns = socket.gethostbyaddr(ip)
    except socket.herror:
        reversed_dns = 'Unknown host'

    try:
        lat, long = geolite2.lookup(ip).location
    except AttributeError:
        lat, long = None, None

    try:
        http80 = HTTP(HTTP80.objects.filter(ip=ip).order_by('-date')[date_position].data)
    except IndexError:
        http80 = None

    try:
        http443 = HTTP(HTTP443.objects.filter(ip=ip).order_by('-date')[date_position].data)
    except IndexError:
        http443 = None

    try:
        http8000 = HTTP(HTTP8000.objects.filter(ip=ip).order_by('-date')[date_position].data)
    except IndexError:
        http8000 = None

    try:
        http8080 = HTTP(HTTP8080.objects.filter(ip=ip).order_by('-date')[date_position].data)
    except IndexError:
        http8080 = None
    #
    # try:
    #     https = Https.objects(ip=ip).order_by('-date')[date_position]
    # except IndexError:
    #     https = None

    return render(request, 'graphs/search.html',
                  {'ip': ip,
                   'reverse': reversed_dns[0],
                   'lat': lat,
                   'long': long,
                   'date_position': date_position,
                   'http80': http80,
                   'http443': http443,
                   'http8000': http8000,
                   'http8080': http8080,
                   # 'https': https
                   })
