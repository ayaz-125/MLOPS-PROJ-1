import os                # For accessing environment variables
import sys               # For system-level exceptions
import pymongo           # For MongoDB connection
import certifi           # For SSL certificate verification

from src.exception import MyException  # Custom exception class
from src.logger import logging         # Logging module
from src.constants import DATABASE_NAME, MONGODB_URL_KEY  # Project constants

# Load SSL certificate to avoid connection timeout errors
import certifi
# ca = certifi.where()
# client = MongoClient(MONGODB_URL_KEY, tlsCAFile=ca)

ca = certifi.where()  # This line automatically finds the CA certificate file

class MongoDBClient:
    """
    This Class is used to Connect MongoDB Database.
    It creates a single shared MongoDB client for the entire project.
    """

    client = None  # This will hold a single MongoDB connection across all objects.

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        This Constructor is automatically called when MongoDBClient() is created.

        Parameters:
        ----------
        database_name : str
            Name of MongoDB Database (Default = DATABASE_NAME)

        Function Steps:
        1. Check if MongoDB connection is already created or not.
        2. If not, create a new connection.
        3. Connect to the given Database.
        4. Raise Custom Exception if anything goes wrong.
        """
        try:
            # Step 1: Check if connection already exists
            if MongoDBClient.client is None:
                # Step 2: Get MongoDB URL from Environment Variables
                mongo_db_url = os.getenv(MONGODB_URL_KEY)  
                
                if mongo_db_url is None:
                    # Raise Exception if MongoDB URL is not found
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                
                # Step 3: Create MongoDB Client
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca,serverSelectionTimeoutMS=100000)
                logging.info("MongoDB Connection Created Successfully.")

            # Step 4: Use Shared MongoDB Connection
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  # Connect to the specific Database
            self.database_name = database_name
            logging.info(f"Connected to MongoDB Database: {database_name}")

        except Exception as e:
            # Raise Custom Exception if Error Occurs
            raise MyException(e, sys)
        

