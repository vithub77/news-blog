from django.utils import timezone
from newsapi import NewsApiClient
import datetime as dt
import requests

from .models import NewsBd, NewsBdEn, PosNews
from secret import api_key


# singleton Class
class News:
    __instance = None
    __key = api_key
    _list_news_ru = []
    _list_news_en = []
    _api = NewsApiClient
    _time_ru = dt
    _time_en = dt
    _time_update_news = 0  # minutes
    _h = 0
    _m = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(News, cls).__new__(cls)
            cls.__instance._api = NewsApiClient(api_key=cls.__key)
            cls.__instance._time_ru = dt.datetime.now()
            cls.__instance._time_en = dt.datetime.now()
        return cls.__instance

    def get_news(self, news_ru: bool):
        if news_ru:
            if (dt.datetime.now() - dt.timedelta(minutes=self._time_update_news)) < self._time_ru:
                return self._list_news_ru
            else:
                self._time_ru = dt.datetime.now()
                news_json = self._api.get_top_headlines(language='ru')
                self._set_news_bd(news_json.get('articles'), news_ru)
                return self._list_news_ru
        else:
            if (dt.datetime.now() - dt.timedelta(minutes=self._time_update_news)) < self._time_en:
                return self._list_news_en
            else:
                self._time_en = dt.datetime.now()
                news_json_en = self._api.get_top_headlines(language='en')
                self._set_news_bd(news_json_en.get('articles'), news_ru)
                print(self._list_news_en, 1111111)
                return self._list_news_en

    def _set_news_bd(self, news, news_ru: bool):
        if news_ru:
            news_time = [f"{(i.data - dt.timedelta(hours=self._h)).strftime('%Y-%m-%d %H:%M:%S')}" for i in
                         NewsBd.objects.order_by('id')[:200]]
            for n in news:
                published_time = n.get('publishedAt')[:-1].replace('T', ' ')
                if published_time in news_time:
                    continue
                url = n.get('url')
                t = n.get('title').split('-')
                author = t[-1].strip()
                description = ' '.join(t[:-1])
                published_time = dt.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S") + dt.timedelta(hours=self._h)
                published_time = timezone.make_aware(published_time)
                NewsBd.objects.create(source=author, description=description,
                                      url=url, data=published_time)
            self._list_news_ru = [{'author': f"{_.source}", 'description': f"{_.description}",
                                   'url': f"{_.url}", 'date': f"{_.data.strftime('%H:%M %d-%m-%Y')}",
                                   'news_id': _.id, 'comments_count': _.comments_set.count()} for _ in
                                  NewsBd.objects.order_by('-data')[:50]]
        else:
            news_time = [f"{(i.data - dt.timedelta(hours=self._h)).strftime('%Y-%m-%d %H:%M:%S')}" for i in
                         NewsBdEn.objects.order_by('id')[:200]]
            for n in news:
                published_time = n.get('publishedAt')[:-1].replace('T', ' ')
                if published_time in news_time:
                    continue
                t = n.get('title').split('-')
                author = t[-1].strip()
                description = ' '.join(t[:-1])
                url = n.get('url')
                published_time = dt.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S") + dt.timedelta(hours=self._h)
                published_time = timezone.make_aware(published_time)
                NewsBdEn.objects.create(source=author, description=description,
                                        url=url, data=published_time)
            self._list_news_en = [{'author': f"{_.source}", 'description': f"{_.description}",
                                   'url': f"{_.url}", 'date': f"{_.data.strftime('%H:%M %d-%m-%Y')}",
                                   'news_id': _.id, 'comments_count': _.commentsen_set.count()} for _ in
                                  NewsBdEn.objects.order_by('-data')[:50]]

        return 0

    @staticmethod
    def get_news_comments(news_id, lang):
        n = NewsBd.objects.get(pk=news_id) if lang == 'ru' else NewsBdEn.objects.get(pk=news_id)
        _com_list = n.comments_set.all().order_by(
            'publication_date') if lang == 'ru' else n.commentsen_set.all().order_by('publication_date')
        comments = [
            {'user': _.author, 'publication_date': _.publication_date.strftime('%H:%M %d-%m-%Y'), 'text': _.text}
            for _ in _com_list]
        result = {'description': f"{n.description}", 'source': f"{n.source}", 'url': f"{n.url}", 'news_id': news_id,
                  'list_comments': comments}
        return result

    @staticmethod
    def set_comments(data):
        lang, news_id = data.get('lang'), data.get('news_id')
        n = NewsBd.objects.get(pk=news_id) if lang == 'ru' else NewsBdEn.objects.get(pk=news_id)
        if lang == "ru":
            n.comments_set.create(author=data.get('username'), text=data.get('text'))
        else:
            n.commentsen_set.create(author=data.get('username'), text=data.get('text'))

    @staticmethod
    def set_news_user(lang, username, news_id):
        n = NewsBd.objects.get(pk=news_id)
        post, created = n.posnews_set.get_or_create(username=username)
        print(post, created, "post, created")

    @staticmethod
    def get_news_postponed(username):
        list_id = [_.news_id for _ in PosNews.objects.filter(username=username)]
        list_news = [{'author': f"{_.source}", 'description': f"{_.description}",
                      'url': f"{_.url}", 'date': f"{_.data.strftime('%H:%M %d-%m-%Y')}",
                      'news_id': _.id, 'comments_count': _.comments_set.count()} for i in list_id for _ in
                     NewsBd.objects.filter(pk=i)]
        return list_news, list_id
