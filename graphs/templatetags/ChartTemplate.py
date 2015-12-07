from django import template

register = template.Library()


@register.inclusion_tag('charts/bars_chart.html')
def bar_chart(id, bars):
    return {'id': id,
            'title': bars['title'],
            'title_x_axis': bars['xaxis'],
            'title_y_axis': bars['yaxis'],
            'x_label': bars['xvalues'],
            'values': bars['values']}
