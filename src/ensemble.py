from n_gram import NGramModel
import numpy as np
import itertools
from collections import defaultdict
from math import log
import json


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
    def __init__(self, n=3, weights=None, model_frequencies=None, model_n_gram_count=None):
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
        self.weighted_frequencies = None

        if weights is not None:
            assert len(weights) == len(self.models)
        self.weights = weights

    # Train the sub models.
    def fit_sub_models(self, series):
        for i, model in enumerate(self.models):
            print "Training model {}".format(i)
            model.fit(series)

    # Creates the required number of models specified by n.
    def _create_models(self):
        self.models = []
        for i in range(self.n):
            self.models.append(NGramModel(i+1, self.model_frequencies[i], self.model_n_gram_count[i]))


    def construct_grid_weights(self):
        # Create the list of possible weights to use for grid searching.
        list_of_weights = np.linspace(0, 1, 6)
        for element in itertools.product(list_of_weights, repeat=self.n - 1):
            if sum(element) <= 1:
                last = 1 - sum(element)
                x = list(element)
                x.append(last)
                self.grid_weights.append(tuple(x))

    def sum_of_log_probabilities(self, new_tune, list_of_weights):
        # cumulative sum of the probabilities of a given token given its
        # history.
        sum_of_log_probs = 0
        largest_model = self.models[-1]
        working_tune = largest_model._pad_string(new_tune)
        working_tune = largest_model._remove_whitespace_punctuation(working_tune)
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

    def generate(self):
        # Create a tune by choosing a model based on weights and then a
        # note based on probability.
        max_length = 400
        tune = self.models[-1].n * "?"
        for i in range(self.n - 1, max_length):
            model = np.random.choice(self.models, 1, p=self.weights)[0]
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
        with open('test_tune.txt', 'w') as f:
            f.write(tune)
        return tune

    def write_to_json(self, filename):
        # This collects the ensemble models weights and the submodels
        # frequencies.
        info = {}
        info['weights'] = self.weights
        info['model_frequencies'] = [model.frequencies for model in self.models]
        info['model_n_gram_count'] = [model.n_gram_count for model in self.models]
        with open(filename, 'w') as fp:
            json.dump(info, fp, indent=4, sort_keys=True)

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

    def get_most_common_grams(self):
        sounds = []
        for model in self.models:
            sounds.append(model.most_common_n_grams)
        return sounds
