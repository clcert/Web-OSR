from django.db.models import Sum
from django.shortcuts import render

from graphs.models import ZmapLog, HTTPSKeyBits, HTTPSSignature, HTTPSCipherSuite, HTTPSTlsProtocol
from graphs.util import filter_by_name


def key_bits(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
            scan_date = scan_date_list.last().date

    trusted = HTTPSKeyBits.objects.filter(port=port, date=scan_date, valid=True).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]
    untrusted = HTTPSKeyBits.objects.filter(port=port, date=scan_date, valid=False).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]

    key_bits_values = sorted(set([i['bits'] for i in trusted]) | set([i['bits'] for i in untrusted]))

    return render(request, 'graphs/cert_key_bits.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Key Bits (HTTPS)',
                       'xaxis': 'Bits',
                       'yaxis': 'Number of Certificates',
                       'categories': [i for i in key_bits_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, key_bits_values, 'bits', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, key_bits_values, 'bits', 'total')]}
                       ]
                   }})


def validation(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    certificate_validation = HTTPSKeyBits.objects.filter(port=port, date=scan_date).values('valid').order_by('valid') \
        .annotate(total=Sum('total')).order_by('valid')

    return render(request, 'graphs/cert_validation.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Certificate Validation (HTTP)',
                       'xaxis': 'Validation',
                       'yaxis': 'Number of Certificates',
                       'categories': [i['valid'] for i in certificate_validation],
                       'values': [{'name': 'https', 'data': [i['total'] for i in certificate_validation]}]}})


def signature(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = HTTPSSignature.objects.filter(port=port, date=scan_date, valid=True).values('signature').order_by('signature') \
        .annotate(total=Sum('total')).order_by('signature')[:10]
    untrusted = HTTPSSignature.objects.filter(port=port, date=scan_date, valid=False).values('signature').order_by('signature') \
        .annotate(total=Sum('total')).order_by('signature')[:10]

    signature_values = sorted(set([i['signature'] for i in trusted]) | set([i['signature'] for i in untrusted]))

    return render(request, 'graphs/cert_signature.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Signature',
                       'xaxis': 'Signature Algorithm',
                       'yaxis': 'Number of Handshake',
                       'label_rotation': -45,
                       'categories': [i for i in signature_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, signature_values, 'signature', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, signature_values, 'signature', 'total')]}
                       ]
                   }})


def cipher_suite(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = HTTPSCipherSuite.objects.filter(port=port, date=scan_date, valid=True).values('cipher_suite').order_by('cipher_suite') \
        .annotate(total=Sum('total')).order_by('cipher_suite')
    untrusted = HTTPSCipherSuite.objects.filter(port=port, date=scan_date, valid=False).values('cipher_suite').order_by('cipher_suite') \
        .annotate(total=Sum('total')).order_by('cipher_suite')

    cipher_suite_values = sorted(set([i['cipher_suite'] for i in trusted]) | set([i['cipher_suite'] for i in untrusted]))

    return render(request, 'graphs/cert_cipher_suite.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Cipher Suites',
                       'xaxis': 'Cipher Suite',
                       'yaxis': 'Number of Handshake',
                       'label_rotation': -90,
                       'categories': [i for i in cipher_suite_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, cipher_suite_values, 'cipher_suite', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, cipher_suite_values, 'cipher_suite', 'total')]}
                       ]
                   }})


def tls_version(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    trusted = HTTPSTlsProtocol.objects.filter(port=port, date=scan_date, valid=True).values('protocol').order_by('protocol') \
        .annotate(total=Sum('total')).order_by('protocol')
    untrusted = HTTPSTlsProtocol.objects.filter(port=port, date=scan_date, valid=False).values('protocol').order_by('protocol') \
        .annotate(total=Sum('total')).order_by('protocol')

    tls_values = sorted(set([i['protocol'] for i in trusted]) | set([i['protocol'] for i in untrusted]))

    return render(request, 'graphs/cert_tls_version.html',
                  {'port': port,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Cipher Suites',
                       'xaxis': 'TLS Version',
                       'yaxis': 'Number of Handshake',
                       'categories': [i for i in tls_values],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, tls_values, 'protocol', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, tls_values, 'protocol', 'total')]}
                       ]
                   }})




