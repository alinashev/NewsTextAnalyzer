import datetime
import nltk

from typing import Any
from utilities.SecretsManager import SecretsManager


class Configurator:

    @staticmethod
    def get_date() -> Any:
        return datetime.date.today() - datetime.timedelta(days=1)

    @staticmethod
    def get_source_name() -> str:
        return "aNews"

    @staticmethod
    def get_db_url() -> str:
        return "jdbc:postgresql://" \
               + SecretsManager.get_secret("a_rds_newsdata")["host"] \
               + "/newsdata"

    def db_configuration(self) -> dict:
        return {
            "user": SecretsManager.get_secret("a_rds_newsdata")["username"],
            "password":
                SecretsManager.get_secret("a_rds_newsdata")["password"],
            "driver": "org.postgresql.Driver"
        }

    def table_config(self) -> dict:
        return {
            "length": {
                "url": self.get_db_url(),
                "table": "length",
                "mode": "append",
                "properties": self.db_configuration()
            },
            "amount": {
                "url": self.get_db_url(),
                "table": "amount",
                "mode": "append",
                "properties": self.db_configuration()
            },
            "word": {
                "url": self.get_db_url(),
                "table": "word",
                "mode": "append",
                "properties": self.db_configuration()
            },
            "part": {
                "url": self.get_db_url(),
                "table": "part",
                "mode": "append",
                "properties": self.db_configuration()
            }
        }

    @staticmethod
    def nltk_setup() -> None:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('vader_lexicon')
