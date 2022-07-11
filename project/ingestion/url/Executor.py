from Extractor import Extractor


class Executor:
    @staticmethod
    def execute(source) -> list:
        extractor: Extractor = Extractor(source)
        extractor.extract()
        return extractor.get_news()
