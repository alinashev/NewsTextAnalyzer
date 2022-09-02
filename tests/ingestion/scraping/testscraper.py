import unittest

from project.ingestion.scraping.configurator import IngestionConfigurator
from project.ingestion.scraping.scraper import Scraper


class TestScraper(unittest.TestCase):
    def setUp(self) -> None:
        source: str = "bbc"

        conf: IngestionConfigurator = \
            IngestionConfigurator(source, "None", "None")

        url: str = "https://www.bbc.co.uk/news/" \
                   + "world-us-canada-61889593?" \
                   + "at_medium=RSS&at_campaign=KARANGA"
        xpath: str = conf.get_xpath().get(source)

        invalid_url: str = "https://dailycaller.com/2022/06/21/" \
                           + "caleb-swanigan-nba-purdue-dead-25" \
                           + "-natural-causes/"

        invalid_xpath: str = "//div[@itemprop='articleBody']//p"

        self.scraper: Scraper = Scraper(url, xpath)
        self.scraper_invalid_url: Scraper = Scraper(invalid_url, xpath)
        self.scraper_invalid_xpath: Scraper = Scraper(url, invalid_xpath)

    def test_scrape(self) -> None:
        page: str = self.scraper.scrape()
        self.assertNotEqual(len(page), 0)

    def test_scrape_with_invalid_url(self) -> None:
        page: str = self.scraper_invalid_url.scrape()
        self.assertEqual(len(page), 0)

    def test_scrape_with_invalid_xpath(self) -> None:
        page: str = self.scraper_invalid_url.scrape()
        self.assertEqual(len(page), 0)


if __name__ == '__main__':
    unittest.main()
