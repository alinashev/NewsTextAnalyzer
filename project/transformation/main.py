import os
import sys

from pyspark.sql import SparkSession

if os.path.exists('transformation.zip'):
    sys.path.insert(0, 'utilities.zip')
else:
    sys.path.insert(0, './utilities')

from utilities.Executor import Executor


def main():
    sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] =\
        '--packages org.postgresql:postgresql:42.4.0 pyspark-shell'

    spark_session: SparkSession = SparkSession.builder.appName("App")\
        .master("local[8]")\
        .config("spark.driver.memory", "1g")\
        .config("spark.executor.memory", "1g")\
        .config("spark.memory.offHeap.enabled", True)\
        .config("spark.memory.offHeap.size", "8g")\
        .config("spark.driver.extraClassPath", sparkClassPath)\
        .getOrCreate()

    Executor.execute(spark_session)


if __name__ == "__main__":
    main()
