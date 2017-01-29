from n_gram import NGramModel
import numpy as np
from itertools import product



class EnsembleModel(NGramModel):
    """
    Takes in a specified number of n's and creates N grams and then

    Parameters
    ----------
    n : int
        number of n gram models wanted
    corpus : pandas series, string
        both both training and test data.


    """
    def __init__(self, n=3):
        self.n = n
        self.models = []
        self.grid_weights = []
        self._create_models()
        self.frequencies = None

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


    def grid_weights(self, string):
        #Create the list of possible weights to use for grid searching.
        for element in itertools.product(np.linspace(0, 1, 11), repeat=self.n - 1):
            if sum(element) <= 1:
                last = 1 - sum(element)
                x = list(element)
                x.append(last)
                self.grid_weights.append(tuple(x))


    def calculate_weighted_frequencies(self, list_of_weights):
        # Given a set of weights finds the weighted frequencies of any letter
        # with an n-1 sized history.
        self.frequencies = defaultdict(lambda: defaultdict(lambda: 0.0))
        largest_model = self.models[-1]
        import pdb; pdb.set_trace()
        for history, token_freq in largest_model.frequencies.iteritems():
            for token in token_freq:
                weighted_sum = 0
                for weight, model in zip(list_of_weights, self.models):
                    if model.n == 1:
                        weighted_sum += model.frequencies[token] * weight
                    else:
                        window = history[- model.n + 1:]
                        weighted_sum += model.frequencies[window][token] * weight
                self.frequencies[history][token] = weighted_sum
