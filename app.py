
import os
import certifi
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from uvicorn import run

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.utils.utils import load_object
from src.utils.estimator import NetworkModel
from src.pipeline.training_pipeline import TrainingPipeline
from src.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME,
)

from src.exception.exception import CustomException
from src.logging.logging import logging

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

templates = Jinja2Templates(directory="./templates")

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
    
@app.get("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object(Path("final_model/preprocessor.pkl"))
        final_model = load_object(Path("final_model/model.pkl"))

        Network_model = NetworkModel(preprocessor, final_model)
        print(df.iloc[0])

        y_pred = Network_model.predict(df)
        print(y_pred)

        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        df.to_csv("prediction_output/output.csv")
        index_html = df.to_html(classes='table table-stripped')
        return templates.TemplateResponse("index.html", {"request": request, "table": index_html})

    except Exception as e:
        raise CustomException(e) from e

if __name__ == "__main__":
    run(app, host='localhost', port=8000)