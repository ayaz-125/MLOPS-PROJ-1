### Code Explanation - Utility Functions (Line by Line)


import os  # Interacts with the operating system to manage file paths and directories
import sys  # Provides system-specific functions, mainly used for exception handling

import numpy as np  # Library for numerical operations, especially arrays
import dill  # Used to serialize Python objects for saving models
import yaml  # Used to read and write YAML configuration files
from pandas import DataFrame  # Represents tabular data with rows and columns

from src.exception import MyException  # Custom exception class for handling errors
from src.logger import logging  # Logs messages for tracking the flow of execution


def read_yaml_file(file_path: str) -> dict:
    """
    Reads YAML file and returns its content as a dictionary
    """
    try:
        with open(file_path, "rb") as yaml_file:  # Opens the YAML file in binary read mode
            return yaml.safe_load(yaml_file)  # Reads and converts YAML content to dictionary
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content into a YAML file
    """
    try:
        if replace and os.path.exists(file_path):  # Checks if file exists and replace is True
            os.remove(file_path)  # Deletes the existing file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Creates directories if they don't exist
        with open(file_path, "w") as file:  # Opens file in write mode
            yaml.dump(content, file)  # Writes content into the file
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs


def load_object(file_path: str) -> object:
    """
    Loads a serialized object using dill
    """
    try:
        with open(file_path, "rb") as file_obj:  # Opens file in binary read mode
            obj = dill.load(file_obj)  # Deserializes object
        return obj  # Returns the loaded object
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves numpy array to file
    """
    try:
        dir_path = os.path.dirname(file_path)  # Extracts directory path
        os.makedirs(dir_path, exist_ok=True)  # Creates directory if not exist
        with open(file_path, 'wb') as file_obj:  # Opens file in binary write mode
            np.save(file_obj, array)  # Saves numpy array
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads numpy array from file
    """
    try:
        with open(file_path, 'rb') as file_obj:  # Opens file in binary read mode
            return np.load(file_obj)  # Loads numpy array
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs


def save_object(file_path: str, obj: object) -> None:
    """
    Serializes and saves Python object using dill
    """
    logging.info("Entered the save_object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Creates directory if not exist
        with open(file_path, "wb") as file_obj:  # Opens file in binary write mode
            dill.dump(obj, file_obj)  # Serializes and saves object
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise MyException(e, sys)  # Raises custom exception if an error occurs

