import os
import sys
import numpy as np
import pandas as pd
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from sklearn.model_selection import train_test_split

from NetworkSecurity.entity.config import DataIngestionConfig
from NetworkSecurity.entity.artifact import DataIngestionArtifact
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e)
        
    def export_collection_as_dataframe(self):
        """Fetch collection data from MongoDB and return it as a DataFrame."""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = MongoClient(MONGO_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)
            return df
        
        except Exception as e:
            raise CustomException(e)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """Save the fetched data into a local feature store CSV."""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            feature_store_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Feature store saved at: {feature_store_file_path}")
            
            return dataframe
        
        except Exception as e:
            raise CustomException(e)
        
    def split_data_into_test_train(self, dataframe: pd.DataFrame):
        """Split the dataset into train and test sets and store them."""
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42,
            )

            logging.info("Performing Train-Test split on dataframe.")

            train_path = Path(self.data_ingestion_config.training_file_path)
            test_path = Path(self.data_ingestion_config.testing_file_path)

            train_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.parent.mkdir(parents=True, exist_ok=True)

            train_set.to_csv(train_path, index=False, header=True)
            test_set.to_csv(test_path, index=False, header=True)

            logging.info(f"Train and test data exported:\nTrain → {train_path}\nTest → {test_path}")

        except Exception as e:
            raise CustomException(e)
        
    def initiate_data_ingestion(self):
        """Main pipeline that runs data fetching, storing, and splitting."""
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_into_test_train(dataframe)
            
            artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            
            logging.info("Data ingestion completed successfully.")
            return artifact

        except Exception as e:
            raise CustomException(e)
