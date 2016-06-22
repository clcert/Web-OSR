from django import template
from datetime import datetime

register = template.Library()


@register.inclusion_tag('tables/http_tables.html')
def http_table(id, port, http_data):
    return {'id': id,
            'ip': http_data.ip,
            'port': port,
            'scan_date': datetime.strptime(http_data.date, '%Y-%m-%d').date(),
            'error': http_data.error,
            'response': http_data.status,
            'header': http_data.parse_header,
            'index': http_data.raw_index,
            'service': http_data.metadata.service,
            }


@register.inclusion_tag("tables/certificate_table.html")
def certificate_table(id, port, protocol, data):
    return {'id': id,
            'ip': data.ip,
            'port': port,
            'protocol': protocol,
            'date': data.date,
            'error': data.error,
            'validate': data.validate,
            'validation_error': data.validation_error,
            'tls_protocol': data.tls_protocol,
            'cipher_suite': data.cipher_suite,
            'chain': data.chain,
            'supported_protocols': data.supported_protocols,
            'supported_cipher_suites': data.supported_cipher_suites
            }
