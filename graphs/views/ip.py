from django.http import HttpResponse
from django.shortcuts import render
from django import forms

from graphs.models import Http80


class SearchForm(forms.Form):
    question = forms.CharField(label='question', max_length=100)


def ip_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            ip = form.cleaned_data['question']
            http_80 = Http80.objects(ip=ip).first()
            print http_80
            return render(request, 'graphs/ip.html', {'ip': ip, 'port80': http_80})
        return HttpResponse("error")
