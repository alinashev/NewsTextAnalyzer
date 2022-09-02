from typing import Any

from commons.configurator import Configurator


class HudiConfigurator(Configurator):
    def get_date(self) -> Any:
        pass

    def __init__(self, hudi_table_name: str, database_name: str) -> None:
        self.hudi_table_name = hudi_table_name
        self.database_name = database_name

    def get_hudi_write_config(self) -> dict:
        return {
            'className': 'org.apache.hudi',
            'hoodie.table.name': self.hudi_table_name,
            'hoodie.datasource.write.operation': 'upsert',
            'hoodie.datasource.write.table.type': 'COPY_ON_WRITE',
            'hoodie.datasource.write.precombine.field': 'date',
            'hoodie.datasource.write.recordkey.field': 'source',
            'hoodie.datasource.write.partitionpath.field':
                'source:SIMPLE,date:SIMPLE,category:SIMPLE',
            'hoodie.datasource.write.keygenerator.class':
                'org.apache.hudi.keygen.CustomKeyGenerator',
            'hoodie.deltastreamer.keygen.timebased.timestamp.type': 'MIXED',
            'hoodie.deltastreamer.keygen.timebased.input.dateformat':
                'yyyy-mm-dd',
            'hoodie.deltastreamer.keygen.timebased.output.dateformat':
                'yyyy/MM/dd'
        }

    def get_hudi_glue_config(self) -> dict:
        return {
            'hoodie.datasource.hive_sync.enable': 'true',
            'hoodie.datasource.hive_sync.sync_as_datasource': 'false',
            'hoodie.datasource.hive_sync.database': self.database_name,
            'hoodie.datasource.hive_sync.table': self.hudi_table_name,
            'hoodie.datasource.hive_sync.use_jdbc': 'false',
            'hoodie.datasource.write.hive_style_partitioning': 'true',
            'hoodie.datasource.hive_sync.partition_extractor_class':
                'org.apache.hudi.hive.MultiPartKeysValueExtractor',
            'hoodie.datasource.hive_sync.partition_fields':
                'source,date,category'
        }
