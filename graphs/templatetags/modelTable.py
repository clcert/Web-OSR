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
            'service': service
          }