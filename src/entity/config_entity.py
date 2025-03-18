import os  # Used to handle file and directory paths.
from src.constants import *  # Importing all project constants.
from dataclasses import dataclass  # Automatically creates constructor for class.
from datetime import datetime  # Used to get current date and time.

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")  
# Stores the current date and time in format like '03_05_2025_10_30_45'.

@dataclass
class TrainingPipelineConfig:  # this function is common for all the other components like data ingestion,data validation,model trainer, model evaluation
    pipeline_name: str = PIPELINE_NAME  # Assigns pipeline name from constants.
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)  
    # Creates artifact folder path with timestamp.
    timestamp: str = TIMESTAMP  # Stores timestamp value.

# Creates object to access pipeline config easily.
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)  
    # Folder path where data will be stored.  example = artifacts/03_05_2025_12_30_45/data_ingestion
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)  
    # Path to store raw data.
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)  
    # Path to store training data.
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)  
    # Path to store testing data.
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO  
    # Splitting data into train and test based on ratio.
    collection_name: str = DATA_INGESTION_COLLECTION_NAME  
    # MongoDB collection name for data storage.


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    validation_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_FILE_NAME.replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   TEST_FILE_NAME.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                     PREPROCSSING_OBJECT_FILE_NAME)
    
@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    _n_estimators = MODEL_TRAINER_N_ESTIMATORS
    _min_samples_split = MODEL_TRAINER_MIN_SAMPLES_SPLIT
    _min_samples_leaf = MODEL_TRAINER_MIN_SAMPLES_LEAF
    _max_depth = MIN_SAMPLES_SPLIT_MAX_DEPTH
    _criterion = MIN_SAMPLES_SPLIT_CRITERION
    _random_state = MIN_SAMPLES_SPLIT_RANDOM_STATE

@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME

@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME

@dataclass
class VehiclePredictorConfig:
    model_file_path: str = MODEL_FILE_NAME
    model_bucket_name: str = MODEL_BUCKET_NAME