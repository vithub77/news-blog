from django.shortcuts import render
from django.http import HttpResponse

from .news import News


def index(request):
    news = News()
    list_news = news.get_news()
    return render(request, 'base/index.html', {'list_news': list_news,
                                               'title': 'Новости'
                                               })
