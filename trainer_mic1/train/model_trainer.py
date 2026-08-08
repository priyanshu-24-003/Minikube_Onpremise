from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from src_utils import Credentials, connect_s3, save_model_typ, remove_data
import io

class Model_Trainer():
    
    def __init__(self,train_file):
        self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
        self.train_data = self.client.fetch_df(train_file)
        self.X = self.train_data.iloc[:,:-1]
        self.Y = self.train_data.iloc[:,-1]
    
    def Trainer(self,)-> RandomForestClassifier:

        model = RandomForestClassifier()
        model.fit(self.X, self.Y)

        return model

    def Training(self)-> None:
        """
        Trains model(self.Trainer) --- saves the model artifact
        """
        model = self.Trainer()

        modelpath = './data/bin/model.pkl'
        save_model_typ(model, modelpath)

        #pushing model to stage
        self.client.push_data(modelpath, "model/stage/")

        remove_data(modelpath)
        
        pass



if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    MT = Model_Trainer('ingest/train.csv/./data/bin/train_ingest.csv')

    MT.Training()    
