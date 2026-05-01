from pandas import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

class Model_Pusher():

    def __init__(self, model, test_data:DataFrame):
        self.test_data = test_data
        self.x = self.test_data.iloc[:,:-1]
        self.y = self.test_data.iloc[:,-1]

        self.current_model = model

    def Pull_Best_Model(self,)->RandomForestClassifier:
        """
        Pulls the best model so far from aws-s3 bucket
        """
        return RandomForestClassifier


    def Evaluate(self)->bool:

        """
        returns True if current model accuracy > best model accuracy
        else returns False
        """
        
        y_current_model = self.current_model.predict(self.x)
        acc_y_current = accuracy_score(self.y, y_current_model)


        y_best_model = self.Pull_Best_Model().predict(self.x)
        acc_y_best = accuracy_score(self.y, y_current_model)

        result = True if acc_y_current > acc_y_best else False
        return result

    def Pusher(self,):
        """
        model pusher to s3
        """
        pass

    def Might_Push(self):
        if self.Evaluate():
            self.Pusher()
        else:
            return "Did Not Accept the model."
        

    