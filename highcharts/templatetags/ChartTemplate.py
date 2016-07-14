from django import template

register = template.Library()


@register.inclusion_tag('bars_chart.html')
def bar_chart(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'title_xaxis': data['xaxis'],
            'title_yaxis': data['yaxis'],
            'xlabel': data['xvalues'],
            'values': data['values']}


@register.inclusion_tag('pie_chart_with_legend.html')
def pie_chart_with_legend(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'data': data['data']}


@register.inclusion_tag('pie_chart.html')
def pie_chart(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'data': data['data']}


@register.inclusion_tag('basic_line.html')
def basic_line(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'xAxis': data['xAxis'],
            'yAxis': data['yAxis'],
            'categories': data['categories'],
            'series': data['series']}


@register.inclusion_tag('irregular_timeline.html')
def irregular_timeline(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'xAxis': data['xAxis'],
            'yAxis': data['yAxis'],
            'series': data['series']}


@register.inclusion_tag('basic_column.html')
def basic_column(div_id, data):
    return {'id': div_id,
            'title': data.get('title'),
            'title_xaxis': data.get('xaxis'),
            'title_yaxis': data.get('yaxis'),
            'label_rotation': data.get('label_rotation'),
            'log_scale': data.get('log_scale'),
            'categories': data.get('categories'),
            'values': data.get('values')}


@register.inclusion_tag('charts/log_bars_chart.html')
def log_bars_chart(div_id, data):
    return {'id': div_id,
            'title': data['title'],
            'title_x_axis': data['xaxis'],
            'title_y_axis': data['yaxis'],
            'x_label': data['xvalues'],
            'values': data['values']}