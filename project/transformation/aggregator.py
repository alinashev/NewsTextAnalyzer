import pyspark.sql.functions as F

from typing import Any
from pyspark.sql.functions import udf, explode
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, ArrayType, FloatType

from textanalyzer import TextAnalyzer


class Aggregator:

    def aggregate(self, df: DataFrame, conf) -> None:
        aggregation: dict = self.action(df)

        for a in aggregation:
            aggregation[a].withColumn(
                "date",
                F.lit(str(conf.get_date()))
            ).write.jdbc(**conf.table_config()[a])

    @staticmethod
    def length(df: DataFrame) -> DataFrame:
        return df.groupBy("category").agg(F.mean("length").alias("length"))

    @staticmethod
    def amount(df: DataFrame) -> DataFrame:
        return df.groupBy("category").count()

    @staticmethod
    def text_analyze(df: DataFrame, param: str) -> DataFrame:
        analyzer: TextAnalyzer = TextAnalyzer(param)
        udf_analyzer: Any = udf(analyzer.analyze, ArrayType(StringType()))
        udf_merge: Any = udf(analyzer.merge_lists, ArrayType(StringType()))
        set_name: str = "{param}_set".format(param=param)

        df: DataFrame = \
            df.withColumn(
                set_name,
                udf_analyzer("news")
            ).groupBy("category").agg(
                udf_merge(F.collect_list(set_name)).alias(set_name)
            ).select(
                F.col("category"),
                explode(set_name).alias(param)
            ).groupBy("category", param).count().orderBy(F.col("count"),
                                                         ascending=False)
        if param == "word":
            udf_polarity: Any = udf(analyzer.polarity, FloatType())
            return df.withColumn("sem", udf_polarity("word"))
        else:
            return df

    def action(self, df) -> dict:
        return {
            "length": Aggregator.length(df),
            "amount": Aggregator.amount(df),
            "word": Aggregator.text_analyze(df, "word"),
            "part": Aggregator.text_analyze(df, "part")
        }
