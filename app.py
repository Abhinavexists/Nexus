
import os
import certifi
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from uvicorn import run

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline
from NetworkSecurity.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME,
)

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging

load_dotenv()

uri = os.getenv('MONGO_URL')
logging.info('MONGODB is set and ready to use')

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=False,
    server_api=ServerApi('1'),
    serverSelectionTimeoutMS=10000
    )

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is Successful")
    
    except Exception as e:
        raise CustomException(e) from e

if __name__ == "__name__":
    run(app, host='localhost', port=8000)