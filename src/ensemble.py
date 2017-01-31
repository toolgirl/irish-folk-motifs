from n_gram import NGramModel
import numpy as np
import itertools
from collections import defaultdict
from math import log



class EnsembleModel(NGramModel):
    """
    Takes in a specified number of n's and creates N grams and then

    Parameters
    ----------
    n : int
        number of n gram models wanted
    corpus : pandas series, string
        both both training and test data.

    Atributes
    ---------



    """
    def __init__(self, n=3):
        self.n = n
        self.models = []
        self.grid_weights = []
        self._create_models()
        self.cumulative_score = None
        self.weighted_frequencies = None
        self.series = None
        self.frequencies = None
        self.weights = None



    # Train the sub models.
    def fit_sub_models(self, series):
        for i, model in enumerate(self.models):
            print "Training model {}".format(i)
            model.fit(series)


    #Creates the required number of models specified by n.
    def _create_models(self):
        for i in range(1, self.n+1):
            #how to deal with the fit method? call after? call now?
            self.models.append(NGramModel(i))


    def construct_grid_weights(self):
        #Create the list of possible weights to use for grid searching.
        list_of_weights = np.linspace(0, 1, 6)
        for element in itertools.product(list_of_weights, repeat=self.n - 1):
            if sum(element) <= 1:
                last = 1 - sum(element)
                x = list(element)
                x.append(last)
                self.grid_weights.append(tuple(x))




    def sum_of_log_probabilities(self, new_tune, list_of_weights):
        sum_of_log_probs = 0
        largest_model = self.models[-1]
        working_tune = largest_model._pad_string(new_tune)
        for i in xrange(largest_model.n - 1, len(working_tune)):
            weighted_frequency = 0
            for weight, model in zip(list_of_weights, self.models):
                history, token = model.get_window_properties(working_tune, i)
                if model.n == 1:
                    weighted_frequency += model.frequencies[token] * weight
                else:
                    weighted_frequency += model.frequencies[history][token] * weight
            sum_of_log_probs += log(weighted_frequency + 1e-10)
        return sum_of_log_probs


    def grid_search(self, series):
        #This needs to take the different weights and different sized
        # n_grams and give back the best combination.
        # What is the perplexity now?
        self.cumulative_score = defaultdict(lambda: 0.0)
        # Get the weights of a given trained model.
        for weights in self.grid_weights:
            for tune in series:
                sums = self.sum_of_log_probabilities(tune, weights)
                self.cumulative_score[weights] += sums

    def find_key_of_max_value(self):
        key = max(self.cumulative_score, key=self.cumulative_score.get)
        self.weights = key
