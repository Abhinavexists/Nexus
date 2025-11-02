from pathlib import Path

# Variables for training pipeline
TARGET_COLUMN: str = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR: str = 'Artifacts'
FILE_NAME: str = 'phisingData.csv'

TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEME_FILE_PATH: Path = Path("data_schema") / "schema.yaml"

# Data Ingestion Constant
DATA_INGESTION_COLLECTION_NAME: str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME: str = 'NetworkDatabase'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TEST_TRAIN_SPLIT_RATION: float = 0.2

# Data Validation Constant
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalidated'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'
