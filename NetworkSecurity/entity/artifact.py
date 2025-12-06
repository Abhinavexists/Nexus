from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    train_file_path: Path
    test_file_path: Path

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: Path
    valid_test_file_path: Path
    invalid_train_file_path: Path
    invalid_test_file_path: Path
    drift_report_file_path: Path

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: Path
    transformed_train_file_path: Path
    transformed_test_file_path: Path