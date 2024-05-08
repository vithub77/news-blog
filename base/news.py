from newsapi import NewsApiClient

class News:
    __key = '79b52491e0ed4f00be27261b822c0396'
    _list_news = []

    def get_news(self):
        api = NewsApiClient(api_key=self.__key)
        r = api.get_top_headlines(language='ru')
        self._list_news = r.get('articles')
        # for i in range(10):
        #     self._list_news.append({'title': f'Title{i}',
        #                             'description': f'description{i}'})
        return self._list_news



