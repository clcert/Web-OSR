from django.shortcuts import render
from graphs.models import AsnIpAmount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def asn(request):
    full_data = AsnIpAmount.objects()
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
                            'xvalues': [i._id for i in partial_data],
                            'values': [{'name': 'Assigned IPs', 'yvalue': [i.total for i in partial_data]}]},
                            'partial_data': partial_data,
                   
                   })

