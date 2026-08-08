from pandas import DataFrame, read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src_utils import Credentials, connect_s3, save_data, remove_data


class Ingestion():
    
    def __init__(self, datafile):
        self.url = datafile
        pass

    def Ingest(self, )->None:


        #local
        # self.df = read_csv(self.url) 

        #production
        self.client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)
        self.df = self.client.fetch_data(self.url)
    
    def Encoding(self,)->None:
        Le = LabelEncoder()
        Le.fit(self.df['passed'])
        self.df['passed'] = Le.transform(self.df['passed'])

        
    def Spliting(self)->tuple:
        train, test = train_test_split(self.df, test_size=0.2, random_state=42,)

        return (train, test)


    def Ingesting(self):
        self.Ingest()
        self.Encoding()
        train,test = self.Spliting()
        print(train.head(4), train.shape)
        print()
        print(test.head(4), test.shape)

        train_path = "./data/bin/train_ingest.csv"
        test_path = "./data/bin/test_ingest.csv"

        save_data(data=train, path=train_path)
        save_data(data=test, path=test_path)

        self.client.push_data(train_path, f'ingest/train.csv')
        self.client.push_data(test_path, f'ingest/test.csv')
        
        remove_data(path=train_path)
        remove_data(path=test_path)

        
        # a line that saves train data
        # a line that saves test data
        

if __name__ == "__main__":

    #local
    # di = Ingestion(datafile="./data/main.csv")

    #production
    di = Ingestion(datafile="main.csv")


    di.Ingesting()



