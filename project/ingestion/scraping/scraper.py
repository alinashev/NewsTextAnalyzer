import requests

from typing import Any
from bs4 import BeautifulSoup
from lxml import etree
from requests import Response


class Scraper:
    def __init__(self, url: str, xpath: str) -> None:
        self.url = url
        self.xpath = xpath

    def scrape(self) -> str:
        webpage: Response = requests.get(self.url)
        soup: BeautifulSoup = BeautifulSoup(webpage.content, "html.parser")
        dom: Any = etree.HTML(str(soup))

        text_list: list = list(
            map(lambda i: str(i.text),
                dom.xpath(self.xpath))
        )
        return ' '.join(map(str, text_list))
