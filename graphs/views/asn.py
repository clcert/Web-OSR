from django.shortcuts import render
from graphs.models import asn, ZmapLog, AsnHTTPServer, AsnHTTPOS, AsnHTTPType, AsnHTTPSKeyBits, AsnHTTPSCipherSuite, AsnHTTPSSignature, AsnHTTPSTlsProtocol, Asn
from django.db.models import Sum
from django.db.models import Q
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from graphs.util import filter_by_name
import ast


def top_asn(request):
    full_data = asn.Asn.objects.all()
    for data in full_data:
        data.block_size = data.number_of_addresses()
    full_data = sorted(full_data, key=operator.attrgetter('block_size'), reverse=True)

    paginator = Paginator(full_data, 25)
    page = request.GET.get('page')
    try:
        partial_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        partial_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        partial_data = paginator.page(paginator.num_pages)
    return render(request, 'graphs/asn.html',
              {'page_title': 'Top Autonomous Systems',
               'panel_title': 'Number of ip addresses per ASN',
               'bars': {'title': 'Number of ip addresses per ASN', 'yaxis': 'Number of ips', 'xaxis': 'Autonomous Systems',
                        # yaxis y xaxis estan cambiados en el chart
                        'xvalues': [i.name.split(',')[0] + str(i.number) for i in partial_data],
                        'values': [{'name': "Number of assigned ip addresses ", 'yvalue': [i.block_size for i in partial_data]}]},
                        'partial_data': partial_data,

               })


def http_server_asn_search(request):
    if request.POST.get('number'):
        try: # transforma el string 12345;13450 a [12345, 13450]
            number = request.POST['number']
            number = number.split(';')
            number = map(int, number)
            return http_server_all_asn(request, number)
        except ValueError:
            pass
    return render(request, 'graphs/http_server_asn.html')


def http_server_asn(request, number, port, scan_date=None, product=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    # if product:
    #     version_server = HTTPServer.objects.filter(port=port, date=scan_date, product=product)[:9]
    print number
    web_server = filter_multiple_numbers(number, AsnHTTPServer.objects).filter(port=port, date=scan_date).values('product').order_by('product')\
        .annotate(total=Sum('total')).order_by('-total')[:10]

    return render(request, 'graphs/http_server_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Web Server Running (HTTP) on Autonomous System %s' % number, 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                       'categories': [i['product'] for i in web_server],
                       'values': [{'name': 'port ' + port, 'data': [i['total'] for i in web_server]}]},
                   'pie': None
                   })


def http_server_all_asn(request, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=80)
    if scan_date is None:
        # NO FUNCIONARA HASTA QUE TENGAMOS TODOS LOS DATOS TRANSFORMEITED!
        # Para ver como queda usar first() en vez de last()
        scan_date = scan_date_list.last().date
    if not number:
        try:
            number = int(request.POST['number'])
            print reverse('graphs/asn/server/all', kwargs={'number': number, 'scan_date': scan_date})
            return HttpResponseRedirect(reverse('graphs/asn/server/all', kwargs={'number': number, 'scan_date': scan_date}))
        except ValueError:
            return HttpResponseRedirect(reverse('graphs/asn/server/all'))

    http80 = filter_multiple_numbers(number, AsnHTTPServer.objects).filter(port=80, date=scan_date).values('product').order_by('product') \
                 .annotate(total=Sum('total')).order_by('-total')[:10]
    http443 = filter_by_name(filter_multiple_numbers(number, AsnHTTPServer.objects).filter(port=443, date=scan_date).values('product').order_by('product') \
                             .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8000 = filter_by_name(filter_multiple_numbers(number, AsnHTTPServer.objects).filter(port=8000, date=scan_date).values('product').order_by('product') \
                              .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8080 = filter_by_name(filter_multiple_numbers(number, AsnHTTPServer.objects).filter(port=8080, date=scan_date).values('product').order_by('product') \
                              .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')

    return render(request, 'graphs/http_server_asn.html',
                  {'port': 'all',
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Web Server Running (HTTP) on Autonomous System %s' % number, 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                            'categories': [i['product'] for i in http80],
                            'values': [
                                {'name': 'port 80', 'data': [i['total'] for i in http80]},
                                {'name': 'port 443', 'data': [i['total'] for i in http443]},
                                {'name': 'port 8000', 'data': [i['total'] for i in http8000]},
                                {'name': 'port 8080', 'data': [i['total'] for i in http8080]}
                            ]}
                   })


def device_type_asn_search(request, port=80):
    if request.POST.get('number'):
        try: # transforma el string 12345;13450 a [12345, 13450]
            number = request.POST['number']
            number = number.split(';')
            number = map(int, number)
            return device_type_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/http_device_type_asn.html')


def device_type_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date
    device = filter_multiple_numbers(number, AsnHTTPType.objects).filter(port=port, date=scan_date).values('type').order_by('type') \
        .annotate(total=Sum('total')).order_by('-total')[:10]
    return render(request, 'graphs/http_device_type_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Device Type of Server (HTTP) on Autonomous System %s' % number, 'xaxis': 'Type of Device',
                       'yaxis': 'Number of Servers',
                       'categories': [i['type'] for i in device],
                       'values': [{'name': 'port ' + str(port), 'data': [i['total'] for i in device]}]}})


def device_type_asn_all(request, number, scan_date):
    scan_date_list = ZmapLog.objects.filter(port=80)
    device80 = filter_multiple_numbers(number, AsnHTTPType.objects).filter(port=80, date=scan_date).values('type').order_by('type') \
                            .annotate(total=Sum('total')).order_by('-total')[:10]
    device443 = filter_by_name(filter_multiple_numbers(number, AsnHTTPType.objects).filter(port=443, date=scan_date).values('type').order_by('type') \
                           .annotate(total=Sum('total')).order_by('-total'), [i['type'] for i in device80], 'type', 'total')
    device8000 = filter_by_name(filter_multiple_numbers(number, AsnHTTPType.objects).filter(port=8000, date=scan_date).values('type').order_by('type') \
                            .annotate(total=Sum('total')).order_by('-total'), [i['type'] for i in device80], 'type', 'total')
    device8080 = filter_by_name(filter_multiple_numbers(number, AsnHTTPType.objects).filter(port=8080, date=scan_date).values('type').order_by('type') \
                            .annotate(total=Sum('total')).order_by('-total'), [i['type'] for i in device80], 'type', 'total')

    return render(request, 'graphs/http_device_type_asn.html',
                  {'port': 'all',
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Device Type of Server (HTTP) on Autonomous System %s' % number, 'xaxis': 'Type of Device',
                            'yaxis': 'Number of Servers',
                            'categories': [i['type'] for i in device80],
                            'values': [{'name': 'port 80', 'data': [i['total'] for i in device80]},
                                       {'name': 'port 443', 'data': [i['total'] for i in device443]},
                                       {'name': 'port 8000', 'data': [i['total'] for i in device8000]},
                                       {'name': 'port 8080', 'data': [i['total'] for i in device8080]}]}})


def operating_system_server_asn_search(request, port=80):
    if request.POST.get('number'):
        try: # transforma el string 12345;13450 a [12345, 13450]
            number = request.POST['number']
            number = number.split(';')
            number = map(int, number)
            return operating_system_server_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/http_operative_systems_asn.html')


def operating_system_server_asn(request, port=80, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date
    operating_system = filter_multiple_numbers(number, AsnHTTPOS.objects).filter(port=port, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total')[:10]

    return render(request, 'graphs/http_operative_systems_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Operative System of Server (HTTP) on Autonomous System %s' % number, 'xaxis': 'Operative Systems',
                       'yaxis': 'Number of Servers',
                       'categories': [i['os'] for i in operating_system],
                       'values': [{'name': 'port ' + str(port), 'data': [i['total'] for i in operating_system]}]}})


def operating_system_server_asn_all(request, number, scan_date):
    scan_date_list = ZmapLog.objects.filter(port=80)
    os80 = filter_multiple_numbers(number, AsnHTTPOS.objects).filter(port=80, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total')[:10]
    os443 = filter_by_name(filter_multiple_numbers(number, AsnHTTPOS.objects).filter(port=443, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')
    os8000 = filter_by_name(filter_multiple_numbers(number, AsnHTTPOS.objects).filter(port=8000, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')
    os8080 = filter_by_name(filter_multiple_numbers(number, AsnHTTPOS.objects).filter(port=8080, date=scan_date).values('os').order_by('os') \
        .annotate(total=Sum('total')).order_by('-total'), [i['os'] for i in os80], 'os', 'total')

    return render(request, 'graphs/http_operative_systems_asn.html',
                  {'port': 'all',
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Operative System of Server (HTTP) on Autonomous System %s' % number, 'xaxis': 'Operative Systems',
                            'yaxis': 'Number of Servers',
                            'categories': [i['os'] for i in os80],
                            'values': [{'name': 'port 80', 'data': [i['total'] for i in os80]},
                                       {'name': 'port 443', 'data': [i['total'] for i in os443]},
                                       {'name': 'port 8000', 'data': [i['total'] for i in os8000]},
                                       {'name': 'port 8080', 'data': [i['total'] for i in os8080]}]}})


def key_bits_asn_search(request, port=443):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return key_bits_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/cert_key_bits_asn.html')


def key_bits_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
            scan_date = scan_date_list.last().date

    trusted = AsnHTTPSKeyBits.objects.filter(asn=number, port=port, date=scan_date, valid=True).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]
    untrusted = AsnHTTPSKeyBits.objects.filter(asn=number, port=port, date=scan_date, valid=False).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]

    key_bits_values = sorted(set([i['bits'] for i in trusted]) | set([i['bits'] for i in untrusted]))

    return render(request, 'graphs/cert_key_bits_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Key Bits (HTTPS) on Autonomous System %s' % number,
                       'xaxis': 'Bits',
                       'yaxis': 'Number of Certificates',
                       'categories': [i for i in key_bits_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, key_bits_values, 'bits', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, key_bits_values, 'bits', 'total')]}
                       ]
                   }})


def validation_asn_search(request, port=443):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return validation_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/cert_validation_asn.html')


def validation_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    certificate_validation = AsnHTTPSKeyBits.objects.filter(asn=number, port=port, date=scan_date).values('valid').order_by('valid') \
        .annotate(total=Sum('total')).order_by('valid')

    return render(request, 'graphs/cert_validation_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Certificate Validation (HTTP) on Autonomous System %s' % number,
                       'xaxis': 'Validation',
                       'yaxis': 'Number of Certificates',
                       'categories': [i['valid'] for i in certificate_validation],
                       'values': [{'name': 'https', 'data': [i['total'] for i in certificate_validation]}]}})


def signature_asn_search(request, port=443):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return validation_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/cert_signature_asn.html')


def signature_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = AsnHTTPSSignature.objects.filter(asn=number, port=port, date=scan_date, valid=True).values('signature').order_by('signature') \
        .annotate(total=Sum('total')).order_by('signature')[:10]
    untrusted = AsnHTTPSSignature.objects.filter(asn=number, port=port, date=scan_date, valid=False).values('signature').order_by('signature') \
        .annotate(total=Sum('total')).order_by('signature')[:10]

    signature_values = sorted(set([i['signature'] for i in trusted]) | set([i['signature'] for i in untrusted]))

    return render(request, 'graphs/cert_signature_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Signature on Autonomous System %s' % number,
                       'xaxis': 'Signature Algorithm',
                       'yaxis': 'Number of Handshake',
                       'label_rotation': -45,
                       'categories': [i for i in signature_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, signature_values, 'signature', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, signature_values, 'signature', 'total')]}
                       ]
                   }})


def cipher_suite_asn_search(request, port=443):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return cipher_suite_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/cert_cipher_suite_asn.html')


def cipher_suite_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = AsnHTTPSCipherSuite.objects.filter(asn=number, port=port, date=scan_date, valid=True).values('cipher_suite').order_by('cipher_suite') \
        .annotate(total=Sum('total')).order_by('cipher_suite')
    untrusted = AsnHTTPSCipherSuite.objects.filter(asn=number, port=port, date=scan_date, valid=False).values('cipher_suite').order_by('cipher_suite') \
        .annotate(total=Sum('total')).order_by('cipher_suite')

    cipher_suite_values = sorted(set([i['cipher_suite'] for i in trusted]) | set([i['cipher_suite'] for i in untrusted]))

    return render(request, 'graphs/cert_cipher_suite_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Cipher Suites on Autonomous System %s' % number,
                       'xaxis': 'Cipher Suite',
                       'yaxis': 'Number of Handshake',
                       'label_rotation': -90,
                       'categories': [i for i in cipher_suite_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, cipher_suite_values, 'cipher_suite', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, cipher_suite_values, 'cipher_suite', 'total')]}
                       ]
                   }})


def tls_version_asn_search(request, port=443):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return tls_version_asn(request, port, number)
        except ValueError:
            pass
    return render(request, 'graphs/cert_tls_version_asn.html')


def tls_version_asn(request, port, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = AsnHTTPSTlsProtocol.objects.filter(asn=number, port=port, date=scan_date, valid=True).values('protocol').order_by('protocol') \
        .annotate(total=Sum('total')).order_by('protocol')
    untrusted = AsnHTTPSTlsProtocol.objects.filter(asn=number, port=port, date=scan_date, valid=False).values('protocol').order_by('protocol') \
        .annotate(total=Sum('total')).order_by('protocol')

    tls_values = sorted(set([i['protocol'] for i in trusted]) | set([i['protocol'] for i in untrusted]))

    return render(request, 'graphs/cert_tls_version_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Cipher Suites on Autonomous System %s' % number,
                       'xaxis': 'TLS Version',
                       'yaxis': 'Number of Handshake',
                       'categories': [i for i in tls_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, tls_values, 'protocol', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, tls_values, 'protocol', 'total')]}
                       ]
                   }})


def filter_multiple_numbers(numbers = None, model_objects = None):
    if numbers[0] == '[':
        numbers = ast.literal_eval(numbers)
    list_of_Q = [Q(**{'asn': num}) for num in numbers]
    return model_objects.filter(reduce(operator.or_, list_of_Q))
