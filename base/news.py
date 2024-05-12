from newsapi import NewsApiClient
import datetime as dt

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

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(News, cls).__new__(cls)
            cls.__instance._api = NewsApiClient(api_key=cls.__key)
            cls.__instance._time_ru = dt.datetime.now()
            cls.__instance._time_en = dt.datetime.now()
        return cls.__instance

    def get_news(self, news_ru):
        if news_ru:
            if (dt.datetime.now() - dt.timedelta(minutes=1)) < self._time_ru:
                print(self._time_ru, 'self._time_ru')
                return self._list_news_ru
            else:
                r = self._api.get_top_headlines(language='ru')
                self._list_news_ru = r.get('articles')
                return self._list_news_ru
        else:
            if (dt.datetime.now() - dt.timedelta(minutes=20)) < self._time_en:
                return self._list_news_en
            else:
                r = self._api.get_top_headlines(language='en')
                self._list_news_en = r.get('articles')
                return self._list_news_en


