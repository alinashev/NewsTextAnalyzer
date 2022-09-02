class News:
    def __init__(self, id: str, date: str,
                 category: str, source: str, news: str) -> None:

        self.id = id
        self.category = category
        self.date = date
        self.source = source
        self.news = news
