import pyspark.sql.functions as F

from pyspark.sql import DataFrame, SparkSession
from typing import Any
from aggregator import Aggregator
from dynamoreader import DynamoReader


class Executor:

    @staticmethod
    def execute(spark_session: SparkSession, conf: Any,
                model: Any, sentiment_classes: DataFrame,
                snowflake) -> None:
        df: DataFrame = DynamoReader.read(spark_session, conf)
        Aggregator().aggregate(
            df.withColumn("length", F.length("news")),
            conf, model, sentiment_classes, snowflake
        )
