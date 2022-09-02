import json
import boto3
from botocore.client import BaseClient
from typing import Any

from loader import Loader


class Stream(Loader):
    def __init__(self, stream_name: str, date: Any) -> None:
        self.stream_name = stream_name
        self.date = date

    @staticmethod
    def get_client() -> BaseClient:
        return boto3.client('kinesis')

    def put(self, news: dict) -> None:
        partition_key: str = news.get("source")
        client: Any = self.get_client()
        client.put_record(
            StreamName=self.stream_name,
            Data=json.dumps(news),
            PartitionKey=partition_key
        )
