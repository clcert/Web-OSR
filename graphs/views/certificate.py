from django.shortcuts import render
from graphs.models import Https
from graphs.views.util import accumulate, complete_bars_chart


def certificate_key_bits(request):
    key_bits_443_trusted = accumulate(Https.objects(valid=True), 'key_bits', with_none=False)[:10]
    key_bits_443_untrusted = accumulate(Https.objects(valid=False), 'key_bits', with_none=False)[:10]

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


def certificate_cipher_suite(request):
    cipher_suite_trusted = accumulate(Https.objects(valid=True), 'cipher_suite', with_none=False)[:10]
    cipher_suite_untrusted = accumulate(Https.objects(valid=False), 'cipher_suite', with_none=False)[:10]

    value_name = set([i[0] for i in cipher_suite_trusted]) | set([i[0] for i in cipher_suite_untrusted])
    cipher_suite_trusted = complete_bars_chart(value_name, cipher_suite_trusted)
    cipher_suite_untrusted = complete_bars_chart(value_name, cipher_suite_untrusted)

    cipher_suite_trusted = sorted(cipher_suite_trusted, key=lambda tup: tup[0])
    cipher_suite_untrusted = sorted(cipher_suite_untrusted, key=lambda tup: tup[0])

    return render(request, 'graphs/cert_cipher_suite.html',
                  {'bars': {'title': 'Cipher Suites', 'xaxis': 'Cipher Suite', 'yaxis': 'Number of Handshake',
                            'xvalues': [i[0] for i in cipher_suite_trusted],
                            'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in cipher_suite_trusted]},
                                       {'name': 'https untrusted', 'yvalue': [i[1] for i in cipher_suite_untrusted]}]}})


def certificate_tls_version(request):
    tls_version_trusted = accumulate(Https.objects(valid=True), 'tlsProtocol', with_none=False)
    tls_version_untrusted = accumulate(Https.objects(valid=False), 'tlsProtocol', with_none=False)

    value_name = set([i[0] for i in tls_version_trusted]) | set([i[0] for i in tls_version_untrusted])
    tls_version_trusted = complete_bars_chart(value_name, tls_version_trusted)
    tls_version_untrusted = complete_bars_chart(value_name, tls_version_untrusted)

    tls_version_trusted = sorted(tls_version_trusted, key=lambda tup: tup[0])
    tls_version_untrusted = sorted(tls_version_untrusted, key=lambda tup: tup[0])

    return render(request, 'graphs/cert_tls_version.html',
                  {'bars': {'title': 'Cipher Suites', 'xaxis': 'TLS Version', 'yaxis': 'Number of Handshake',
                            'xvalues': [i[0] for i in tls_version_trusted],
                            'values': [{'name': 'https trusted', 'yvalue': [i[1] for i in tls_version_trusted]},
                                       {'name': 'https untrusted', 'yvalue': [i[1] for i in tls_version_untrusted]}]}})



