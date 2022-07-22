import boto3

from typing import Any


class Loader:
    def __init__(self, table: Any, date: Any) -> None:
        self.table = table
        self.date = date

    def put(self, id: str, category: str, source: str, news: str) -> None:
        database: Any = boto3.resource("dynamodb")
        table: Any = database.Table(self.table)
        table.put_item(
            Item={
                "id": id,
                "category": category,
                "date": self.date,
                "source": source,
                "news": news
            }
        )
