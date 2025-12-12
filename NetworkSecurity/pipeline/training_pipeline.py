from pathlib import Path

from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import ModelTrainer

from NetworkSecurity.entity.config import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from NetworkSecurity.entity.artifact import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            logging.info('Initiate Data Ingestion')

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info('Data Initialization completed')
            
            print(data_ingestion_artifact)
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            logging.info('Initiate Data Validation')

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Data validation completed')
            
            print(data_validation_artifact)
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e) from e
        
    def start_data_trasformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            logging.info('Initiate Data Transformation')

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info('Data Transformation Completed')
            
            print(data_transformation_artifact)
            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            logging.info('Initiate Model Training')

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info('Model Training Completed')

            print(model_trainer_artifact)
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_trasformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        except Exception as e:
            raise CustomException(e) from e