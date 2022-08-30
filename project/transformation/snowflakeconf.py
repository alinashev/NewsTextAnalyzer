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


"""
from commons.secretsmanager import SecretsManager
from pyspark.sql import SparkSession

from snowflakeconf import SnowflakeConfigurator


def main():
    spark = SparkSession.builder.appName("App") \
        .master("local[8]") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.memory.offHeap.enabled", True) \
        .config("spark.memory.offHeap.size", "8g") \
        .getOrCreate()

    snowflake = SnowflakeConfigurator()
    df = spark.read.format(snowflake.snowflake_source_name) \
        .options(**snowflake.snowflake_configuration()) \
        .option("dbtable", snowflake.source_table_name) \
        .load()
    df.show(n=3)


if __name__ == "__main__":
    main()"""
