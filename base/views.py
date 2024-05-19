from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views import generic

from .news import News
from .forms import UserLoginForm, UserRegisterForm


def index(request):
    name = request.user.get_username() if request.user.is_authenticated else 'anon'
    url_redirect = reverse('base:main_page', args=('ru', name))
    return redirect(url_redirect)


class MainPage(generic.ListView):
    news = News()
    form = UserLoginForm()
    template_name = "base/news.html"
    context_object_name = "list_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get('lang', 'ru')
        context['title'] = 'Новости России' if lang == 'ru' else 'Новости в Мире'
        context['lang'] = lang
        context['username'] = self.kwargs.get('username')
        context['form'] = self.request.GET.get('form',
                                               self.form)  # self.form if not self.request.user.is_authenticated else '<h1>He World</h1>'
        return context

    def get_queryset(self):
        return self.news.get_news(news_ru=True if self.kwargs['lang'] == 'ru' else False)


def register_user(request, lang):
    if request.user.is_authenticated:
        url_redirect = reverse('base:main_page', args=(lang, request.user.get_username()))
        return redirect(url_redirect)
    else:
        if request.method == "POST":
            form = UserRegisterForm(data=request.POST)
            if form.is_valid():
                # form.save()
                username = request.POST['username']
                psw = request.POST['password1']
                user = User.objects.create_user(username=username, password=psw)
                login(request, user)
                url_redirect = reverse('base:main_page', args=(lang, username))
                return redirect(url_redirect)
            else:
                news = News()
                list_news = news.get_news(news_ru=True if lang == 'ru' else False)
                title = 'Новости России-Регистрация' if lang == 'ru' else 'Новости в Мире-Регистрация'
                context = {'title': title, 'form': form, 'lang': lang, 'username': 'anon', 'list_news': list_news}
                return render(request, 'base/register.html', context)

        news = News()
        list_news = news.get_news(news_ru=True if lang == 'ru' else False)
        title = 'Новости России-Регистрация' if lang == 'ru' else 'Новости в Мире-Регистрация'
        form = UserRegisterForm()
        context = {'list_news': list_news, 'lang': lang, 'title': title, 'username': 'anonym', 'form': form}
        return render(request, "base/register.html", context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            psw = request.POST.get('password')
            user = authenticate(username=username, password=psw)
            if user:
                login(request, user)
                url_redirect = reverse('base:main_page', args=('ru', username))
                return redirect(url_redirect)
        else:
            news = News()
            list_news = news.get_news(news_ru=True)
            context = {'form': form, 'lang': 'ru', 'username': 'anon', 'list_news': list_news}
            return render(request, 'base/news.html', context)
    else:
        url_redirect = reverse('base:main_page', args=('ru', 'anon'))
        return redirect(url_redirect)


def user_logout(request, lang):
    logout(request)
    url_redirect = reverse('base:main_page', args=(lang, 'anon'))
    return redirect(url_redirect)


def comments_view(request, lang, username, news_id):
    if request.method == 'POST':
        data = {'lang': lang, 'username': username,
                'news_id': news_id, 'text': request.POST.get('comment_text')}
        News.set_comments(data)
    # if username != 'anon':
    #     user = User.objects.get(username=username)
    #     date_joined = user.date_joined.strftime('%d-%m-%Y')
    form = UserLoginForm()
    json_comments = News.get_news_comments(news_id, lang)
    title = f'Комментарии: {" ".join(json_comments.get("description").split()[:2])}'
    context = {'title': title, 'username': username, 'lang': lang, 'form': form,
               'json_comments': json_comments}
    return render(request, 'base/comments.html', context)
