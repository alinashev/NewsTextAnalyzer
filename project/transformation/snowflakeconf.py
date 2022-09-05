from commons.secretsmanager import SecretsManager


class SnowflakeConfigurator:
    def __init__(self):
        self.snowflake_source_name = "net.snowflake.spark.snowflake"
        self.snowflake_database = "NEWSDATA"
        self.snowflake_schema = "PUBLIC"
        self.snowflake_warehouse = "NTA_WH"

    def snowflake_configuration(self):
        return {
            "sfURL": SecretsManager.get_secret("a-nta-sf-url"),
            "sfUser": SecretsManager.get_secret("a-nta-sf-user"),
            "sfPassword": SecretsManager.get_secret("a-nta-sf-password"),
            "sfDatabase": self.snowflake_database,
            "sfSchema": self.snowflake_schema,
            "sfWarehouse": self.snowflake_warehouse
        }
