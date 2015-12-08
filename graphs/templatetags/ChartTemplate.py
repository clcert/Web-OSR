from django import template

register = template.Library()


@register.inclusion_tag('charts/bars_chart.html')
def bar_chart(id, data):
    return {'id': id,
            'title': data['title'],
            'title_x_axis': data['xaxis'],
            'title_y_axis': data['yaxis'],
            'x_label': data['xvalues'],
            'values': data['values']}


@register.inclusion_tag('charts/pie_chart_with_legend.html')
def pie_chart_with_legend(id, data):
    return {'id': id,
            'title': data['title'],
            'data': data['data']}


@register.inclusion_tag('charts/pie_chart.html')
def pie_chart(id, data):
    return {'id': id,
            'title': data['title'],
            'data': data['data']}


@register.inclusion_tag('charts/basic_line.html')
def basic_line(id, data):
    return {'id': id,
            'title': 'Hola'}
            # 'data': data['data']}
