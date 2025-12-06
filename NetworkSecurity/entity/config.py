from pathlib import Path
from datetime import datetime
from NetworkSecurity.constant import training_pipeline
from NetworkSecurity.exception.exception import CustomException

# The problem: mutable/default argument trap
# datetime.now() is evaluated once at function definition time, not each time when create a new object.
# So if i create multiple instances of TrainingPipelineConfig, they’ll all get the same timestamp (the time the class was first defined), 
# not the time of creation.

# class TrainingPipelineConfig:
#     def __init__(self, timestamp = datetime.now()):
#         timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
#         self.pipeline_name = training_pipeline.PIPELINE_NAME
#         self.artifact_name = training_pipeline.ARTIFACT_DIR
#         self.artifact_dir = Path(self.artifact_name).joinpath(timestamp)
#         self.timestamp: str = timestamp


class TrainingPipelineConfig:
    def __init__(self, timestamp:str | None = None):
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

            self.pipeline_name = training_pipeline.PIPELINE_NAME
            self.artifact_name = training_pipeline.ARTIFACT_DIR
            self.artifact_dir: Path = Path(self.artifact_name) / timestamp
            self.timestamp: str = timestamp
        except Exception as e:
            raise CustomException(e)
        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_ingestion_dir: Path = Path(training_pipeline_config.artifact_dir) / training_pipeline.DATA_INGESTION_DIR_NAME

            self.feature_store_file_path: Path = (
                self.data_ingestion_dir /
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR /
                training_pipeline.FILE_NAME
            )

            self.training_file_path: Path = (
                self.data_ingestion_dir /
                training_pipeline.DATA_INGESTION_INGESTED_DIR /
                training_pipeline.TRAIN_FILE_NAME
            )

            self.testing_file_path: Path = (
                self.data_ingestion_dir /
                training_pipeline.DATA_INGESTION_INGESTED_DIR /
                training_pipeline.TEST_FILE_NAME
            )

            self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TEST_TRAIN_SPLIT_RATION
            self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        except Exception as e:
            raise CustomException(e)
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_validation_dir: Path = (
                training_pipeline_config.artifact_dir /
                training_pipeline.DATA_VALIDATION_DIR_NAME 
            )
            
            self.valid_data_dir: Path = (
                self.data_validation_dir /
                training_pipeline.DATA_VALIDATION_VALID_DIR
            )

            self.invalid_data_dir: Path = (
                self.data_validation_dir /
                training_pipeline.DATA_VALIDATION_INVALID_DIR
            )

            self.valid_data_train_path: Path = (
                self.valid_data_dir / 
                training_pipeline.TRAIN_FILE_NAME
            )

            self.valid_data_test_path: Path = (
                self.valid_data_dir / 
                training_pipeline.TEST_FILE_NAME
            )

            self.invalid_data_train_path: Path = (
                self.invalid_data_dir / 
                training_pipeline.TRAIN_FILE_NAME
            )

            self.invalid_data_test_path: Path = (
                self.invalid_data_dir /
                training_pipeline.TEST_FILE_NAME
            )

            self.drift_report_file_path: Path = (
                self.data_validation_dir /
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR /
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
            )
        except Exception as e:
            raise CustomException(e)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_transformation_dir: Path = (
                training_pipeline_config.artifact_dir / training_pipeline.DATA_TRANSFORMATION_DIR_NAME
            )

            self.transformed_train_file_path: Path = (
                self.data_transformation_dir /
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR /
                training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
            )

            self.transformed_test_file_path: Path = (
                self.data_transformation_dir /
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR /
                training_pipeline.TEST_FILE_NAME.replace("csv", "npy")
            )

            self.transformed_object_file_path: Path = (
                self.data_transformation_dir /
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR /
                training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
            )
        except Exception as e:
            raise CustomException(e)
    
