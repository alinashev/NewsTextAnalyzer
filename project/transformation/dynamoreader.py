import boto3

from typing import Any
from boto3.dynamodb.conditions import Attr
from pyspark.sql import DataFrame, SparkSession

from configurator import TransformationConfigurator


class DynamoReader:

    @staticmethod
    def read(spark_session: SparkSession, conf) -> DataFrame:
        dynamodb: Any = boto3.resource('dynamodb')
        table: Any = dynamodb.Table(
            TransformationConfigurator.get_source_name()
        )
        
        response: Any = table.scan(
            FilterExpression=Attr('date').eq(
                str(conf.get_date())))
        data: list = response["Items"]

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                FilterExpression=Attr('date').eq(
                    str(conf.get_date())),
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        try:
            return spark_session.sparkContext.parallelize(data).toDF()
        except ValueError:
            print("No available data for the selected day")
            raise SystemExit
