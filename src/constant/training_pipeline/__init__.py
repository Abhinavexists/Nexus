import numpy as np
from pathlib import Path

# Variables for training pipeline
TARGET_COLUMN: str = 'Result'
PIPELINE_NAME: str = 'Nexus'
ARTIFACT_DIR: str = 'Artifacts'
FILE_NAME: str = 'phisingData.csv'

TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEMA_FILE_PATH: Path = Path("data_schema") / "schema.yaml"
SAVED_MODEL_DIR: Path = Path.cwd().joinpath('saved_models')
MODEL_FILE_NAME: str = 'model.pkl'

# Data Ingestion Constant
DATA_INGESTION_COLLECTION_NAME: str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME: str = 'NetworkDatabase'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO: float = 0.2

# Data Validation Constant
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalidated'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

# Data Transformation Constant
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

## knn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

# Model Trainer Constant
MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OCERFITTING_UNDERFITTING_THRESHOLD: float = 0.05

TRAINING_BUCKET_NAME = "Nexus"
