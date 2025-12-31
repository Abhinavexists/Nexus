import json
import os
from pathlib import Path

import certifi
import pandas as pd
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.exception.exception import CustomException
from src.logger.logger import logging

load_dotenv()

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

uri = os.getenv("MONGO_URL")
logging.info("MONGODB is set and ready to use")


class NetworkDataExtract:
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise CustomException(e)

    def convert_csv_to_json(self, file_path: Path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info("records are ready")
            return records

        except Exception as e:
            raise CustomException(e)

    def insert_data_to_mongo(self, records, database, collections):
        try:
            self.records = records
            self.database = database
            self.collections = collections
            self.mongo_client = MongoClient(
                uri,
                tls=True,
                tlsCAFile=certifi.where(),
                tlsAllowInvalidCertificates=False,
                server_api=ServerApi("1"),
                serverSelectionTimeoutMS=10000,
            )
            self.database = self.mongo_client[self.database]
            self.collections = self.database[self.collections]
            self.collections.insert_many(records)
            logging.info("collections is ready")

            return len(self.records)

        except Exception as e:
            raise CustomException(e)


if __name__ == "__main__":
    FILE_PATH = Path("data/phisingData.csv")
    DATABASE = "NetworkDatabase"
    Collections = "NetworkData"
    nde = NetworkDataExtract()
    records = nde.convert_csv_to_json(FILE_PATH)
    no_of_records = nde.insert_data_to_mongo(
        records=records, database=DATABASE, collections=Collections
    )
    print(no_of_records)
