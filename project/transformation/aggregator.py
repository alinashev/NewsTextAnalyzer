import pyspark.sql.functions as F
from typing import Any
from pyspark.sql.functions import udf, explode
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, ArrayType

from textanalyzer import TextAnalyzer


class Aggregator:

    def aggregate(self, df: DataFrame, conf: Any,
                  model: Any, sentiment_classes: DataFrame,
                  snowflake) -> None:
        aggregation: dict = self.action(df, model, sentiment_classes)

        for a in aggregation:
            df_temp = aggregation[a].withColumn(
                "date",
                F.lit(str(conf.get_date()))
            )
            df_temp.write.jdbc(**conf.table_config()[a])
            if self.is_sentiment(a):
                df_temp.write.format("net.snowflake.spark.snowflake") \
                    .options(**snowflake.snowflake_configuration()) \
                    .option("dbtable", "SENTIMENT") \
                    .mode("append") \
                    .save()

    @staticmethod
    def length(df: DataFrame) -> DataFrame:
        return df.groupBy("category").agg(F.mean("length").alias("length"))

    @staticmethod
    def amount(df: DataFrame) -> DataFrame:
        return df.groupBy("category").count()

    @staticmethod
    def text_analyze(df: DataFrame, model: Any,
                     sentiment_classes: DataFrame,
                     param: str = None) -> DataFrame:

        analyzer: TextAnalyzer = TextAnalyzer(param)
        udf_analyzer: Any = udf(analyzer.analyze, ArrayType(StringType()))
        udf_merge: Any = udf(analyzer.merge_lists, ArrayType(StringType()))
        if param is None:
            param = "word"
        set_name: str = "{param}_set".format(param=param)

        df: DataFrame = \
            df.withColumn(
                set_name, udf_analyzer("news")
            ).groupBy("category").agg(
                udf_merge(F.collect_list(set_name)).alias(set_name)
            ).select(
                F.col("category"),
                explode(set_name).alias(param)
            ).groupBy("category", param).count().orderBy(F.col("count"),
                                                         ascending=False)
        if param == "part":
            return df
        else:
            return Aggregator.predict(
                model, df, "word", analyzer, sentiment_classes
            ).drop("processed", "polarity", "features",
                   "rawPrediction", "probability")

    @staticmethod
    def sentiment_analyze(df: DataFrame, model: Any,
                          sentiment_classes: DataFrame) -> DataFrame:
        analyzer: TextAnalyzer = TextAnalyzer()
        return Aggregator.predict(
            model, df, "news", analyzer, sentiment_classes
        ).drop("news", "processed", "features",
               "rawPrediction", "probability", "polarity")

    @staticmethod
    def predict(model: Any, df, target_column: str,
                analyzer: Any, sentiment_classes: DataFrame) -> DataFrame:
        udf_analyzer: Any = udf(analyzer.analyze, ArrayType(StringType()))
        df: DataFrame = model.transform(
            analyzer.preparation(df, udf_analyzer, target_column)
        )
        return df.join(
            sentiment_classes,
            df.prediction == sentiment_classes.polarity
        )

    def is_sentiment(self, action):
        return True if action == "sentiment" else False

    def action(self, df: DataFrame, model: Any,
               sentiment_classes: DataFrame) -> dict:
        return {
            "length": Aggregator.length(df),
            "amount": Aggregator.amount(df),
            "word": Aggregator.text_analyze(
                df, model, sentiment_classes),
            "part": Aggregator.text_analyze(
                df, model, sentiment_classes, "part"),
            "sentiment": Aggregator.sentiment_analyze(
                df, model, sentiment_classes)
        }
