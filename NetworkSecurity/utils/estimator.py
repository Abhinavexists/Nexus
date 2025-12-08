import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from typing import Any

from NetworkSecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

from NetworkSecurity.logging.logging import logging
from NetworkSecurity.exception.exception import CustomException


class NetworkModel:
    def __init__(self, preprocessor: Pipeline, model: Any):
        try:
            self.preprocessor = preprocessor
            self.model = model

        except Exception as e:
            raise CustomException(e)
        
    def predict(self, x: pd.DataFrame) -> np.ndarray:
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred

        except Exception as e:
            raise CustomException(e)