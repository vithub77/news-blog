from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .news import News


def index(request):
    url_redirect = reverse('base:main_page', args=('ru',))
    return redirect(url_redirect, permanent=True)


class MainPage(generic.ListView):
    news = News()
    template_name = "base/news.html"
    context_object_name = "list_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('lang', 'ru')
        context['title'] = 'Новости России' if lang == 'ru' else 'Новости в Мире'
        context['lang'] = lang
        return context

    def get_queryset(self):
        return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


class Register(generic.ListView):
    news = News()
    template_name = "base/register.html"
    context_object_name = "list_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('lang', 'ru')
        context['title'] = 'Новости России-Регистрация' if lang == 'ru' else 'Новости в Мире-Регистрация'
        context['lang'] = lang
        return context

    def get_queryset(self):
        return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


# def register(request, lang):
#     # return HttpResponse('страница Рега')
#     # form_class = UserCreationForm
#     return render(request, 'base/register.html')

class Login(generic.ListView):
    news = News()
    template_name = "base/user.html"
    context_object_name = "list_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('lang', 'ru')
        context['title'] = 'Новости России' if lang == 'ru' else 'Новости в Мире'
        context['lang'] = lang
        return context

    def get_queryset(self):
        return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)
