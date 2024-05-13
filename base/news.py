from django.utils import timezone
from newsapi import NewsApiClient
import datetime as dt

from .models import NewsBd
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

        else:
            if (dt.datetime.now() - dt.timedelta(minutes=self._time_update_news)) < self._time_en:
                return self._list_news_en
            else:
                self._time_en = dt.datetime.now()
                news_json_en = self._api.get_top_headlines(language='en')
                self._set_news_bd(news_json_en.get('articles'), news_ru)

    def _set_news_bd(self, news, news_ru: bool):
        l_time = [f"{(i.data - dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}" for i in NewsBd.objects.order_by('id')[:20]]
        for n in news:
            published_time = n.get('publishedAt')[:-1].replace('T', ' ')
            if published_time in l_time:
                continue
            t = n.get('title').split('-')
            author = t[-1].strip()
            description = ' '.join(t[:-1])
            url = n.get('url')
            published_time = dt.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S") + dt.timedelta(hours=3)
            published_time = timezone.make_aware(published_time)
            _news = NewsBd(source=author, description=description,
                           url=url, data=published_time)
            _news.save()

    def _get_from_bd(self):
        pass
