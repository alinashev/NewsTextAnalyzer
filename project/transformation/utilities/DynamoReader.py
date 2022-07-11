import boto3

from typing import Any
from boto3.dynamodb.conditions import Attr
from pyspark.sql import DataFrame, SparkSession
from utilities.Configurator import Configurator


class DynamoReader:

    @staticmethod
    def read(spark_session: SparkSession) -> DataFrame:
        dynamodb: Any = boto3.resource('dynamodb')
        table: Any = dynamodb.Table(Configurator.get_source_name())
        response: Any = table.scan(
            FilterExpression=Attr('date').eq(
                str(Configurator.get_date())))["Items"]
        return spark_session.sparkContext.parallelize(response).toDF()
