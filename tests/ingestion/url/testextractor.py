import unittest

from project.ingestion.url.extractor import Extractor


class TestExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_source: str = "bbc"
        self.invalid_source: str = "aaa"

        self.extractor: Extractor = Extractor(self.valid_source)
        self.extractor_invalid: Extractor = Extractor(self.invalid_source)

    def test_list_length(self) -> None:
        self.extractor.extract()
        news_list: int = len(self.extractor.get_news())
        self.assertNotEqual(news_list, 0)

    def test_invalid_source(self) -> None:
        try:
            self.extractor_invalid.extract()
        except NameError as ne:
            self.assertEqual(ne.name, "NameError")


if __name__ == '__main__':
    unittest.main()
