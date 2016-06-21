from django import template
from datetime import datetime

register = template.Library()


@register.inclusion_tag('tables/http_tables.html')
def http_table(id, port, http_data):
    if http_data.metadata is not None:
        service = http_data.metadata.service
    else:
        service = None
    return {'id': id,
            'port': port,
            'ip': http_data.ip,
            'scan_date': datetime.strptime(http_data.date, '%Y-%m-%d').date(),
            'error': http_data.error,
            'response': http_data.status,
            'header': http_data.parse_header,
            'index': http_data.raw_index,
            # 'service': service,
            }



@register.inclusion_tag("tables/certificate_table.html")
def certificate_table(protocol, id, port, cert_data, ip):
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
            'ciphers_suites': cert_data.ciphersSuites,
            'ip': ip
            }
