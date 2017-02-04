from ensemble import EnsembleModel
import numpy as np
import pandas as pd
from pandas_ml import ConfusionMatrix


class BinaryNGramClassifier(object):
    '''
    Takes in different models and a new tune and predicts which class the tune belongs to. (Right now model1 is D and model 2 is G)
    Parameters
    ----------

    Attributes
    ----------

    '''
    def __init__(self):
        self.model1 = None
        self.model2 = None
        self.prediction = None

    def train(self, series1, series2):
        self.model1 = EnsembleModel()
        self.model1.fit_sub_models(series1)
        self.model2 = EnsembleModel()
        self.model2.fit_sub_models(series2)


    def predict(self, new_series, class1name, class2name):
        prediction = [None] * len(new_series)
        for i, tune in enumerate(new_series):
            sum1 = self.model1.sum_of_log_probabilities(tune)
            sum2 = self.model2.sum_of_log_probabilities(tune)
            if sum1 > sum2:
                prediction[i] = class1name
            else:
                prediction[i] = class2name
        self.prediction = pd.Series(prediction)

    def score_result(self, series_of_actual_y):

        if len(series_of_actual_y) != len(self.prediction):
            print "Please pass series of the same size as y"
        else:
            y_actu = list(pd.Series(series_of_actual_y, name='Actual'))
            y_pred = list(pd.Series(self.prediction, name='Predicted'))
            cm = ConfusionMatrix(y_actu, y_pred)
            print cm
            cm.print_stats()
