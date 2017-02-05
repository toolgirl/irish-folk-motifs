import numpy as np
import itertools
from collections import defaultdict
from math import log
import json
from n_gram import NGramModel

DEFAULT_WEIGHTS = {
                    1: (1,),
                    2: (0.0, 1.0),
                    3: (0.0, 0.2, 0.8),
                    4: (0.0, 0.2, 0.2, 0.6),
                    5: (0.0, 0.2, 0.2, 0.2, 0.4),
                    6: (0.0, 0.2, 0.2, 0.2, 0.2, 0.2),
                    7: (0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0)
                    }


class EnsembleModel(NGramModel):
    """
    Takes in a specified number of models with a default at 6 and Instantiates n NGramModel objects.
    Grid search finds the best set of weights for different numbers of models.
    Generate method generates notes from randomly choosing a model and then a token based on the frequency of that token given that history.

    Parameters
    ----------
    n : int, default = 6
        number of n gram models wanted
    model_frequencies : defaultdict of defaultdicts
        Holds the frequencies of the indivdual models frequencies
        (for instatiating from json).
    model_n_gram_count : dict of Counter()
        Count of the model 4 and up most common grams.
    weights : tuple of weights
        Set of weights to give the models when checking pseudo probability of
        a new tune. Defaults have been defined if not given.

    Atributes
    ---------
    models : list
        list of NGramModel objects of n length
    cumulative_score : float
        The pseudo probability a new tune given the weighted input from all the
        model from all models.
    grid_weights : list of tuples
        All possible sets of weights for any sized model.
    """
    def __init__(self, n=6, weights=None, model_frequencies=None, model_n_gram_count=None):
        self.n = n
        self.models = None
        self.grid_weights = None
        if model_frequencies is None:
            self.model_frequencies = [None] * self.n
        else:
            self.model_frequencies = model_frequencies
        if model_n_gram_count is None:
            self.model_n_gram_count = [None] * self.n
        else:
            self.model_n_gram_count = model_n_gram_count
        self._create_models()
        self.cumulative_score = None
        if weights is not None:
            assert len(weights) == len(self.models)
            self.weights = weights
        else:
            self.weights = DEFAULT_WEIGHTS[self.n]

    # Instantiates an instance of EnsembleModel from a .json file.
    @classmethod
    def load_from_json(cls, filename):
        em = None
        with open(filename) as j:
            info = json.load(j)
            n = len(info['weights'])
            weights = info['weights']
            frequencies = info['model_frequencies']
            n_gram_count = info['model_n_gram_count']
            em = cls(n, weights, frequencies, n_gram_count)
        return em

    # Creates a dump of the instance of a given model for later use.
    def write_to_json(self, filename):
        # This collects the ensemble models weights and the submodels
        # frequencies.
        info = {}
        info['weights'] = self.weights
        info['model_frequencies'] = [model.frequencies for model in self.models]
        info['model_n_gram_count'] = [model.n_gram_count for model in self.models]
        with open(filename, 'w') as fp:
            json.dump(info, fp, indent=4, sort_keys=True)

    # Train the sub models.
    def fit_sub_models(self, series):
        for i, model in enumerate(self.models):
            print "Training model {}".format(i)
            model.fit(series)

    # Cumulative sum of the probabilities of a given token given its
    # history.
    def sum_of_log_probabilities(self, new_tune, weights=None):
        if weights is None:
            weights = self.weights
        sum_of_log_probs = 0
        largest_model = self.models[-1]
        working_tune = largest_model._pad_string(new_tune)
        working_tune = largest_model._remove_whitespace_punctuation(working_tune)
        for i in xrange(largest_model.n - 1, len(working_tune)):
            weighted_frequency = 0
            for weight, model in zip(weights, self.models):
                history, token = model.get_window_properties(working_tune, i)
                if model.n == 1:
                    weighted_frequency += model.frequencies[token] * weight
                else:
                    weighted_frequency += model.frequencies[history][token] * weight
            sum_of_log_probs += log(weighted_frequency + 1e-10)
        return sum_of_log_probs

    # Next 3 methods conduct the grid search for the optimal weights.
    def construct_grid_weights(self):
        # Create the list of possible weights to use for grid searching.
        list_of_weights = np.linspace(0, 1, 6)
        for element in itertools.product(list_of_weights, repeat=self.n - 1):
            if sum(element) <= 1:
                last = 1 - sum(element)
                x = list(element)
                x.append(last)
                self.grid_weights.append(tuple(x))

    def grid_search(self, series):
        # This needs to take the different weights and different sized
        # n_grams and give back the best combination.
        self.cumulative_score = defaultdict(float)
        # Get the weights of a given trained model.
        for weights in self.grid_weights:
            for tune in series:
                sums = self.sum_of_log_probabilities(tune, weights)
                self.cumulative_score[weights] += sums
            print '------------'
        self.find_best_weights()

    def find_best_weights(self):
        key = max(self.cumulative_score, key=self.cumulative_score.get)
        self.weights = key

    def generate(self, weights=None):
        # Create a tune by choosing a model based on weights and then a
        # note based on probability.
        if weights is not None:
            weights = weights
        else:
            weights = self.weights
        max_length = 400
        tune = self.models[-1].n * "?"
        for i in range(self.n - 1, max_length):
            model = np.random.choice(self.models, 1, p=weights)[0]
            history, ignore = model.get_window_properties(tune, i)
            choose = model.frequencies[history]
            if model.n == 1 or len(choose) == 0:
                unigram = self.models[0].frequencies
                token = np.random.choice(unigram.keys(), 1, p=unigram.values())[0]
            else:
                token = np.random.choice(choose.keys(), 1, p=choose.values())[0]
            tune += token
            if token == '?':
                break
        tune = tune.replace("?", "")
        tune = tune.replace(" ", "")
        tune = tune.replace('\n', '').replace('\r', '')
        with open('../results/test_tune.txt', 'w') as f:
            f.write(tune)
        return tune

    # Returns the most common patterns from the higher grams.
    def get_most_common_grams(self):
        sounds = []
        assert self.n > 3:
        for model in self.models[3:]:
            sounds.append(model.most_common_n_grams)
        return sounds

    # Creates the required number of models specified by n.
    def _create_models(self):
        self.models = []
        for i in range(self.n):
            self.models.append(NGramModel(i+1, self.model_frequencies[i], self.model_n_gram_count[i]))
