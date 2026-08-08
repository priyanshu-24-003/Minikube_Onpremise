from pandas import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from src_utils import Credentials, connect_s3, save_model_typ, remove_data
import io

class Model_Pusher():

    def __init__(self, datafile):
        self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
        self.test_data = self.client.fetch_df(datafile)
        print(f"testing data with shape {self.test_data.shape} loaded", )
        self.x = self.test_data.iloc[:,:-1]
        self.y = self.test_data.iloc[:,-1]
        
        self.stage_model = self.client.fetch_model_typ("model/stage//./data/bin/model.pkl")

    def Pull_Best_Model(self,)->RandomForestClassifier:
        """
        Pulls the best model (model/production/model.pkl) from aws-s3 bucket
        """

        self.production_model = self.client.fetch_model_typ("model/Production//./data/bin/model.pkl")

        return self.production_model


    def Evaluate(self)->bool:

        """
        returns True if current model accuracy > best model accuracy
        else returns False
        """
        
        y_stage_model = self.stage_model.predict(self.x)
        acc_y_stage = accuracy_score(self.y, y_stage_model)


        y_best_model = self.Pull_Best_Model().predict(self.x)
        acc_y_best = accuracy_score(self.y, y_best_model)

        print("stage accuracy " ,acc_y_stage, "\n", "production accuracy ", acc_y_best)
        result = True if acc_y_stage >= acc_y_best else False
        return result

    def Pusher(self,):
        """
        Pushes staged model to Production (if stage outperforms Production) to s3
        """
        

        if self.Evaluate():
            modelpath = './data/bin/model.pkl'
            save_model_typ(self.stage_model, modelpath)
            self.client.push_data(modelpath, "model/Production/")
            remove_data(modelpath)
            print("Accepted the model.")
            return True
        else:
            print("Did Not Accept the model.")
            return False
        



if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    MP = Model_Pusher("ingest/test.csv/./data/bin/test_ingest.csv")
    MP.Pusher()
    # MT.Training()    



