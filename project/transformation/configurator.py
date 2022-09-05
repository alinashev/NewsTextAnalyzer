import datetime
import nltk

from typing import Any

from commons.configurator import Configurator
from commons.secretsmanager import SecretsManager


class TransformationConfigurator(Configurator):

    def get_date(self) -> Any:
        return datetime.date.today() - datetime.timedelta(days=1)

    @staticmethod
    def get_source_name() -> str:
        return "aNews"

    @staticmethod
    def get_db_url() -> str:
        return "jdbc:postgresql://" \
               + SecretsManager.get_secret("a_rds_newsdata")["host"] \
               + "/newsdata"

    def get_db_configuration(self) -> dict:
        return {
            "user": SecretsManager.get_secret("a_rds_newsdata")["username"],
            "password":
                SecretsManager.get_secret("a_rds_newsdata")["password"],
            "driver": "org.postgresql.Driver"
        }

    def get_db_table_config(self) -> dict:
        return {
            "length": {
                "url": self.get_db_url(),
                "table": "length",
                "mode": "append",
                "properties": self.get_db_configuration()
            },
            "amount": {
                "url": self.get_db_url(),
                "table": "amount",
                "mode": "append",
                "properties": self.get_db_configuration()
            },
            "word": {
                "url": self.get_db_url(),
                "table": "word_sentiment",
                "mode": "append",
                "properties": self.get_db_configuration()
            },
            "part": {
                "url": self.get_db_url(),
                "table": "part",
                "mode": "append",
                "properties": self.get_db_configuration()
            },
            "sentiment": {
                "url": self.get_db_url(),
                "table": "sentiment",
                "mode": "append",
                "properties": self.get_db_configuration()
            }
        }

    def get_snowflake_table_name(self) -> str:
        return "SENTIMENT"

    def get_snowflake_source_name(self) -> str:
        return "net.snowflake.spark.snowflake"

    def get_snowflake_database(self) -> str:
        return "NEWSDATA"

    def get_snowflake_schema(self) -> str:
        return "PUBLIC"

    def get_snowflake_warehouse(self) -> str:
        return "NTA_WH"

    def get_snowflake_configuration(self) -> dict:
        return {
            "sfURL": SecretsManager.get_secret("a-nta-sf-url"),
            "sfUser": SecretsManager.get_secret("a-nta-sf-user"),
            "sfPassword": SecretsManager.get_secret("a-nta-sf-password"),
            "sfDatabase": self.get_snowflake_database(),
            "sfSchema": self.get_snowflake_schema(),
            "sfWarehouse": self.get_snowflake_warehouse()
        }

    @staticmethod
    def nltk_setup() -> None:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
