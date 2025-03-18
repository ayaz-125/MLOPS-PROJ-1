### Code Explanation - Data Ingestion Class (Line by Line)


import os  # Used to interact with the operating system, create folders, and manage file paths
import sys  # Provides access to system-specific parameters and functions, mainly used for exception handling

from pandas import DataFrame  # DataFrame is a two-dimensional table used to store and manipulate data
from sklearn.model_selection import train_test_split  # Splits data into training and testing datasets

from src.entity.config_entity import DataIngestionConfig  # Configuration class that stores file paths and split ratio settings
from src.entity.artifact_entity import DataIngestionArtifact  # Stores paths of training and testing files after data ingestion
from src.exception import MyException  # Custom exception class to handle and log errors
from src.logger import logging  # Logs messages for tracking execution flow
from src.data_access.proj1_data import Proj1Data  # Connects with MongoDB to extract data
from src.constants import *

class DataIngestion:   #Defines the DataIngestion class, which handles the data ingestion process.
    
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):  #Initializes an instance of the class with a default DataIngestionConfig object.
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config  # Assigns the provided or default DataIngestionConfig object to the class variable.
        except Exception as e:
            raise MyException(e, sys)  # Catches initialization errors, logs them, and raises a custom exception.

    def export_data_into_feature_store(self) -> DataFrame:
        
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception

        This function extracts data from MongoDB, converts it into a Pandas DataFrame, 
        logs its shape, and saves it as a CSV file at a specified location. If an error occurs, 
        it logs the issue and raises a custom exception. 
        """
        try:
            logging.info("Exporting data from MongoDB")  # Logs the start of the data export process.

            my_data = Proj1Data()  # Creates an object to fetch data from MongoDB

            # This line retrieves data from a specified collection (defined in the configuration) 
            # and exports it as a Pandas DataFrame for further processing
            dataframe = my_data.export_collection_as_dataframe(
                collection_name=DATA_INGESTION_COLLECTION_NAME)  # Retrieves data from MongoDB and converts it into a Pandas DataFrame.

            logging.info("load hogya dataframe ")
            logging.info(f"Shape of dataframe: {dataframe.shape}")  # Logs the shape of the retrieved DataFrame.

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path  # Gets the file path where the CSV will be saved.
            
            # This is just for the understanding of the directory name and the file name.
            # logging.info(f"directory name of the ---->{os.path.dirname(feature_store_file_path)}") -- output-artifact\03_08_2025_14_20_01\data_ingestion\feature_store
            # logging.info(f"file name of the feature_store_dir---->{os.path.basename(feature_store_file_path)}") -- output-data.csv


            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)  # Extracts the directory from the file path and creates it if it doesn't exist.

            dataframe.to_csv(feature_store_file_path, index=False, header=True)  # 	Saves the DataFrame as a CSV file.

            return dataframe  # Returns the DataFrame for further processing.

        except Exception as e:
            raise MyException(e, sys)  # Catches any errors, logs them, and raises a custom exception.

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        This function splits the given DataFrame into training and testing sets based on a 
        predefined ratio and saves them as CSV files in a specified directory. If an error occurs,
        it logs the issue and raises a custom exception.
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)  # Splits the DataFrame into training and testing sets based on the defined ratio.
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)  # Ensures the directory for storing train/test data exists, creates it if needed.
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)  # Saves the training set as a CSV file.
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)  # Saves the testing set as a CSV file.
        except Exception as e:
            raise MyException(e, sys)  # Catches errors, logs them, and raises a custom exception.

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception

        This function initiates the data ingestion process by extracting data from MongoDB, 
        saving it as a CSV file, and splitting it into training and testing sets. 
        It then returns a DataIngestionArtifact containing the file paths of the train and 
        test datasets
        """
        try:
            print("------------------------------------------------------------------------------------------------")

            dataframe = self.export_data_into_feature_store()  # Calls the method to fetch and export data into a CSV file.
            self.split_data_as_train_test(dataframe)  # 	Splits the exported data into training and testing sets.
            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)  # Returns a DataIngestionArtifact containing the paths of train and test data.
               
        except Exception as e:
            raise MyException(e, sys)  # Catches any error, logs it, and raises a custom exception.




