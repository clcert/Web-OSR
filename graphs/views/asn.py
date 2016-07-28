from django.shortcuts import render
from graphs.models import asn, ZmapLog, AsnHTTPServer
from django.db.models import Sum
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from graphs.util import filter_by_name


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


def asn_search(request):
    return render(request, 'graphs/asn_search.html',
                  {
                      'panel_title': "Acabas de buscar " + str(request.GET['question'])
                  })


def http_server_asn_search(request):
    if request.POST.get('number'):
        try:
            number = int(request.POST['number'])
            return http_server_all_asn(request, number)
        except ValueError:
            pass
    return render(request, 'graphs/http_server_asn.html')


def http_server_asn(request, number, port, scan_date=None, product=None):
    scan_date_list = ZmapLog.objects.filter(port=port)
    if scan_date is None:
        scan_date = scan_date_list.last().date

    # if product:
    #     version_server = HTTPServer.objects.filter(port=port, date=scan_date, product=product)[:9]

    web_server = AsnHTTPServer.objects.filter(asn=number, port=port, date=scan_date).values('product').order_by('product')\
        .annotate(total=Sum('total')).order_by('-total')[:10]

    return render(request, 'graphs/http_server_asn.html',
                  {'port': port,
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {
                       'title': 'Web Server Running (HTTP) on Autonomous System %s' % number, 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                       'categories': [i['product'] for i in web_server],
                       'values': [{'name': 'port ' + port, 'data': [i['total'] for i in web_server]}]},
                   'pie': None
                   })


def http_server_all_asn(request, number=None, scan_date=None):
    scan_date_list = ZmapLog.objects.filter(port=80)
    if scan_date is None:
        # NO FUNCIONARA HASTA QUE TENGAMOS TODOS LOS DATOS TRANSFORMEITED!
        # Para ver como queda usar first() en vez de last()
        scan_date = scan_date_list.last().date
    if not number:
        try:
            number = int(request.POST['number'])
            print reverse('graphs/asn/server/all', kwargs={'number': number, 'scan_date': scan_date})
            return HttpResponseRedirect(reverse('graphs/asn/server/all', kwargs={'number': number, 'scan_date': scan_date}))
        except ValueError:
            return HttpResponseRedirect(reverse('graphs/asn/server/all'))

    http80 = AsnHTTPServer.objects.filter(asn=number, port=80, date=scan_date).values('product').order_by('product') \
                 .annotate(total=Sum('total')).order_by('-total')[:10]
    http443 = filter_by_name(AsnHTTPServer.objects.filter(asn=number, port=443, date=scan_date).values('product').order_by('product') \
                             .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8000 = filter_by_name(AsnHTTPServer.objects.filter(asn=number, port=8000, date=scan_date).values('product').order_by('product') \
                              .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')
    http8080 = filter_by_name(AsnHTTPServer.objects.filter(asn=number, port=8080, date=scan_date).values('product').order_by('product') \
                              .annotate(total=Sum('total')), [i['product'] for i in http80], 'product', 'total')

    return render(request, 'graphs/http_server_asn.html',
                  {'port': 'all',
                   'number': number,
                   'scan_date': scan_date,
                   'scan_list': [i.date for i in scan_date_list],
                   'bars': {'title': 'Web Server Running (HTTP) on Autonomous System %s' % number, 'xaxis': 'Web Server', 'yaxis': 'Number of Servers',
                            'categories': [i['product'] for i in http80],
                            'values': [
                                {'name': 'port 80', 'data': [i['total'] for i in http80]},
                                {'name': 'port 443', 'data': [i['total'] for i in http443]},
                                {'name': 'port 8000', 'data': [i['total'] for i in http8000]},
                                {'name': 'port 8080', 'data': [i['total'] for i in http8080]}
                            ]}
                   })
