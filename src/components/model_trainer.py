# Importing required libraries
import sys  # Used to handle system-specific parameters and functions
from typing import Tuple  # Used to specify the type of return values for better code clarity

# Importing libraries for numerical operations and machine learning
import numpy as np  # Used for working with arrays and numerical data
from sklearn.ensemble import RandomForestClassifier  # RandomForestClassifier from sklearn for classification tasks
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score  # Evaluation metrics for model performance

# Importing custom modules
from src.exception import MyException  # Custom exception class to handle exceptions
from src.logger import logging  # Custom logging module to log information
from src.utils.main_utils import load_numpy_array_data, load_object, save_object  # Utility functions to load and save data and models
from src.entity.config_entity import ModelTrainerConfig  # Configuration class for model trainer parameters
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact  # Classes to manage different artifacts in the pipeline
from src.entity.estimator import MyModel  # Class to encapsulate preprocessing and model objects

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        """
        Constructor method to initialize ModelTrainer class
        :param data_transformation_artifact: Output reference of data transformation artifact stage
        :param model_trainer_config: Configuration for model training
        """
        self.data_transformation_artifact = data_transformation_artifact  # Stores transformed data paths
        self.model_trainer_config = model_trainer_config  # Stores model trainer configuration

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        This function trains a RandomForestClassifier with specified parameters and calculates evaluation metrics
        :param train: Training data
        :param test: Testing data
        :return: Trained model and metric artifact
        """
        try:
            logging.info("Training RandomForestClassifier with specified parameters")
            # Splitting data into features and target
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            logging.info("train-test split done.")

            # Initialize RandomForestClassifier with parameters from configuration
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                min_samples_split=self.model_trainer_config._min_samples_split,
                min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                max_depth=self.model_trainer_config._max_depth,
                criterion=self.model_trainer_config._criterion,
                random_state=self.model_trainer_config._random_state
            )

            # Fit the model to training data
            logging.info("Model training going on...")
            model.fit(x_train, y_train)
            logging.info("Model training done.")

            # Make predictions on test data
            y_pred = model.predict(x_test)
            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            # Create metric artifact to store evaluation results
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            return model, metric_artifact

        except Exception as e:
            raise MyException(e, sys) from e  # Custom exception handling

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        This function initiates the model training steps
        :return: Model trainer artifact containing model path and metrics
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            print("------------------------------------------------------------------------------------------------")
            print("Starting Model Trainer Component")
            # Load transformed train and test data
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info("train-test data loaded")

            # Train model and get metrics
            trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            logging.info("Model object and artifact loaded.")

            # Load preprocessing object
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessing obj loaded.")

            # Check model performance against expected accuracy
            if accuracy_score(train_arr[:, -1], trained_model.predict(train_arr[:, :-1])) < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")

            # Save final model including preprocessing and trained model
            logging.info("Saving new model as performance is better than previous one.")
            my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            # Create ModelTrainerArtifact containing model path and metrics
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys) from e  # Custom exception handling
