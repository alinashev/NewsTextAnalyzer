import os

from pyspark.sql import SparkSession

from textanalyzer import TextAnalyzer
from executor import Executor
from configurator import TransformationConfigurator

from trainer import Trainer


def main():
    sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = \
        '--packages org.postgresql:postgresql:42.4.0 pyspark-shell'

    spark_session: SparkSession = SparkSession.builder.appName("App") \
        .master("local[8]") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.memory.offHeap.enabled", True) \
        .config("spark.memory.offHeap.size", "8g") \
        .config("spark.driver.extraClassPath", sparkClassPath) \
        .getOrCreate()

    TransformationConfigurator.nltk_setup()

    conf: TransformationConfigurator = TransformationConfigurator()
    analyzer: TextAnalyzer = TextAnalyzer()
    trainer: Trainer = Trainer(spark_session, analyzer)

    Executor.execute(
        spark_session, conf,
        trainer.train(), trainer.sentiment_classes
    )


if __name__ == "__main__":
    main()
