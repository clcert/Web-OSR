from django.http import HttpResponse
from django.shortcuts import render


def search(request):
    return render(request, 'graphs/search.html')