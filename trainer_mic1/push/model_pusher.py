from pandas import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from src_utils import Credentials, connect_s3, save_model_typ, remove_data
import io
import logging

logger = logging.getLogger(__name__)

class Model_Pusher():

    def __init__(self, datafile):
        try:
            self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
            self.test_data = self.client.fetch_df(datafile)
            print(f"testing data with shape {self.test_data.shape} loaded", )
            self.x = self.test_data.iloc[:,:-1]
            self.y = self.test_data.iloc[:,-1]
            
            self.stage_model = self.client.fetch_model_typ("model/stage//./data/bin/model.pkl")
            logger.info(f"connected to S3 inside {__name__}")

        except Exception as e:
            logger.error(f"Error {e} in {__name__} while connecting to S3 inside Constructor of Model_Pusher class")


    def Pull_Best_Model(self,)->RandomForestClassifier:
        """
        Pulls the best model (model/production/model.pkl) from aws-s3 bucket
        """
        try:
            self.production_model = self.client.fetch_model_typ("model/Production//./data/bin/model.pkl")
            logger.info('Pulled the best model from production/ inside s3 {__name__}')
            return self.production_model
        except Exception as e:
            logger.error(f"Error {e} in {__name__} while Pulling the best production model from s3 inside Pull_Best_Model")



    def Evaluate(self)->bool:

        """
        returns True if current model accuracy > best model accuracy
        else returns False
        """
        try:
            y_stage_model = self.stage_model.predict(self.x)
            acc_y_stage = accuracy_score(self.y, y_stage_model)


            y_best_model = self.Pull_Best_Model().predict(self.x)
            acc_y_best = accuracy_score(self.y, y_best_model)

            print("stage accuracy " ,acc_y_stage, "\n", "production accuracy ", acc_y_best)
            result = True if acc_y_stage >= acc_y_best else False
            logger.info('Model Evaluation complete inside Evaluate method')
            return result
        except Exception as e:
            logger.error(f"Error {e} in {__name__} while Evaluating the Model")


    def Pusher(self,):
        """
        Pushes staged model to Production (if stage outperforms Production) to s3
        """

      
        try:
            Evaluation = self.Evaluate()
        except Exception as error:
            print("No Production Model Found, Pushing the Latest Model ..")
            Evaluation = True
            pass

        try:            
            if Evaluation:
                print("Pushing Staged Model to Production")
                modelpath = './data/bin/model.pkl'
                save_model_typ(self.stage_model, modelpath)
                self.client.push_data(modelpath, "model/Production/")
                remove_data(modelpath)
                logger.info(f"Accepted the model.{__name__}")
                return "Accepted the model."
            else:
                logger.info(f"Did Not Accept the model. {__name__}")
                return "Did not Accept the model."
        except Exception as e:
                logger.error(f"Error {e} in {__name__} in Pusher Method")
                return "Pusher Method Failed"
            



if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    MP = Model_Pusher("ingest/test.csv/./data/bin/test_ingest.csv")
    MP.Pusher()
    # MT.Training()    



