import pyspark.sql.functions as F

from pyspark.sql import DataFrame

from aggregator import Aggregator
from dynamoreader import DynamoReader


class Executor:

    @staticmethod
    def execute(spark_session, conf) -> None:
        df: DataFrame = DynamoReader.read(spark_session, conf)
        Aggregator().aggregate(df.withColumn("length", F.length("news")), conf)
