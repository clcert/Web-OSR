from operator import itemgetter

from django.shortcuts import render

from graphs.models import Http80, Http8000, ZmapLog, Http443, Http8080

port_dict = {
    '80': Http80,
    '443': Http443,
    '8000': Http8000,
    '8080': Http8080
}


def filter_by_name(data, names):
    filtered_list = list()

    for name in names:
        total = 0
        for elem in data:
            if name == elem[0]:
                total = elem[1]
                break
        filtered_list.append((name, total))
    return filtered_list


def add_other(data):
    sum = 0
    for elem in data:
        sum += elem[1]
    data.append(('Other', 1 - sum))

    return data


def accumulate(mongo_collections, query, sorted_by=1, reverse=True, with_none=True, percentage=False):
    freqs = mongo_collections.aggregate({'$group': {'_id': '$' + query, 'total': {'$sum': 1}}})

    freqs_dict = dict()
    for freq in freqs:
        if with_none or freq['_id'] is not None:
            freqs_dict[freq['_id']] = freq['total']

    if percentage:
        sum = 0
        for key, value in freqs_dict.iteritems():
            sum += value

        sum = float(sum)
        for key, value in freqs_dict.iteritems():
            freqs_dict[key] = value / sum
    return sorted(freqs_dict.items(), key=itemgetter(sorted_by), reverse=reverse)


def version_web_server(port, scan, version):
    version_data = None
    if version:
        version_data = add_other(accumulate(port_dict[port].objects(date=scan, metadata__service__product=version),
                                            'metadata.service.version', percentage=True)[:9])
    return version_data


def index(request):
    zmap80 = ZmapLog.objects(port='80')
    zmap443 = ZmapLog.objects(port='443')
    zmap8000 = ZmapLog.objects(port='8000')
    zmap8080 = ZmapLog.objects(port='8080')

    http80 = accumulate(Http80.objects(header__exists=True).only('date'), 'date', sorted_by=0, reverse=False)
    http443 = accumulate(Http443.objects(header__exists=True).only('date'), 'date', sorted_by=0, reverse=False)
    http8000 = accumulate(Http8000.objects(header__exists=True).only('date'), 'date', sorted_by=0, reverse=False)
    http8080 = accumulate(Http8080.objects(header__exists=True).only('date'), 'date', sorted_by=0, reverse=False)

    return render(request, 'graphs/index.html',
                  {'line': {
                      'title': 'Hosts Hit in Chilean Internet (HTTP)',
                      'xAxis': 'Date of Scan',
                      'yAxis': 'Hits',
                      'series': [{'name': 'Zmap, Port 80', 'data': [[i.date, i.recv] for i in zmap80]},
                                 {'name': 'Zmap, Port 443', 'data': [[i.date, i.recv] for i in zmap443]},
                                 {'name': 'Zmap, Port 8000', 'data': [[i.date, i.recv] for i in zmap8000]},
                                 {'name': 'Zmap, Port 8080', 'data': [[i.date, i.recv] for i in zmap8080]},
                                 {'name': 'Grabber, Port 80', 'data': [[i[0], i[1]] for i in http80]},
                                 {'name': 'Grabber, Port 443', 'data': [[i[0], i[1]] for i in http443]},
                                 {'name': 'Grabber, Port 8000', 'data': [[i[0], i[1]] for i in http8000]},
                                 {'name': 'Grabber, Port 8080', 'data': [[i[0], i[1]] for i in http8080]}]
                  }})


def http_server(request, port, scan, version=None):
    # Database Query
    zmap = ZmapLog.objects(port=port)
    web_server_frequency = accumulate(port_dict[port].objects(date=scan), 'metadata.service.product', with_none=False)[
                           :10]

    return render(request, 'graphs/http_server.html',
                  {'port': port,
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Web Server Running (HTTP)', 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                            'xvalues': [i[0] for i in web_server_frequency],
                            'values': [{'name': 'port ' + port, 'yvalue': [i[1] for i in web_server_frequency]}]},
                   'pie': {'title': version, 'data': version_web_server(port, scan, version)}})


def http_server_all(request, scan):
    zmap = ZmapLog.objects(port='80')
    http80 = accumulate(Http80.objects(date=scan), 'metadata.service.product', with_none=False)[:10]
    name = [i[0] for i in http80]
    http443 = filter_by_name(accumulate(Http443.objects(date=scan), 'metadata.service.product', with_none=False)[:10], name)
    http8000 = filter_by_name(accumulate(Http8000.objects(date=scan), 'metadata.service.product', with_none=False)[:10], name)
    http8080 = filter_by_name(accumulate(Http8080.objects(date=scan), 'metadata.service.product', with_none=False)[:10], name)

    return render(request, 'graphs/http_server.html',
                  {'port': 'all',
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Web Server Running (HTTP)', 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port 80', 'yvalue': [i[1] for i in http80]},
                                       {'name': 'port 443', 'yvalue': [i[1] for i in http443]},
                                       {'name': 'port 8000', 'yvalue': [i[1] for i in http8000]},
                                       {'name': 'port 8080', 'yvalue': [i[1] for i in http8080]}]}
                   })


def os_server(request, port=80):
    frequency = accumulate(port_dict[port].objects(date='2015-11-30'), 'metadata.device.os', with_none=False)[:10]
    name = [i[0] for i in frequency]
    return render(request, 'graphs/operative_systems.html',
                  {'port': port,
                   'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port ' + str(port), 'yvalue': [i[1] for i in frequency]}]}})


def os_server_all(request):
    frequency_80 = accumulate(Http80.objects(date='2015-11-30'), 'metadata.device.os', with_none=False)[:10]
    name = [i[0] for i in frequency_80]
    frequency_8000 = filter_by_name(accumulate(Http8000.objects, 'metadata.device.os', with_none=False)[:10], name)

    return render(request, 'graphs/operative_systems.html',
                  {'port': 'all',
                   'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port 80', 'yvalue': [i[1] for i in frequency_80]},
                                       {'name': 'port 8000', 'yvalue': [i[1] for i in frequency_8000]}]}})


def device_type(request, port=80):
    frequency = accumulate(port_dict[port].objects(date='2015-11-30'), 'metadata.device.type', with_none=False)[:10]
    name = [i[0] for i in frequency]
    return render(request, 'graphs/device_type.html',
                  {'port': port,
                   'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port ' + str(port), 'yvalue': [i[1] for i in frequency]}]}})


def device_type_all(request):
    frequency_80 = accumulate(Http80.objects(date='2015-11-30'), 'metadata.device.type', with_none=False)[:10]
    name = [i[0] for i in frequency_80]
    frequency_8000 = filter_by_name(accumulate(Http8000.objects, 'metadata.device.type', with_none=False)[:10], name)

    return render(request, 'graphs/device_type.html',
                  {'port': 'all',
                   'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port 80', 'yvalue': [i[1] for i in frequency_80]},
                                       {'name': 'port 8000', 'yvalue': [i[1] for i in frequency_8000]}]}})
