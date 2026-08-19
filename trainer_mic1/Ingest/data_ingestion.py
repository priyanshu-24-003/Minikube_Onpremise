from pandas import DataFrame, read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src_utils import Credentials, connect_s3, save_data, remove_data, save_model_typ
import logging

logger = logging.getLogger(__name__)

class Ingestion():
    
    def __init__(self, datafile):
        self.url = datafile
        pass

    def Ingest(self, )->None:


        #local
        # self.df = read_csv(self.url) 

        #production
        try:
            self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
            self.df = self.client.fetch_df(self.url)
            logger.info(f"connected to S3 inside {__name__}")

        except Exception as e:
            logger.error(f"Error {e} in {__name__} while connecting to S3 inside Ingest Method")
        
    def Encoding(self,)->LabelEncoder:
        try:
            Le = LabelEncoder()
            Le.fit(self.df['passed'])
            self.df['passed'] = Le.transform(self.df['passed'])
            logger.info(f"Method Encoding Succesfull inside {__name__}")
            return Le
        except Exception as e:
            logger.error(f"Error {e} in {__name__} inside Encoding Method")


        
    def Spliting(self)->tuple:
        try:    
            train, test = train_test_split(self.df, test_size=0.2, )
            logger.info(f"Method Spliting Succesfull inside {__name__}")
            return (train, test)
        except Exception as e:
            logger.error(f"Error {e} in {__name__} inside Spliting Method")


    def Ingesting(self):
        try:
            logger.info("Data Ingestion Started...")
            self.Ingest()
            encoder = self.Encoding()
            train,test = self.Spliting()
            print(train.head(4), train.shape)
            print()
            print(test.head(4), test.shape)

            train_path = "./data/bin/train_ingest.csv"
            test_path = "./data/bin/test_ingest.csv"
            encoder_path = "./data/bin/encoder.pkl"

            save_data(data=train, path=train_path)
            save_data(data=test, path=test_path)
            save_model_typ(encoder, encoder_path)

            self.client.push_data(train_path, f'ingest/train.csv')
            self.client.push_data(test_path, f'ingest/test.csv')
            self.client.push_data(encoder_path, f"model/encoder")
            
            remove_data(path=train_path)
            remove_data(path=test_path)
            remove_data(path=encoder_path)
            logger.info('Data Ingestion Completed')
            return True
        except Exception as e:
            logger.error(f"Error {e} in {__name__} inside Ingesting Method")
            return False
        

if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    di = Ingestion(datafile="main.csv")
    di.Ingesting()



