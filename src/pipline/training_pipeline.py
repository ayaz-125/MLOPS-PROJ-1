
import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

from src.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig,
                                          DataTransformationConfig,
                                          ModelTrainerConfig,
                                          ModelEvaluationConfig,
                                          ModelPusherConfig)
                                          
from src.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact,
                                            ModelTrainerArtifact,
                                            ModelEvaluationArtifact,
                                            ModelPusherArtifact)



class TrainPipeline:  #Defines a class named TrainPipeline for handling the training pipeline.
    def __init__(self):   #Initializes an instance of the TrainPipeline class.
        self.data_ingestion_config = DataIngestionConfig()  #	Creates an instance of DataIngestionConfig to store data ingestion configurations.
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
        


    
    def start_data_ingestion(self) -> DataIngestionArtifact:  #Defines a method to start data ingestion and return a DataIngestionArtifact.
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class") #Logs that the method execution has started.
            logging.info("Getting the data from mongodb")  #Logs that data retrieval from MongoDB is starting.
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)  #Creates an instance of DataIngestion, passing the configuration object.
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()  #Calls the method to fetch data, save it, and split it into train/test sets.
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact  #Returns the DataIngestionArtifact containing train and test dataset paths.
        except Exception as e:
            raise MyException(e, sys) from e  #Raises a custom exception MyException with system details for debugging.
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys)



        #This pipeline is for exceuting the code 
    def run_pipeline(self, ) -> None:  #Defines the run_pipeline method, which runs the entire training pipeline. It doesn't return anything (None).
            """
            This method of TrainPipeline class is responsible for running complete pipeline
            """
            try:
                data_ingestion_artifact = self.start_data_ingestion()  #Calls start_data_ingestion() to fetch and prepare train/test datasets.

                data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)  #Calls start_data_validation() to check data quality and integrity.

                data_transformation_artifact = self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)  #Calls start_data_transformation() to preprocess and transform data.

                model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact) #Calls start_model_trainer() to train a machine learning model.

                model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        model_trainer_artifact=model_trainer_artifact)
                if not model_evaluation_artifact.is_model_accepted:
                    logging.info(f"Model not accepted.")
                    return None
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
                
            except Exception as e:
                raise MyException(e, sys)
            

