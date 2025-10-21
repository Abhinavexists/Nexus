import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging
from NetworkSecurity.entity.artifact import DataIngestionArtifact
from NetworkSecurity.entity.config import DataIngestionConfig, TrainingPipeineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipeineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Initate the data Ingestion')

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        raise CustomException(e)
