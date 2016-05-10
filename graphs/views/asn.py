from django.shortcuts import render
from graphs.models import AsnIpAmount


def asn(request):
    asn = AsnIpAmount.objects()

    return render(request, 'graphs/asn.html',
                  {'page_title': 'Top Autonomous Systems',
                   'panel_title': 'Number of ip addresses per ASN',
                   'bars': {'title': 'Number of ip addresses per ASN', 'xaxis': 'Number of ips', 'yaxis': 'Autonomous Systems',
                            'xvalues': [i._id for i in asn],
                            'values': [{'name': 'Assigned IPs', 'yvalue': [i.total for i in asn]}]},
                   })

