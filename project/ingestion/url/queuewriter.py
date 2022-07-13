import boto3

from botocore.client import BaseClient


class QueueWriter:
    @staticmethod
    def write(queue_name, message) -> None:
        client: BaseClient = boto3.client('sqs')
        client.send_message(
            QueueUrl=queue_name,
            MessageBody=message)
