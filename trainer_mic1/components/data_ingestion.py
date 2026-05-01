from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# from src_utils import 


class Ingestion():
    
    def __init__(self):
        pass

    def Ingest(self, url)->None:

        self.df = None # Dataframe
    
    def Encoding(self,)->None:
        Le = LabelEncoder()
        self.df.iloc[:,-1] = Le.fit_transform(self.df.iloc[:, -1])
        
    def Spliting(self)->tuple:
        train, test = train_test_split(self.df, test_size=0.2, random_state=42,)

        return (train, test)

    def Ingesting(self):
        self.Ingest(url='')
        self.Encoding()
        train,test = self.Spliting()
        # a line that saves train data
        # a line that saves test data




