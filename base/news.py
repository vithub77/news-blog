from newsapi import NewsApiClient


# singlton Class
class News:
    __instance = None
    __key = '79b52491e0ed4f00be27261b822c0396'
    _list_news = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(News, cls).__new__(cls)
        return cls.__instance

    def get_news(self, news_ru):
        api = NewsApiClient(api_key=self.__key)
        r = api.get_top_headlines(language='ru') if news_ru else api.get_top_headlines(language='en')
        self._list_news = r.get('articles')
        return self._list_news
