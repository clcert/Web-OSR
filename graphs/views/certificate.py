from django.db.models import Sum
from django.shortcuts import render

from graphs.models import ZmapLog, HTTPSKeyBits
from graphs.util import filter_by_name


def certificate_key_bits(request, port, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
            scan_date = scan_date_list.first().date
            # scan_date = scan_date_list.last().date

    trusted = HTTPSKeyBits.objects.filter(port=port, date=scan_date, valid=True).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]
    untrusted = HTTPSKeyBits.objects.filter(port=port, date=scan_date, valid=False).values('bits').order_by('bits') \
        .annotate(total=Sum('total')).order_by('bits')[:10]

    key_bits = sorted(set([i['bits'] for i in trusted]) | set([i['bits'] for i in untrusted]))

    return render(request, 'graphs/certificate.html',
                  {'page_title': 'HTTPs Protocol Key Bits', 'panel_title': 'HTTPS Certificates Key Bits',
                   'bars': {
                       'title': 'Key Bits (HTTPS)',
                       'xaxis': 'Bits',
                       'yaxis': 'Number of Certificates',
                       'categories': [i for i in key_bits],
                       'values': [
                           {'name': 'https trusted', 'data': [i['total'] for i in filter_by_name(trusted, key_bits, 'bits', 'total')]},
                           {'name': 'https untrusted', 'data': [i['total'] for i in filter_by_name(untrusted, key_bits, 'bits', 'total')]}
                       ]
                   }})


# def certificate_validation(request):
#     key_bits_443 = accumulate(Https.objects(), 'validate', with_none=False)[:10]
#
#     return render(request, 'graphs/certificate.html',
#                   {'page_title': 'HTTPS Certificate Validation', 'panel_title': 'Scanned in 11/11/11',
#                    'bars': {'title': 'Certificate Validation (HTTP)', 'xaxis': 'Validation',
#                             'yaxis': 'Number of Certificates',
#                             'xvalues': [i[0] for i in key_bits_443],
#                             'values': [{'name': 'https', 'yvalue': [i[1] for i in key_bits_443]}]}})
#
#
# def certificate_signature(request):
#     signature_trusted = accumulate(Https.objects(valid=True), 'signature_algorithm', with_none=False)
#     signature_untrusted = accumulate(Https.objects(valid=False), 'signature_algorithm', with_none=False)
#
#     value_name = set([i[0] for i in signature_trusted]) | set([i[0] for i in signature_untrusted])
#     signature_trusted = complete_bars_chart(value_name, signature_trusted)
#     signature_untrusted = complete_bars_chart(value_name, signature_untrusted)
#
#     signature_trusted = sorted(signature_trusted, key=lambda tup: tup[0])
#     signature_untrusted = sorted(signature_untrusted, key=lambda tup: tup[0])
#
#     return render(request, 'graphs/certificate.html',
#                   {'page_title': 'HTTPS Certificate Signature', 'panel_title': 'Scanned in 11/11/11',
#                    'bars': {'title': 'Signature', 'xaxis': 'Signature Algorithm', 'yaxis': 'Number of Handshake',
#                             'xvalues': [i[0] for i in signature_trusted],
#                             'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in signature_trusted]},
#                                        {'name': 'https untrusted', 'yvalue': [i[1] for i in signature_untrusted]}]}})
#
#
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



