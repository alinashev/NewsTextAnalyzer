import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.session import SparkSession
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame, Row
from pyspark.sql.functions import *
from pyspark.sql.functions import col, to_timestamp, monotonically_increasing_id, to_date, when
import datetime
from awsglue import DynamicFrame

import boto3

## @params: [JOB_NAME]
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "database_name", "kinesis_table_name",
     "starting_position_of_kinesis_iterator", "hudi_table_name",
     "window_size", "s3_path_hudi", "s3_path_spark"]
)

spark = SparkSession.builder.config(
    'spark.serializer',
    'org.apache.spark.serializer.KryoSerializer'
).config('spark.sql.hive.convertMetastoreParquet', 'false').getOrCreate()

sc = spark.sparkContext
glueContext = GlueContext(sc)
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

database_name = args["database_name"]
kinesis_table_name = args["kinesis_table_name"]
hudi_table_name = args["hudi_table_name"]
s3_path_hudi = args["s3_path_hudi"]
s3_path_spark = args["s3_path_spark"]
starting_position_of_kinesis_iterator = args["starting_position_of_kinesis_iterator"]
window_size = args["window_size"]
catalogue_table_name = database_name + '.' + hudi_table_name

data_frame_from_catalog = glueContext.create_data_frame.from_catalog(
    database=database_name,
    table_name=kinesis_table_name,
    transformation_ctx="DataSource0",
    additional_options={
        "inferSchema": "true",
        "startingPosition": starting_position_of_kinesis_iterator
    }
)

hudi_write_config = {
    'className': 'org.apache.hudi',
    'hoodie.table.name': hudi_table_name,
    'hoodie.datasource.write.operation': 'upsert',
    'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
    'hoodie.datasource.write.precombine.field': 'date',
    'hoodie.datasource.write.recordkey.field': 'source',
    'hoodie.datasource.write.partitionpath.field':
        'source:SIMPLE,year:SIMPLE,month:SIMPLE,day:SIMPLE',
    'hoodie.datasource.write.keygenerator.class':
        'org.apache.hudi.keygen.CustomKeyGenerator',
    'hoodie.deltastreamer.keygen.timebased.timestamp.type': 'MIXED',
    'hoodie.deltastreamer.keygen.timebased.input.dateformat': 'yyyy-mm-dd',
    'hoodie.deltastreamer.keygen.timebased.output.dateformat': 'yyyy/MM/dd'
}

hudi_glue_config = {
    'hoodie.datasource.hive_sync.enable': 'true',
    'hoodie.datasource.hive_sync.sync_as_datasource': 'false',
    'hoodie.datasource.hive_sync.database': database_name,
    'hoodie.datasource.hive_sync.table': hudi_table_name,
    'hoodie.datasource.hive_sync.use_jdbc': 'false',
    'hoodie.datasource.write.hive_style_partitioning': 'true',
    'hoodie.datasource.hive_sync.partition_extractor_class':
        'org.apache.hudi.hive.MultiPartKeysValueExtractor',
    'hoodie.datasource.hive_sync.partition_fields': 'source,year,month,day'
}


def get_existing_table_schema(table):
    return table.select("*").limit(0)


def delete_extra_column(df):
    return df.drop(
        '_hoodie_commit_time', '_hoodie_commit_seqno',
        '_hoodie_record_key', '_hoodie_partition_path',
        '_hoodie_file_name'
    )


def evolve_schema(kinesis_df, table):
    try:
        glue_catalog_df = delete_extra_column(
            get_existing_table_schema(table)
        )
        if kinesis_df.schema != glue_catalog_df.schema:
            return kinesis_df.unionByName(
                glue_catalog_df,
                allowMissingColumns=True
            )
    except Exception as e:
        print(e)
        return kinesis_df


def processBatch(data_frame):
    if data_frame.count() > 0:
        kinesis_dynamic_frame = DynamicFrame.fromDF(
            data_frame, glueContext, "from_kinesis_data_frame"
        ).toDF()

        kinesis_data_frame = evolve_schema(
            kinesis_dynamic_frame.toDF(),
            catalogue_table_name
        )

        glueContext.write_dynamic_frame.from_options(
            frame=DynamicFrame.fromDF(
                kinesis_data_frame,
                glueContext,
                "evolved_kinesis_data_frame"
            ),
            connection_type="custom.spark",
            connection_options={
                'path': s3_path_hudi,
                **hudi_write_config,
                **hudi_glue_config
            }
        )


glueContext.forEachBatch(
    frame=data_frame_from_catalog,
    batch_function=processBatch,
    options={
        "windowSize": window_size,
        "checkpointLocation": s3_path_spark
    }
)

job.commit()
