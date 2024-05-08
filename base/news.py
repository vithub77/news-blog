class News:
    _list_news = []

    def get_news(self):
        for i in range(10):
            self._list_news.append({'title': f'Title{i}',
                                    'description': f'description{i}'})
        return self._list_news
