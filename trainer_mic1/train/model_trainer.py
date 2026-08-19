from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from src_utils import Credentials, connect_s3, save_model_typ, remove_data
import io
import logging

class Model_Trainer():
    
    def __init__(self,train_file):
        """
        train_file: training data that this class fetches from s3 bucket.
        """

        try:
            self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
            self.train_data = self.client.fetch_df(train_file)
            print(f"training data with shape {self.train_data.shape} loaded")
            self.X = self.train_data.iloc[:,:-1]
            self.Y = self.train_data.iloc[:,-1]
            logging.info(f"connected to S3 inside {__name__}")

        except Exception as e:
            logging.error(f"Error {e} in {__name__} while connecting to S3 inside Constructor of Model_Trainer class")

            
        
    def Trainer(self,)-> RandomForestClassifier:

        try:
            model = RandomForestClassifier()
            model.fit(self.X, self.Y)
            logging.info(f"Model training complete inside {__name__}")
            return model
        except Exception as e:
            logging.error(f"Error {e} in {__name__} while training model inside Trainer Method")


    def Training(self)-> None:
        """
        Trains model(self.Trainer) --- saves the model artifact
        """
        try:
            model = self.Trainer()

            #saves the model to local data/bin dir
            modelpath = './data/bin/model.pkl'
            save_model_typ(model, modelpath)

            #pushing model from local dir to modle/stage in s3
            self.client.push_data(modelpath, "model/stage/")

            #removing model from local
            remove_data(modelpath)
            logging.info(f"Model Traning Was Successfull inside {__name__}")
            return True
        except Exception as e:
            logging.error(f"Error {e} in {__name__} Inside main function")
            return False
        pass



if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    MT = Model_Trainer('ingest/train.csv/./data/bin/train_ingest.csv')

    MT.Training()    
