import datetime

from project.commons.Configurator import Configurator


class IngestionConfigurator(Configurator):

    def __init__(self, source: str, table: str) -> None:
        self.source = source
        self.table = table
        self.date = str(datetime.date.today() - datetime.timedelta(days=1))

    def get_date(self) -> str:
        return self.date

    def get_table_name(self) -> str:
        return self.table

    def get_xpath(self) -> dict:
        return {
            "bbc":
                "//div[@width='compact']"
                + "//article"
                + "//div[@data-component='text-block']//p",

            "americanbankingnews":
                "//div[@itemprop='articleBody']//p",

            "dailycaller":
                "//main//div[@id='ob-read-more-selector']//p"
        }
