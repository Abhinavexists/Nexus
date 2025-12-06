import sys
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging
from NetworkSecurity.entity.artifact import DataIngestionArtifact
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.entity.config import (
    DataIngestionConfig, 
    TrainingPipelineConfig, 
    DataValidationConfig,
    DataTransformationConfig
    )

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Initiate the data Ingestion')

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info('Data Initialisation completed')
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info('Initiate the data validation')

        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info('Data validation completed')
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info('Data Transformation Complete')
        print(data_transformation)

    except Exception as e:
        raise CustomException(e)
