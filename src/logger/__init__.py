import logging  # This module is used to create logs in the application.
import os  # This module helps to interact with the operating system (like creating folders).
from logging.handlers import RotatingFileHandler  # This class automatically rotates log files when they reach a certain size.
from from_root import from_root  # This function gives the root folder path of the project.
from datetime import datetime  # This module provides the current date and time.

# Constants for log setup
LOG_DIR = 'logs'  # Name of the folder where log files will be saved.
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # Log file name with current date and time.
# LOG_FILE = 'AYAZ.log'
MAX_LOG_SIZE = 5 * 1024 * 1024  # Maximum log file size is set to 5 MB.
BACKUP_COUNT = 3  # Only 3 backup log files will be kept.

# Log file path setup
log_dir_path = os.path.join(from_root(), LOG_DIR)  # Create full folder path like 'root_folder/logs'.
os.makedirs(log_dir_path, exist_ok=True)  # If the folder doesn't exist, it will create the folder automatically.
log_file_path = os.path.join(log_dir_path, LOG_FILE)  # Complete log file path including file name.

def configure_logger():
    """
    This function configures the logging system to write logs to both a file and the console.
    """
    logger = logging.getLogger()  # Create a logger object.
    logger.setLevel(logging.DEBUG)  # Set log level to DEBUG, which means all logs will be recorded (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    
    # Log message format
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # File handler with rotation (logs will rotate if the file reaches 5 MB)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)  # Attach the log format to file logs.
    file_handler.setLevel(logging.DEBUG)  # Save all logs from DEBUG level and above.
    
    # Console handler (display logs in the terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)  # Attach the log format to console logs.
    console_handler.setLevel(logging.INFO)  # Display only INFO level and higher logs in the terminal.
    
    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Start logging setup by calling the function
configure_logger()


'''
Summary

------>This code automatically creates log files inside the 'logs' folder.

------>It saves logs both in files and displays them on the console.

------>If the log file exceeds 5 MB, it automatically creates a new file and keeps only 3 backup files.

------>The log format includes time, logger name, log level, and message.

'''