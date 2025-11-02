import os
import pandas as pd
from scipy.stats import ks_2samp
from pathlib import Path
from typing import Optional

from NetworkSecurity.constant.training_pipeline import SCHEME_FILE_PATH
from NetworkSecurity.entity.config import DataIngestionConfig, DataValidationConfig
from NetworkSecurity.entity.artifact import DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.utils.utils import read_yaml_file, write_yaml_file
from NetworkSecurity.logging.logging import logging


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEME_FILE_PATH)

        except Exception as e:
            raise CustomException(e)
        
    @staticmethod
    def read_file(file_path: Path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required Number of columns: {number_of_columns}")
            logging.info(f"Total number of columns in dataframe: {dataframe.columns}")

            if(number_of_columns == len(dataframe.columns)):
                return True
            else:
                return False

        except Exception as e:
            raise CustomException(e)
        
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold:float = 0.96):
        try:
            drift_status = False
            report = {}

            for columns in base_df.columns:
                d1 = base_df[columns]
                d2 = current_df[columns]
                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    drift_status = True
                
                report.update({columns:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = Path(drift_report_file_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)

            write_yaml_file(drift_report_file_path, report)
            
            return drift_status
                        
        except Exception as e:
            raise CustomException(e)

        
    def intitiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_file(train_file_path)
            test_dataframe = DataValidation.read_file(test_file_path)

            # validate data 
            train_status = self.validate_number_of_columns(train_dataframe)
            test_status = self.validate_number_of_columns(test_dataframe)

            if not train_status:
                error_message = f"Train Dataframe doesn't have all the columns \n"
                raise CustomException(Exception(error_message))
            if not test_status:
                error_message = f"Test Dataframe doesn't have all the columns \n"
                raise CustomException(Exception(error_message))

            status = self.detect_data_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = Path(self.data_validation_config.valid_data_train_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_data_train_path, index=False, header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_data_test_path, index=False, header=True
            )
            data_validation_artifact = DataValidationArtifact(
                            validation_pool=status,
                            valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                            valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                            invalid_train_file_path=Path(""), # used instead of None
                            invalid_test_file_path=Path(""),
                            drift_report_file_path=self.data_validation_config.drift_report_file_path,
                        )
            
            return data_validation_artifact
            
        except Exception as e:
            raise CustomException(e)