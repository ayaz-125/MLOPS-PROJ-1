# Importing necessary libraries
import sys  # Used to access system-specific parameters and functions
import numpy as np  # Used for numerical operations and array manipulation
import pandas as pd  # Used for data manipulation and analysis

# Importing SMOTEENN from imblearn to handle imbalanced datasets
from imblearn.combine import SMOTEENN  # Combines SMOTE and Edited Nearest Neighbours for balancing datasets

# Importing pipeline utilities for data transformation
from sklearn.pipeline import Pipeline  # Used to create machine learning pipelines
from sklearn.preprocessing import StandardScaler, MinMaxScaler  # StandardScaler for Z-score normalization, MinMaxScaler for scaling between 0 and 1
from sklearn.compose import ColumnTransformer  # Used to apply different transformers to different columns

# Importing project-specific constants and entities
from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR  # Constants like target column name and schema file path
from src.entity.config_entity import DataTransformationConfig  # Configuration for data transformation
from src.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact  # Artifact classes for different stages
from src.exception import MyException  # Custom exception class
from src.logger import logging  # Logger to track execution steps
from src.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file  # Utility functions for saving objects and reading YAML files

# DataTransformation Class
class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            # Assigning artifacts and config to instance variables
            self.data_ingestion_artifact = data_ingestion_artifact  # Artifact containing train-test data paths
            self.data_transformation_config = data_transformation_config  # Configuration containing file paths
            self.data_validation_artifact = data_validation_artifact  # Artifact containing validation status
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)  # Reading schema configuration from YAML file
        except Exception as e:
            raise MyException(e, sys)  # Raising custom exception if any error occurs

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)  # Reading CSV file into DataFrame
        except Exception as e:
            raise MyException(e, sys)  # Raising custom exception if reading fails

    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a pipeline object for data transformation.
        It applies StandardScaler and MinMaxScaler to numerical columns.
        """
        logging.info("Entered get_data_transformer_object method")
        try:
            # Creating transformers for numerical columns
            numeric_transformer = StandardScaler()  # Standardizes numerical columns
            min_max_scaler = MinMaxScaler()  # Scales numerical columns between 0 and 1
            
            # Extracting column names from schema
            num_features = self._schema_config['num_features']  # Numerical features
            mm_columns = self._schema_config['mm_columns']  # MinMaxScaler features

            # Defining column transformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("StandardScaler", numeric_transformer, num_features),
                    ("MinMaxScaler", min_max_scaler, mm_columns)
                ],
                remainder='passthrough'  # Remaining columns will pass without transformation
            )

            # Wrapping the preprocessor into a pipeline
            final_pipeline = Pipeline(steps=[("Preprocessor", preprocessor)])
            logging.info("Pipeline Created Successfully")
            return final_pipeline

        except Exception as e:
            logging.exception("Exception occurred in get_data_transformer_object")
            raise MyException(e, sys) from e

    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male"""
        logging.info("Mapping Gender column")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)  # Mapping Gender values to 0 and 1
        return df

    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical columns"""
        logging.info("Creating dummy variables")
        df = pd.get_dummies(df, drop_first=True)  # Creating one-hot encoded dummy variables
        return df

    def _rename_columns(self, df):
        """Rename columns for better understanding"""
        logging.info("Renaming columns")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')  # Converting columns to integer type
        return df

    def _drop_id_column(self, df):
        """Drop ID column"""
        logging.info("Dropping ID column")
        drop_col = self._schema_config['drop_columns']  # Fetching column name from schema
        if drop_col in df.columns:
            df = df.drop(drop_col, axis=1)  # Dropping column
        return df

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """Initiates Data Transformation Pipeline"""
        try:
            print("------------------------------------------------------------------------------------------------")

            logging.info("Starting Data Transformation")

            # Check if data validation is successful
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)

            # Read train and test datasets
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            # Splitting features and target columns
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Applying custom transformations
            input_feature_train_df = self._map_gender_column(input_feature_train_df)
            input_feature_train_df = self._drop_id_column(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columns(input_feature_train_df)

            input_feature_test_df = self._map_gender_column(input_feature_test_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columns(input_feature_test_df)

            # Get Transformer Pipeline
            preprocessor = self.get_data_transformer_object()
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # Handling Imbalanced Dataset using SMOTEENN
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr, target_feature_test_df)

            # Saving Transformation Objects
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, np.c_[input_feature_train_final, target_feature_train_final])
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, np.c_[input_feature_test_final, target_feature_test_final])

            return DataTransformationArtifact(
                self.data_transformation_config.transformed_object_file_path,
                self.data_transformation_config.transformed_train_file_path,
                self.data_transformation_config.transformed_test_file_path
            )
        except Exception as e:
            raise MyException(e, sys) from e
