from django import template

register = template.Library()


@register.inclusion_tag('protocols/http.html')
def http(title, data):
    return {'title': title,
            'data': data
            }
