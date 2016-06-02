from django import template

register = template.Library()


@register.inclusion_tag('tables/http_tables.html')
def http_table(id, port, http_data):
    if http_data.metadata is not None:
        service = http_data.metadata.service
    else:
        service = None

    return {'id': id,
            'port': port,
            'date': http_data.date,
            'error': http_data.error,
            'response': http_data.response,
            'server': http_data.server,
            'content_type': http_data.content_type,
            'www_authenticate': http_data.www_authenticate,
            'header': http_data.header,
            'index': http_data.index,
            'service': service,
            'ip': http_data.ip,
            }


@register.inclusion_tag("tables/certificate_table.html")
def certificate_table(protocol, id, port, cert_data):
    return {'protocol': protocol,
            'id': id,
            'port': port,
            'date': cert_data.date,
            'error': cert_data.error,
            'valid': cert_data.valid,
            'tls_protocol': cert_data.tls_protocol,
            'cipher_suite': cert_data.cipher_suite,
            'certificate_authority': cert_data.certificate_authority,
            'signature_algorithm': cert_data.signature_algorithm,
            'key_bits': cert_data.key_bits,
            'protocols': cert_data.protocols,
            'ciphers_suites': cert_data.ciphersSuites
            }
