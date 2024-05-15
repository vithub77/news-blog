from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .news import News


def index(request):
    name = request.user.get_username() if request.user.is_authenticated else 'anon'
    url_redirect = reverse('base:main_page', args=('ru', name))
    return redirect(url_redirect)


class MainPage(generic.ListView):
    news = News()
    template_name = "base/news.html"
    context_object_name = "list_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('lang', 'ru')
        context['title'] = 'Новости России' if lang == 'ru' else 'Новости в Мире'
        context['lang'] = lang
        context['username'] = self.kwargs.get('username')
        return context

    def get_queryset(self):
        return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


def register_user(request, lang):
    if request.user.is_authenticated:
        url_redirect = reverse('base:main_page', args=(lang, request.user.get_username()))
        return redirect(url_redirect)
    else:
        if request.method == "POST":
            if request.POST['password1'] == request.POST['password2']:
                username = request.POST['username']
                psw = request.POST['password1']
                user = User.objects.create_user(username=username, password=psw)
                login(request, user)
                url_redirect = reverse('base:main_page', args=(lang, username))
                return redirect(url_redirect)

        news = News()
        list_news = news.get_news(news_ru=True if lang == 'ru' else False)
        title = 'Новости России-Регистрация' if lang == 'ru' else 'Новости в Мире-Регистрация'
        context = {'list_news': list_news, 'lang': lang, 'title': title, 'username': 'anonym'}
        return render(request, "base/register.html", context)


# class RegisterUser(generic.ListView):
#     form_class = UserCreationForm
#     news = News()
#     template_name = "base/register.html"
#     context_object_name = "list_news"
#     success_url = reverse_lazy('login')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(self.kwargs, '111111111')
#         lang = self.kwargs.get('lang', 'ru')
#         context['title'] = 'Новости России-Регистрация' if lang == 'ru' else 'Новости в Мире-Регистрация'
#         context['lang'] = lang
#         return context
#
#     def get_queryset(self):
#         return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


# def register(request, lang):
#     # return HttpResponse('страница Рега')
#     # form_class = UserCreationForm
#     return render(request, 'base/register.html')

# class Login(generic.ListView):
#     news = News()
#     template_name = "base/user.html"
#     context_object_name = "list_news"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         lang = self.kwargs.get('lang', 'ru')
#         context['title'] = 'Новости России' if lang == 'ru' else 'Новости в Мире'
#         context['lang'] = lang
#         return context
#
#     def get_queryset(self):
#         return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(username=username, password=psw)
        if user:
            login(request, user)
            username = request.session.get('username')
            url_redirect = reverse('base:main_page', args=('ru', username))
            return redirect(url_redirect)
        else:
            return HttpResponse(f'Hello world Nouser')


def user_logout(request, lang):
    logout(request)
    url_redirect = reverse('base:main_page', args=(lang, 'anon'))
    return redirect(url_redirect)
