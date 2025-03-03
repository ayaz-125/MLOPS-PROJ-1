import os  # This module helps us interact with the operating system like creating folders and files.
from pathlib import Path  # This is used to manage file paths in a clean way.

project_name = "src"  # This is the main project folder name where all subfolders and files will be created.

# List of all files and folders that need to be created
list_of_files = [
    f"{project_name}/__init__.py",  # This makes the 'src' folder a Python package.
    f"{project_name}/components/__init__.py",  # This makes 'components' folder a package.
    f"{project_name}/components/data_ingestion.py",  # File for data ingestion code.
    f"{project_name}/components/data_validation.py",  # File for data validation code.
    f"{project_name}/components/data_transformation.py",  # File for data transformation code.
    f"{project_name}/components/model_trainer.py",  # File for model training code.
    f"{project_name}/components/model_evaluation.py",  # File for model evaluation code.
    f"{project_name}/components/model_pusher.py",  # File for model deployment code.
    f"{project_name}/configuration/__init__.py",  # This makes 'configuration' folder a package.
    f"{project_name}/configuration/mongo_db_connection.py",  # File to connect with MongoDB.
    f"{project_name}/configuration/aws_connection.py",  # File to connect with AWS services.
    f"{project_name}/cloud_storage/__init__.py",  # This makes 'cloud_storage' folder a package.
    f"{project_name}/cloud_storage/aws_storage.py",  # File for AWS storage-related code.
    f"{project_name}/data_access/__init__.py",  # This makes 'data_access' folder a package.
    f"{project_name}/data_access/proj1_data.py",  # File to access data from databases.
    f"{project_name}/constants/__init__.py",  # This makes 'constants' folder a package.
    f"{project_name}/entity/__init__.py",  # This makes 'entity' folder a package.
    f"{project_name}/entity/config_entity.py",  # File for configuration entities like file paths.
    f"{project_name}/entity/artifact_entity.py",  # File for artifact entities like output files.
    f"{project_name}/entity/estimator.py",  # File for model estimation functions.
    f"{project_name}/entity/s3_estimator.py",  # File for AWS S3 model storage.
    f"{project_name}/exception/__init__.py",  # This makes 'exception' folder a package.
    f"{project_name}/logger/__init__.py",  # This makes 'logger' folder a package.
    f"{project_name}/pipline/__init__.py",  # This makes 'pipeline' folder a package.
    f"{project_name}/pipline/training_pipeline.py",  # File for model training pipeline.
    f"{project_name}/pipline/prediction_pipeline.py",  # File for prediction pipeline.
    f"{project_name}/utils/__init__.py",  # This makes 'utils' folder a package.
    f"{project_name}/utils/main_utils.py",  # File for utility functions like saving files.
    "app.py",  # Main application file where Flask or FastAPI code will run.
    "requirements.txt",  # File to store all required libraries for the project.
    "Dockerfile",  # File to create Docker image.
    ".dockerignore",  # File to ignore unnecessary files in Docker image.
    "demo.py",  # Sample demo file to check project structure.
    "setup.py",  # File to install the package.
    "pyproject.toml",  # File to configure project dependencies.
    "config/model.yaml",  # Configuration file for model parameters.
    "config/schema.yaml",  # Configuration file for data schema.
]

# Loop through each file in the list
for filepath in list_of_files:
    filepath = Path(filepath)  # Convert string path to Path object
    filedir, filename = os.path.split(filepath)  # Split folder path and file name

    # If folder doesn't exist, create it
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # exist_ok=True means don't raise error if folder already exists.

    # If file doesn't exist or file is empty, create an empty file
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:  # Create file in write mode
            pass  # 'pass' means do nothing, just create an empty file
    else:
        print(f"file is already present at: {filepath}")  # If file already exists, print message
