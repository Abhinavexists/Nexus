import os
from pathlib import Path
from datetime import datetime
from NetworkSecurity.constant import training_pipeline
from exception.exception import CustomException

# The problem: mutable/default argument trap
# datetime.now() is evaluated once at function definition time, not each time when create a new object.
# So if i create multiple instances of TrainingPipelineConfig, they’ll all get the same timestamp (the time the class was first defined), 
# not the time of creation.

# class TrainingPipeineConfig:
#     def __init__(self, timestamp = datetime.now()):
#         timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
#         self.pipeline_name = training_pipeline.PIPELINE_NAME
#         self.artifact_name = training_pipeline.ARTIFACT_DIR
#         self.artifact_dir = Path(self.artifact_name).joinpath(timestamp)
#         self.timestamp: str = timestamp


class TrainingPipeineConfig:
    def __init__(self, timestamp:str | None = None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir: Path = Path(self.artifact_name) / timestamp
        self.timestamp: str = timestamp
        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipeineConfig):
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