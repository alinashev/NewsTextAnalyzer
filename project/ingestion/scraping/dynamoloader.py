import boto3

from typing import Any

from loader import Loader


class Dynamo(Loader):
    def __init__(self, table: Any, date: Any) -> None:
        self.table = table
        self.date = date

    def put(self, news: dict) -> None:
        database: Any = boto3.resource("dynamodb")
        table: Any = database.Table(self.table)
        table.put_item(Item=news)
