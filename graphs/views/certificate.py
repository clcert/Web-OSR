from django.db.models import Sum
from django.shortcuts import render

from graphs.models import ZmapLog, HTTPSKeyBits, HTTPSSignature, HTTPSCipherSuite
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

    return render(request, 'graphs/certificate.html',
                  {'page_title': 'HTTPs Protocol Key Bits', 'panel_title': 'HTTPS Certificates Key Bits',
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

    return render(request, 'graphs/certificate.html',
                  {'page_title': 'HTTPS Certificate Validation', 'panel_title': 'Scanned in 11/11/11',
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

    return render(request, 'graphs/certificate.html',
                  {'page_title': 'HTTPS Certificate Signature',
                   'panel_title': 'Scanned in 11/11/11',
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

    return render(request, 'graphs/certificate.html',
                  {'page_title': 'HTTPS Certificate Cipher Suites',
                   'panel_title': 'Scanned in 11/11/11',
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


# def certificate_cipher_suite(request):
#     cipher_suite_trusted = accumulate(Https.objects(valid=True), 'cipher_suite', with_none=False)[:10]
#     cipher_suite_untrusted = accumulate(Https.objects(valid=False), 'cipher_suite', with_none=False)[:10]
#
#     value_name = set([i[0] for i in cipher_suite_trusted]) | set([i[0] for i in cipher_suite_untrusted])
#     cipher_suite_trusted = complete_bars_chart(value_name, cipher_suite_trusted)
#     cipher_suite_untrusted = complete_bars_chart(value_name, cipher_suite_untrusted)
#
#     cipher_suite_trusted = sorted(cipher_suite_trusted, key=lambda tup: tup[0])
#     cipher_suite_untrusted = sorted(cipher_suite_untrusted, key=lambda tup: tup[0])
#
#     return render(request, 'graphs/certificate.html',
#                   {'page_title': 'HTTPS Certificate Cipher Suites', 'panel_title': 'Scanned in 11/11/11',
#                    'bars': {'title': 'Cipher Suites', 'xaxis': 'Cipher Suite', 'yaxis': 'Number of Handshake',
#                             'xvalues': [i[0] for i in cipher_suite_trusted],
#                             'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in cipher_suite_trusted]},
#                                        {'name': 'https untrusted', 'yvalue': [i[1] for i in cipher_suite_untrusted]}]}})
#
#
# def certificate_tls_version(request):
#     tls_version_trusted = accumulate(Https.objects(valid=True), 'tls_protocol', with_none=False)
#     tls_version_untrusted = accumulate(Https.objects(valid=False), 'tls_protocol', with_none=False)
#
#     value_name = set([i[0] for i in tls_version_trusted]) | set([i[0] for i in tls_version_untrusted])
#     tls_version_trusted = complete_bars_chart(value_name, tls_version_trusted)
#     tls_version_untrusted = complete_bars_chart(value_name, tls_version_untrusted)
#
#     tls_version_trusted = sorted(tls_version_trusted, key=lambda tup: tup[0])
#     tls_version_untrusted = sorted(tls_version_untrusted, key=lambda tup: tup[0])
#
#     return render(request, 'graphs/certificate.html',
#                   {'page_title': 'HTTPS Certificate TLS Version', 'panel_title': 'Scanned in 11/11/11',
#                    'bars': {'title': 'Cipher Suites', 'xaxis': 'TLS Version', 'yaxis': 'Number of Handshake',
#                             'xvalues': [i[0] for i in tls_version_trusted],
#                             'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in tls_version_trusted]},
#                                        {'name': 'https untrusted', 'yvalue': [i[1] for i in tls_version_untrusted]}]}})



