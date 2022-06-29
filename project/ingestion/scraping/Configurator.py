import datetime


class Configurator:
    def __init__(self, source: str, table: str) -> None:
        self.source = source
        self.table = table
        self.date = str(datetime.date.today() - datetime.timedelta(days=1))

    def get_bbc_param(self) -> dict:
        return {
            "xpath": "//div[@width='compact']//article//div[@data-component='text-block']//p",
            "table_name": self.table,
            "date": self.date
        }

    def get_americanbankingnews_param(self) -> dict:
        return {
            "xpath": "//div[@itemprop='articleBody']//p",
            "table_name": self.table,
            "date": self.date
        }

    def get_dailycaller_param(self) -> dict:
        return {
            "xpath": "//main//div[@id='ob-read-more-selector']//p",
            "table_name": self.table,
            "date": self.date
        }

    def get_param(self) -> dict:
        if self.source == "bbc":
            return self.get_bbc_param()
        if self.source == "americanbankingnews":
            return self.get_americanbankingnews_param()
        if self.source == "dailycaller":
            return self.get_dailycaller_param()
