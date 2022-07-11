import pyspark.sql.functions as F

from pyspark.sql import DataFrame
from utilities.Aggregator import Aggregator
from utilities.DynamoReader import DynamoReader


class Executor:

    @staticmethod
    def execute(spark_session) -> None:
        df: DataFrame = DynamoReader.read(spark_session)
        Aggregator().aggregate(df.withColumn("length", F.length("news")))
