# These are the constant which we will use in the project various times

import os  # Used to work with file paths or directories.
from datetime import date  # Used to get the current date.

# MongoDB connection constants
DATABASE_NAME = "Proj1"  # Name of MongoDB Database
COLLECTION_NAME = "Proj1-data"  # Name of MongoDB Collection (Table)
MONGODB_URL_KEY = "MONGODB_URL"  # Key to store MongoDB URL

# Pipeline and Artifact Directory
PIPELINE_NAME: str = ""  # Name of ML Pipeline (Empty for now)
ARTIFACT_DIR: str = "artifact"  # Folder to store pipeline artifacts like models and data

# Model File
MODEL_FILE_NAME = "model.pkl"  # File name where trained model will be saved

# Target Column
TARGET_COLUMN = "Response"  # Column name which we want to predict
CURRENT_YEAR = date.today().year  # Automatically stores the current year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"  # File to store preprocessing object

# Data File Names
FILE_NAME: str = "data.csv"  # Original Dataset file name
TRAIN_FILE_NAME: str = "train.csv"  # Train dataset file name
TEST_FILE_NAME: str = "test.csv"  # Test dataset file name
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")  # Path of schema.yaml file

# AWS Credentials
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"  # AWS Access Key ID environment variable
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"  # AWS Secret Key environment variable
REGION_NAME = "us-east-1"  # AWS Region Name

"""
Data Ingestion Constants
"""
DATA_INGESTION_COLLECTION_NAME: str = "Proj1-data"  # MongoDB collection name for data
DATA_INGESTION_DIR_NAME: str = "data_ingestion"  # Folder to store ingested data
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Folder to store features data
DATA_INGESTION_INGESTED_DIR: str = "ingested"  # Folder to store final ingested data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25  # Splitting ratio for train and test data

"""
Data Validation Constants
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"  # Folder to store validation reports
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"  # Validation report file name

"""
Data Transformation Constants
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"  # Folder to store transformed data
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"  # Transformed data folder
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"  # Folder to store transformation objects like encoders or scalers

"""
Model Trainer Constants
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"  # Folder to store trained models
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"  # Directory where model.pkl will be saved
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"  # Model file name
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6  # Minimum model score expected
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")  # Model config file path
MODEL_TRAINER_N_ESTIMATORS = 20  # Number of Trees in Random Forest
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7  # Minimum number of samples to split the node
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6  # Minimum number of samples at leaf node
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10  # Maximum depth of tree
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'  # Splitting criteria
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101  # Random state for reproducibility

"""
Model Evaluation Constants
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02  # Minimum model performance improvement required
MODEL_BUCKET_NAME = "my-model-mlopsproj14"  # AWS S3 bucket name to store models
MODEL_PUSHER_S3_KEY = "model-registry"  # Folder inside S3 bucket to store models

# Flask App Constants
APP_HOST = "0.0.0.0"  # Host to run Flask app publicly
APP_PORT = 5000  # Port Number to run Flask App
