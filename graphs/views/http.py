from django.db.models import Count, Sum
from django.shortcuts import render
from graphs.models import ZmapLog, HTTP80, HTTP_PORT, HTTP443, HTTP8000, HTTP8080, HTTPServer, HTTPOS
from graphs.util import count, filter_by_name


def http_index(request):
    zmap80 = ZmapLog.objects.filter(port=80)
    zmap443 = ZmapLog.objects.filter(port=443)
    zmap8000 = ZmapLog.objects.filter(port=8000)
    zmap8080 = ZmapLog.objects.filter(port=8080)

    http80 = HTTP80.objects.filter(success=True).values('date').annotate(total=Count('date')).order_by('date')
    http443 = HTTP443.objects.filter(success=True).values('date').annotate(total=Count('date')).order_by('date')
    http8000 = HTTP8000.objects.filter(success=True).values('date').annotate(total=Count('date')).order_by('date')
    http8080 = HTTP8080.objects.filter(success=True).values('date').annotate(total=Count('date')).order_by('date')

    return render(request, 'graphs/http_index.html',
                  {'line': {
                      'title': 'Hosts Hit in Chilean Internet (HTTP)',
                      'xAxis': 'Date of Scan',
                      'yAxis': 'Hits',
                      'series': [
                          {'name': 'Zmap, Port 80', 'data': [[str(i.date), i.recv] for i in zmap80]},
                          {'name': 'Zmap, Port 443', 'data': [[str(i.date), i.recv] for i in zmap443]},
                          {'name': 'Zmap, Port 8000', 'data': [[str(i.date), i.recv] for i in zmap8000]},
                          {'name': 'Zmap, Port 8080', 'data': [[str(i.date), i.recv] for i in zmap8000]},
                          {'name': 'Grabber, Port 80', 'data': [[str(i.get('date')), i.get('total')] for i in http80]},
                          {'name': 'Grabber, Port 443', 'data': [[str(i.get('date')), i.get('total')] for i in http443]},
                          {'name': 'Grabber, Port 8000', 'data': [[str(i.get('date')), i.get('total')] for i in http8000]},
                          {'name': 'Grabber, Port 8080', 'data': [[str(i.get('date')), i.get('total')] for i in http8080]}
                      ]
                  }})


def http_server(request, port, scan_date=None, product=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    # if product:
    #     version_server = HTTPServer.objects.filter(port=port, date=scan_date, product=product)[:9]

    web_server = HTTPServer.objects.filter(port=port, date=scan_date).values('product').order_by('product')\
        .annotate(total=Sum('total')).order_by('-total')[:10]

    return render(request, 'graphs/http_server.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Web Server Running (HTTP)', 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                       'xvalues': [i['product'] for i in web_server],
                       'values': [{'name': 'port ' + port, 'yvalue': [i['total'] for i in web_server]}]},
                   'pie': None
                   })

        # return render(request, 'graphs/http_server.html',
        #               {'port': port,
        #                'scan_date': scan,
        #                'scan_list': [i.date for i in zmap],
        #                'bars': {'title': 'Web Server Running (HTTP)', 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
        #                         'xvalues': [i[0] for i in web_server_frequency],
        #                         'values': [{'name': 'port ' + port, 'yvalue': [i[1] for i in web_server_frequency]}]},
        #                'pie': {'title': version, 'data': version_web_server(port, scan, version)}})


def http_server_all(request, scan_date):
    scan_date_list = ZmapLog.objects.filter(port=80)
    http80 = HTTPServer.objects.filter(port=80, date=scan_date).values('product').order_by('product') \
        .annotate(total=Sum('total')).order_by('-total')[:10]
    http443 = filter_by_name(HTTPServer.objects.filter(port=443, date=scan_date).values('product').order_by('product') \
        .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8000 = filter_by_name(HTTPServer.objects.filter(port=8000, date=scan_date).values('product').order_by('product') \
        .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8080 = filter_by_name(HTTPServer.objects.filter(port=8080, date=scan_date).values('product').order_by('product') \
        .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')

    return render(request, 'graphs/http_server.html',
                  {'port': 'all',
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Web Server Running (HTTP)', 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                            'xvalues': [i['product'] for i in http80],
                            'values': [
                                {'name': 'port 80', 'yvalue': [i['total'] for i in http80]},
                                {'name': 'port 443', 'yvalue': [i['total'] for i in http443]},
                                {'name': 'port 8000', 'yvalue': [i['total'] for i in http8000]},
                                {'name': 'port 8080', 'yvalue': [i['total'] for i in http8080]}
                            ]}
                   })


def operating_system_server(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    operating_system = HTTPOS.objects.filter(port=port, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total')[:10]

    return render(request, 'graphs/operative_systems.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                       'yaxis': 'Number of Servers',
                       'xvalues': [i['os'] for i in operating_system],
                       'values': [{'name': 'port ' + str(port), 'yvalue': [i['total'] for i in operating_system]}]}})


def operating_system_server_all(request, scan_date):
    scan_date_list = ZmapLog.objects.filter(port=80)
    os80 = HTTPOS.objects.filter(port=80, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total')[:10]
    os443 = filter_by_name(HTTPOS.objects.filter(port=443, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')
    os8000 = filter_by_name(HTTPOS.objects.filter(port=8000, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')
    os8080 = filter_by_name(HTTPOS.objects.filter(port=8080, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')

    return render(request, 'graphs/operative_systems.html',
                  {'port': 'all',
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'xvalues': [i['os'] for i in os80],
                            'values': [{'name': 'port 80', 'yvalue': [i['total'] for i in os80]},
                                       {'name': 'port 443', 'yvalue': [i['total'] for i in os443]},
                                       {'name': 'port 8000', 'yvalue': [i['total'] for i in os8000]},
                                       {'name': 'port 8080', 'yvalue': [i['total'] for i in os8080]}]}})



        # def os_server_all(request, scan):
        #     zmap = ZmapLog.objects(port='80')
        #     os80 = accumulate(HttpOperativeSystem.objects(port='80', scan=scan), 'operative_system', sum_value='$count', with_none=False)[:10]
        #     os443 = filter_by_name(accumulate(HttpOperativeSystem.objects(port='443', scan=scan), 'operative_system', sum_value='$count', with_none=False)[:10], [i[0] for i in os80])
        #     os8000 = filter_by_name(accumulate(HttpOperativeSystem.objects(port='8000', scan=scan), 'operative_system', sum_value='$count', with_none=False)[:10], [i[0] for i in os80])
        #     os8080 = filter_by_name(accumulate(HttpOperativeSystem.objects(port='8080', scan=scan), 'operative_system', sum_value='$count', with_none=False)[:10], [i[0] for i in os80])
        #
        #     return render(request, 'graphs/operative_systems.html',
        #                   {'port': 'all',
        #                    'scan_date': scan,
        #                    'scan_list': [i.date for i in zmap],
        #                    'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
        #                             'yaxis': 'Number of Servers',
        #                             'xvalues': [i[0] for i in os80],
        #                             'values': [{'name': 'port 80', 'yvalue': [i[1] for i in os80]},
        #                                        {'name': 'port 443', 'yvalue': [i[1] for i in os443]},
        #                                        {'name': 'port 8000', 'yvalue': [i[1] for i in os8000]},
        #                                        {'name': 'port 8080', 'yvalue': [i[1] for i in os8080]}]}})
        #
        #
        # def device_type(request, port, scan):
        #     zmap = ZmapLog.objects(port=port)
        #     device = accumulate(HttpDeviceType.objects(port=port, scan=scan), 'device_type', sum_value='$count', with_none=False)[:10]
        #
        #     return render(request, 'graphs/device_type.html',
        #                   {'port': port,
        #                    'scan_date': scan,
        #                    'scan_list': [i.date for i in zmap],
        #                    'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
        #                             'yaxis': 'Number of Servers',
        #                             'xvalues': [i[0] for i in device],
        #                             'values': [{'name': 'port ' + str(port), 'yvalue': [i[1] for i in device]}]}})
        #
        #
        # def device_type_all(request, scan):
        #     zmap = ZmapLog.objects(port='80')
        #     device80 = accumulate(HttpDeviceType.objects(port='80', scan=scan), 'device_type', sum_value='$count', with_none=False)[:10]
        #     device443 = filter_by_name(accumulate(HttpDeviceType.objects(port='443', scan=scan), 'device_type', sum_value='$count', with_none=False)[:10], [i[0] for i in device80])
        #     device8000 = filter_by_name(accumulate(HttpDeviceType.objects(port='8000', scan=scan), 'device_type', sum_value='$count', with_none=False)[:10], [i[0] for i in device80])
        #     device8080 = filter_by_name(accumulate(HttpDeviceType.objects(port='8080', scan=scan), 'device_type', sum_value='$count', with_none=False)[:10], [i[0] for i in device80])
        #
        #     return render(request, 'graphs/device_type.html',
        #                   {'port': 'all',
        #                    'scan_date': scan,
        #                    'scan_list': [i.date for i in zmap],
        #                    'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
        #                             'yaxis': 'Number of Servers',
        #                             'xvalues': [i[0] for i in device80],
        #                             'values': [{'name': 'port 80', 'yvalue': [i[1] for i in device80]},
        #                                        {'name': 'port 443', 'yvalue': [i[1] for i in device443]},
        #                                        {'name': 'port 8000', 'yvalue': [i[1] for i in device8000]},
        #                                        {'name': 'port 8080', 'yvalue': [i[1] for i in device8080]}]}})