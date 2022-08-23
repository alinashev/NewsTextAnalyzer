import datetime

from commons.configurator import Configurator


class IngestionConfigurator(Configurator):

    def __init__(self, source: str, table: str, stream: str) -> None:
        self.source = source
        self.table = table
        self.stream = stream
        self.date = str(datetime.date.today() - datetime.timedelta(days=1))

    def get_date(self) -> str:
        return self.date

    def get_table_name(self) -> str:
        return self.table

    def get_stream_name(self) -> str:
        return self.stream

    def get_xpath(self) -> dict:
        return {
            "bbc":
                "//div[@width='compact']"
                + "//article"
                + "//div[@data-component='text-block']//p",

            "dailycaller":
                "//main//div[@id='ob-read-more-selector']//p",

            "metro":
                "//article//p[not(@class='follow-promo')]",

            "guardian":
                "//div[@id='maincontent']//p",

            "dailymail":
                "//div[@itemprop='articleBody']//p"
        }
