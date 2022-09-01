from typing import Any

from pyspark.ml.classification import NaiveBayes
from pyspark.ml.feature import StringIndexer
from pyspark.pandas import DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, ArrayType


class Trainer:
    def __init__(self, spark_session, analyzer) -> None:
        self.spark_session = spark_session
        self.analyzer = analyzer
        self.sentiment_classes = None

    def train(self) -> None:
        training: DataFrame = self.spark_session.read.csv(
            'data/train.csv', inferSchema=True, header=True)

        training: DataFrame \
            = self.indexing(training, "polarity_class", "polarity")
        udf_analyzer: Any = udf(self.analyzer.analyze,
                                ArrayType(StringType()))
        prepared_df: DataFrame = self.analyzer.preparation(
            training, udf_analyzer, target_col="text")
        nb: NaiveBayes = NaiveBayes(
            smoothing=1.0, modelType="multinomial", labelCol="polarity")
        model: Any = nb.fit(prepared_df)
        return model

    def indexing(self, df: DataFrame,
                 inputCol: str, outputCol: str) -> DataFrame:
        indexer: StringIndexer = StringIndexer(
            inputCol=inputCol, outputCol=outputCol)
        indexed_df: DataFrame = indexer.fit(df).transform(df)
        self.sentiment_classes: DataFrame = \
            indexed_df.select("polarity_class", "polarity").distinct()
        return indexed_df
