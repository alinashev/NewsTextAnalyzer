import uuid

from Loader import Loader
from Scraper import Scraper


class Executor:
    @staticmethod
    def execute(url: str, category: str, source: str,
                xpath: str, table_name: str, date: str) -> None:
        bbc_scraper: Scraper = Scraper(url, xpath)
        loader: Loader = Loader(table_name, date)
        loader.put(uuid.uuid4().hex, category, source, bbc_scraper.scrape())
