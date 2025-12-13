# Nexus: Network Security Classification & Phishing Detection

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124-green.svg)](https://fastapi.tiangolo.com/)
[![MLOps](https://img.shields.io/badge/MLOps-Pipeline-red.svg)](https://mlflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A complete MLOps pipeline for classifying network security threats and detecting phishing attacks. This project demonstrates an end-to-end machine learning system with data processing, model training, experiment tracking, and a REST API for predictions.

## What This Project Does

- **Trains ML models** to classify network traffic and identify phishing attempts
- **Automates the entire ML workflow** from data ingestion to model deployment
- **Tracks experiments** with MLflow for reproducibility and model comparison
- **Serves predictions** via FastAPI REST API with interactive documentation
- **Manages artifacts** with AWS S3 for versioning and persistence
- **Stores data** in MongoDB Atlas for scalability

## Quick Start

### Installation

```bash
git clone https://github.com/Abhinavexists/Nexus.git
cd mlops-project
pip install -r requirements.txt
```

### Environment Setup

Create `.env` file in the project root:

```env
MONGO_URL=your_mongodb_atlas_connection_string
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### Run Training Pipeline

```python
from src.pipeline.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
pipeline.run_pipeline()
```

This will:

1. Load data from MongoDB
2. Validate and transform the data
3. Train 5 different ML models
4. Evaluate performance and select the best one
5. Save the model to S3 and log metrics to MLflow

### Start the API Server

```bash
python app.py
```

Then visit `http://localhost:8000/docs` for interactive API documentation.

**Available Endpoints:**

- `GET /train` - Trigger training pipeline
- `POST /predict` - Make predictions on CSV data
- `GET /docs` - Interactive Swagger UI

## Project Structure

```text
src/
├── components/              # ML pipeline components
│   ├── data_ingestion.py   # Load from MongoDB
│   ├── data_validation.py  # Schema & drift checks
│   ├── data_transformation.py # Feature engineering
│   └── model_trainer.py     # Train & evaluate models
├── pipeline/
│   └── training_pipeline.py # Orchestrate workflow
├── cloud/
│   └── s3_syncer.py         # AWS S3 integration
├── entity/                  # Data schemas
├── constant/                # Configuration
├── exception/               # Error handling
├── logging/                 # Logging setup
└── utils/                   # Helper functions

app.py                       # FastAPI application
requirements.txt             # Python dependencies
pyproject.toml              # Project config & build settings
```

## How It Works

### Data Pipeline

1. **Data Ingestion** - Fetch network traffic features from MongoDB Atlas
2. **Validation** - Check schema integrity and detect data drift
3. **Transformation** - Encode categorical features, scale numerical values
4. **Model Training** - Train multiple models with hyperparameter tuning
5. **Evaluation** - Compare accuracy, precision, recall, F1-score
6. **Registry** - Store best model in S3 and MLflow

### Supported Models

- Logistic Regression
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)
- XGBoost

## Experiment Tracking with MLflow

Track all training runs and compare model performance:

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

View at `http://localhost:5000`:

- Training metrics (accuracy, precision, recall, F1-score)
- Model parameter configurations
- Performance comparisons across runs
- Artifact lineage and versions

## Docker Deployment

```bash
docker build -t nexus:latest .
docker run -p 8000:8000 \
  -e MONGO_URL=your_connection_string \
  nexus:latest
```

## Development & Code Quality

### Setup

```bash
pip install -e ".[dev]"
```

### Code Quality Tools

```bash
# Format code
black src/

# Sort imports
isort src/

# Type checking
mypy src/

# Linting
flake8 src/

# Run tests
pytest tests/
```

## Key Technologies

- **FastAPI** - Modern REST API framework with auto-generated documentation
- **MLflow** - Experiment tracking and model registry
- **MongoDB Atlas** - Cloud document database
- **AWS S3** - Artifact storage and versioning
- **scikit-learn** - Machine learning models
- **pandas & numpy** - Data manipulation and numerical computing

## Dependencies

See `requirements.txt` for the complete list. Main dependencies:

- numpy, pandas, scikit-learn (data & ML)
- fastapi, uvicorn (API)
- mlflow (experiment tracking)
- pymongo (database)
- python-dotenv, PyYAML (configuration)

## Error Handling & Logging

Custom exception handling with detailed error context:

```python
from src.exception.exception import CustomException

try:
    # your code
except Exception as e:
    raise CustomException(e)
```

Structured logging throughout:

```python
from src.logging.logging import logging

logging.info("Processing batch...")
logging.error("Failed to load model", exc_info=True)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

## Important Notes

- MongoDB Atlas network access must be configured for your IP
- AWS credentials are required for artifact storage
- Update `.env` before running training
- Check `/logs` directory for detailed debugging information

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Abhinav Kumar Singh**

- Email: abhinavkumarsingh2023@gmail.com
- GitHub: [@Abhinavexists](https://github.com/Abhinavexists)

## Resources

- [Repository](https://github.com/Abhinavexists/Nexus)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MLflow Docs](https://mlflow.org/)
