from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from .news import News


def index(request):
    url_redirect = reverse('base:page_news', args=('ru',))
    return redirect(url_redirect, permanent=True)


def page_news(request, lang):
    news = News()
    list_news = news.get_news(news_ru=True if lang == 'ru' else False)
    return render(request, 'base/news.html', {'list_news': list_news,
                                              'title': 'Новости'
                                              })
