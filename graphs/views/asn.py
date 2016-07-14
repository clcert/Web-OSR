from django.shortcuts import render
from graphs.models import asn
from django.http import HttpResponse
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def top_asn(request):
    full_data = asn.Asn.objects.all()
    for data in full_data:
        data.block_size = data.number_of_addresses()
    full_data = sorted(full_data, key=operator.attrgetter('block_size'), reverse=True)

    paginator = Paginator(full_data, 25)
    page = request.GET.get('page')
    try:
        partial_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        partial_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        partial_data = paginator.page(paginator.num_pages)
    return render(request, 'graphs/asn.html',
              {'page_title': 'Top Autonomous Systems',
               'panel_title': 'Number of ip addresses per ASN',
               'bars': {'title': 'Number of ip addresses per ASN', 'yaxis': 'Number of ips', 'xaxis': 'Autonomous Systems',
                                                                    # yaxis y xaxis estan cambiados en el chart
                        'xvalues': [i.name.split(',')[0] + str(i.number) for i in partial_data],
                        'values': [{'name': "Number of assigned ip addresses ", 'yvalue': [i.block_size for i in partial_data]}]},
                        'partial_data': partial_data,

               })
