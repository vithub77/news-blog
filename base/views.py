from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse('Hello App News')
    return render(request, 'base/index.html')
