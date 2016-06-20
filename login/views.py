from django.shortcuts import render

from graphs.models import ZmapLog


def index(request):
    http_scan_date = ZmapLog.objects.filter(port=80).last().date
    https_scan_date = ZmapLog.objects.filter(port=443).last().date
    scans = ZmapLog.objects.order_by('port', '-date').distinct('port')[:10]

    return render(request, 'index.html',
                  {'http_scan_date': http_scan_date,
                   'https_scan_date': https_scan_date,
                   'scans': scans})
