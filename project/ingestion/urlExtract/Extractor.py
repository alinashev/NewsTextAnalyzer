import http.client
import urllib.parse
import json
import datetime

from typing import Any
from keys import access_key


class Extractor:
    def __init__(self, source: Any) -> None:
        self.source = source
        self.news_list = list()
        self.counter = 0
        self.offset = 0

    def extract(self, offset=0) -> None:
        connector: http.client.HTTPConnection = http.client.HTTPConnection('api.mediastack.com')
        params: str = urllib.parse.urlencode({
            'access_key': access_key,
            'sources': self.source,
            'sort': 'published_desc',
            'limit': 100,
            'date': datetime.date.today() - datetime.timedelta(days=1),
            'offset': offset
        })
        connector.request('GET', '/v1/news?{}'.format(params))

        data: Any = json.loads(connector.getresponse().read().decode('utf-8'))
        news_count: int = data["pagination"]["total"]

        self.news_list.extend(data["data"])
        self.counter += data["pagination"]["count"]
        if 100 < news_count != self.counter:
            self.offset += 100
            self.extract(offset=self.offset)

    def get_news(self) -> list:
        return self.news_list
