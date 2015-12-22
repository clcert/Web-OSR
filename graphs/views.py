from operator import itemgetter
from django.shortcuts import render
from graphs.models import Http80, Http8000, ZmapLog, Http443, Http8080, GrabberScan, Https, HttpWebServer, \
    HttpOperativeSystem, HttpDeviceType

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


def complete_bars_chart(value_name, value_list):
    """
    :type value_list: list
    :type value_name: set
    """
    new_set = value_name - set([i[0] for i in value_list])
    for elem in new_set:
        value_list.append((elem, 0))

    return value_list


def add_other(data):
    sum = 0
    for elem in data:
        sum += elem[1]
    data.append(('Other', 1 - sum))

    return data


def accumulate(mongo_collections, query, sum_value=1, reverse=True, with_none=True, percentage=False):
    freqs = mongo_collections.aggregate({'$group': {'_id': '$' + query, 'total': {'$sum': sum_value}}})

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
    return sorted(freqs_dict.items(), key=itemgetter(1), reverse=reverse)


def version_web_server(port, scan, version):
    version_data = None
    if version:
        version_data = add_other(accumulate(port_dict[port].objects(date=scan, metadata__service__product=version),
                                            'metadata.service.version', percentage=True)[:9])
    return version_data


def date_to_yyyy_mm_dd(date):
    return str(date.year) + '-' + str(date.month) + '-' + str(date.day)


def index(request):
    return render(request, 'graphs/index.html')


def http_index(request):
    zmap80 = ZmapLog.objects(port='80')
    zmap443 = ZmapLog.objects(port='443')
    zmap8000 = ZmapLog.objects(port='8000')
    zmap8080 = ZmapLog.objects(port='8080')

    http80 = GrabberScan.objects(port='80')
    http443 = GrabberScan.objects(port='443')
    http8000 = GrabberScan.objects(port='8000')
    http8080 = GrabberScan.objects(port='8080')

    return render(request, 'graphs/http_index.html',
                  {'line': {
                      'title': 'Hosts Hit in Chilean Internet (HTTP)',
                      'xAxis': 'Date of Scan',
                      'yAxis': 'Hits',
                      'series': [{'name': 'Zmap, Port 80', 'data': [[i.date, i.recv] for i in zmap80]},
                                 {'name': 'Zmap, Port 443', 'data': [[i.date, i.recv] for i in zmap443]},
                                 {'name': 'Zmap, Port 8000', 'data': [[i.date, i.recv] for i in zmap8000]},
                                 {'name': 'Zmap, Port 8080', 'data': [[i.date, i.recv] for i in zmap8080]},
                                 {'name': 'Grabber, Port 80',
                                  'data': [[date_to_yyyy_mm_dd(i.date), i.amount] for i in http80]},
                                 {'name': 'Grabber, Port 443',
                                  'data': [[date_to_yyyy_mm_dd(i.date), i.amount] for i in http443]},
                                 {'name': 'Grabber, Port 8000',
                                  'data': [[date_to_yyyy_mm_dd(i.date), i.amount] for i in http8000]},
                                 {'name': 'Grabber, Port 8080',
                                  'data': [[date_to_yyyy_mm_dd(i.date), i.amount] for i in http8080]}]
                  }})


def http_server(request, port, scan, version=None):
    # Database Query
    zmap = ZmapLog.objects(port=port)
    web_server_frequency = accumulate(HttpWebServer.objects(port=port, scan=scan), 'product', sum_value='$count',
                                      with_none=False)[:10]

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
    http443 = filter_by_name(accumulate(Http443.objects(date=scan), 'metadata.service.product', with_none=False)[:10],
                             name)
    http8000 = filter_by_name(accumulate(Http8000.objects(date=scan), 'metadata.service.product', with_none=False)[:10],
                              name)
    http8080 = filter_by_name(accumulate(Http8080.objects(date=scan), 'metadata.service.product', with_none=False)[:10],
                              name)

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


def os_server(request, port, scan):
    zmap = ZmapLog.objects(port=port)
    os = accumulate(HttpOperativeSystem.objects(port=port, scan=scan), 'operative_system', sum_value='$count',
                    with_none=False)[:10]

    return render(request, 'graphs/operative_systems.html',
                  {'port': port,
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'xvalues': [i[0] for i in os],
                            'values': [{'name': 'port ' + str(port), 'yvalue': [i[1] for i in os]}]}})


def os_server_all(request, scan):
    zmap = ZmapLog.objects(port='80')
    os80 = accumulate(Http80.objects(date=scan), 'metadata.device.os', with_none=False)[:10]
    name = [i[0] for i in os80]
    os443 = filter_by_name(accumulate(Http443.objects(date=scan), 'metadata.device.os', with_none=False)[:10], name)
    os8000 = filter_by_name(accumulate(Http8000.objects(date=scan), 'metadata.device.os', with_none=False)[:10], name)
    os8080 = filter_by_name(accumulate(Http8080.objects(date=scan), 'metadata.device.os', with_none=False)[:10], name)

    return render(request, 'graphs/operative_systems.html',
                  {'port': 'all',
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Operative System of Server (HTTP)', 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port 80', 'yvalue': [i[1] for i in os80]},
                                       {'name': 'port 443', 'yvalue': [i[1] for i in os443]},
                                       {'name': 'port 8000', 'yvalue': [i[1] for i in os8000]},
                                       {'name': 'port 8080', 'yvalue': [i[1] for i in os8080]}]}})


def device_type(request, port, scan):
    zmap = ZmapLog.objects(port=port)
    device = accumulate(HttpDeviceType.objects(port=port, scan=scan), 'device_type', sum_value='$count', with_none=False)[:10]

    return render(request, 'graphs/device_type.html',
                  {'port': port,
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
                            'yaxis': 'Number of Servers',
                            'xvalues': [i[0] for i in device],
                            'values': [{'name': 'port ' + str(port), 'yvalue': [i[1] for i in device]}]}})


def device_type_all(request, scan):
    zmap = ZmapLog.objects(port='80')
    device80 = accumulate(Http80.objects(date=scan), 'metadata.device.type', with_none=False)[:10]
    name = [i[0] for i in device80]
    device443 = filter_by_name(accumulate(Http443.objects(date=scan), 'metadata.device.type', with_none=False)[:10],
                               name)
    device8000 = filter_by_name(accumulate(Http8000.objects(date=scan), 'metadata.device.type', with_none=False)[:10],
                                name)
    device8080 = filter_by_name(accumulate(Http8080.objects(date=scan), 'metadata.device.type', with_none=False)[:10],
                                name)

    return render(request, 'graphs/device_type.html',
                  {'port': 'all',
                   'scan_date': scan,
                   'scan_list': [i.date for i in zmap],
                   'bars': {'title': 'Device Type of Server (HTTP)', 'xaxis': 'Type of Device',
                            'yaxis': 'Number of Servers',
                            'xvalues': name,
                            'values': [{'name': 'port 80', 'yvalue': [i[1] for i in device80]},
                                       {'name': 'port 443', 'yvalue': [i[1] for i in device443]},
                                       {'name': 'port 8000', 'yvalue': [i[1] for i in device8000]},
                                       {'name': 'port 8080', 'yvalue': [i[1] for i in device8080]}]}})


def certificate_key_bits(request):
    key_bits_443_trusted = accumulate(Https.objects(valid=True), 'keyBits', with_none=False)[:10]
    key_bits_443_untrusted = accumulate(Https.objects(valid=False), 'keyBits', with_none=False)[:10]

    value_name = set([i[0] for i in key_bits_443_trusted]) | set([i[0] for i in key_bits_443_untrusted])
    key_bits_443_trusted = complete_bars_chart(value_name, key_bits_443_trusted)
    key_bits_443_untrusted = complete_bars_chart(value_name, key_bits_443_untrusted)

    key_bits_443_trusted = sorted(key_bits_443_trusted, key=lambda tup: int(tup[0]))
    key_bits_443_untrusted = sorted(key_bits_443_untrusted, key=lambda tup: int(tup[0]))

    return render(request, 'graphs/cert_key_bits.html',
                  {'bars': {'title': 'Key Bits (HTTPS)', 'xaxis': 'Bits', 'yaxis': 'Number of Certificates',
                            'xvalues': [i[0] for i in key_bits_443_trusted],
                            'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in key_bits_443_trusted]},
                                       {'name': 'https untrusted', 'yvalue': [i[1] for i in key_bits_443_untrusted]}]}})


def certificate_validation(request):
    key_bits_443 = accumulate(Https.objects(), 'validate', with_none=False)[:10]

    return render(request, 'graphs/cert_key_bits.html',
                  {'bars': {'title': 'Certificate Validation (HTTP)', 'xaxis': 'Validation',
                            'yaxis': 'Number of Certificates',
                            'xvalues': [i[0] for i in key_bits_443],
                            'values': [{'name': 'https', 'yvalue': [i[1] for i in key_bits_443]}]}})


def certificate_signature(request):
    signature = accumulate(Https.objects, 'signatureAlgorithm')
