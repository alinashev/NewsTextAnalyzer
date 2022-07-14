import json
import boto3

from typing import Any
from boto3 import Session
from botocore.client import BaseClient


class SecretsManager:

    @staticmethod
    def get_secret(secret_name) -> dict:
        session: Session = boto3.session.Session()
        client: BaseClient = session.client(
            service_name='secretsmanager'
        )
        get_secret_value_response: Any = client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(get_secret_value_response["SecretString"])
