import numpy as np

from sklearn.metrics import f1_score, precision_score, recall_score, r2_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from src.entity.artifact import ClassificationMetricArtifact
from src.exception.exception import CustomException


def get_classification_score(y_true: np.ndarray, y_pred: np.ndarray) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metric = ClassificationMetricArtifact(
            f1_score = float(model_f1_score),
            precision_score = float(model_precision_score),
            recall_score = float(model_recall_score)
        )

        return classification_metric
    
    except Exception as e:
        raise CustomException(e)
    

def evaluate_models(x_train: np.ndarray,
                   y_train: np.ndarray,
                   x_test: np.ndarray,
                   y_test: np.ndarray,
                   models, 
                   params):
    try:
        report: dict = {}

        for model_name, model in models.items():
            para  = params.get(model_name, {})

            gs = GridSearchCV(model, para, cv=3, verbose=True)
            gs.fit(x_train, y_train)

            # rs = RandomizedSearchCV(model, para, n_iter=50, cv=3, random_state=42, verbose=42)
            # rs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_test_pred = model.predict(x_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report
        
    except Exception as e:
        raise CustomException(e)

    
