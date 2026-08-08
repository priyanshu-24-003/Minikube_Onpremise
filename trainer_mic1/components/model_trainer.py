from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
# from src_utils import 

class Model_Trainer():
    
    def __init__(self, train_data:DataFrame):
        self.train_data = train_data
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
        # a line that saves the model artifact
        pass
       