import json #Imports the json module for saving validation results in a JSON file.
import sys  #Imports sys for handling system-specific parameters and exceptions.
import os   #Imports os to interact with the operating system (e.g., creating directories).

import pandas as pd

from pandas import DataFrame  #	Imports DataFrame specifically from pandas for type hinting.

from src.exception import MyException  #Imports a custom exception class MyException to handle errors.
from src.logger import logging  #	Imports a logging utility to record logs during execution.
from src.utils.main_utils import read_yaml_file #	Imports a function to read YAML configuration files.
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact #Imports artifact entities related to data ingestion and validation.
from src.entity.config_entity import DataValidationConfig  #Imports the configuration entity for data validation.
from src.constants import SCHEMA_FILE_PATH  #Imports the constant that holds the file path for the schema file.


class DataValidation: #Defines a class DataValidation to handle data validation in the pipeline.
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig): #Defines a class DataValidation to handle data validation in the pipeline.
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact  #Stores the DataIngestionArtifact instance.
            self.data_validation_config = data_validation_config #	Stores the DataValidationConfig instance.
            self._schema_config =read_yaml_file(file_path=SCHEMA_FILE_PATH)  #Reads the schema file (YAML) and stores it in _schema_config.
        except Exception as e:
            raise MyException(e,sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:  #Defines a method to check if the dataset has the required number of columns.
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])  #Compares the number of columns in the DataFrame with the expected number in the schema file.
            logging.info(f"Is required column present: [{status}]")  #Logs whether all required columns are present.
            return status   #Returns True if columns match, otherwise False.
        except Exception as e:
            raise MyException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:  #	Defines a method to check for missing numerical and categorical columns.
        """
        Method Name :   is_column_exist
        Description :   This method validates the existence of a numerical and categorical columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns  #Stores all column names of the DataFrame.
            missing_numerical_columns = []   #Initializes an empty list for missing numerical columns.
            missing_categorical_columns = []   #Initializes an empty list for missing categorical columns.
            for column in self._schema_config["numerical_columns"]:  #Iterates over all expected numerical columns.
                if column not in dataframe_columns:  #Checks if the column is missing.
                    missing_numerical_columns.append(column)  #Appends missing numerical columns to the list.

            if len(missing_numerical_columns)>0:  
                logging.info(f"Missing numerical column: {missing_numerical_columns}") #Logs missing numerical columns.


            for column in self._schema_config["categorical_columns"]:  #Iterates over all expected categorical columns.
                if column not in dataframe_columns:  #Checks if the column is missing.
                    missing_categorical_columns.append(column)  #	Appends missing categorical columns to the list.

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}") #Logs missing categorical columns.

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True  #Returns False if any column is missing; otherwise, True.
        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod   #Declares this method as static (it doesn’t depend on the instance).
    def read_data(file_path) -> DataFrame:  #Defines a method to read a CSV file and return a DataFrame.
        try:
            return pd.read_csv(file_path)   #Reads the CSV file and returns a DataFrame.
        except Exception as e:
            raise MyException(e, sys)
        

    def initiate_data_validation(self) -> DataValidationArtifact:  #Initiates data validation and returns an artifact.

        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            print("------------------------------------------------------------------------------------------------")

            validation_error_msg = ""
            logging.info("Starting data validation")  #Logs the start of data validation.

            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path), #Reads the train and test datasets from file paths.
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            # Checking col len of dataframe for train/test df
            status = self.validate_number_of_columns(dataframe=train_df)  #	Checks if train dataset has the required columns.
            if not status:  #If columns are missing...
                validation_error_msg += f"Columns are missing in training dataframe. "  #	Appends an error message.
            else:
                logging.info(f"All required columns present in training dataframe: {status}")

            status = self.validate_number_of_columns(dataframe=test_df)  #Checks if test dataset has the required columns.
            if not status:  #If columns are missing...
                validation_error_msg += f"Columns are missing in test dataframe. "   #Appends an error message.
            else:
                logging.info(f"All required columns present in testing dataframe: {status}")

            # Validating col dtype for train/test df
            status = self.is_column_exist(df=train_df)  #Checks if train dataset has required numerical/categorical columns.
            if not status:  #If columns are missing...
                validation_error_msg += f"Columns are missing in training dataframe. "  #Appends an error message.
            else:
                logging.info(f"All categorical/int columns present in training dataframe: {status}")

            status = self.is_column_exist(df=test_df) #Checks if test dataset has required numerical/categorical columns.
            if not status:  #If columns are missing...
                validation_error_msg += f"Columns are missing in test dataframe."  #Appends an error message.
            else:
                logging.info(f"All categorical/int columns present in testing dataframe: {status}")

            validation_status = len(validation_error_msg) == 0  #	If validation_error_msg is empty, set validation_status to True.

            data_validation_artifact = DataValidationArtifact(  #Creates a DataValidationArtifact.
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path) #Extracts directory path for validation report.
            os.makedirs(report_dir, exist_ok=True)  #Creates the directory if it does not exist.

            # Save validation status and message to a JSON file
            validation_report = {  #Creates a dictionary to store validation results.
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:  #Opens a JSON file for writing validation results.
                json.dump(validation_report, report_file, indent=4)  #Writes validation results to a JSON file.

            logging.info("Data validation artifact created and saved to JSON file.")  #Logs success message.
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact  #Returns the validation artifact.
        except Exception as e:
            raise MyException(e, sys) from e