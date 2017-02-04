from collections import Counter, defaultdict
import pandas as pd
import numpy as np
from math import log
import string


class NGramModel(object):
    """
    Takes a series from a DataFrame and an n and trains a model of a given n.

    Parameters
    ----------
    n : int
        Size of the window to of characters to look at.
    frequencies : dict of dicts, optional
        Contains frequencies if the models is being instantiated from json.
    n_gram_count : dict, optional
        Contains counts of all the n_grams if the model is being instantiated from json.

    Attributes
    ----------
    n : int
        Size of the window of characters to consider in the string.
    token_count : defaultdict of Counter()
        Counts the occurance of the last character in a window to the preceding ones.
    frequencies : defaultdict of defaultdicts.
        Holds the frequency a given last character shows up after the preceding ones
        given that all chararters show up.
    score : float
        Pseudo probability of a token given its history.
    n_gram_count : str
        Count of a window of size n. This can give me the most frequent combinations of sounds.
    """
    def __init__(self, n, frequencies=None, n_gram_count=None):
        self.n = n
        # dictionary of counters that take a prefix and count all occuranced of what comes after.
        self.token_count = None
        # defaultdict of defaultdict that holds the frequencies of a given suffix.
        if frequencies is not None:
            self._convert_to_defaultdict(frequencies)
        else:
            self.frequencies = None
        self.score = None
        if n_gram_count is not None:
            self.n_gram_count = Counter(n_gram_count)
        else:
            self.n_gram_count = None

    # Create dictionary of Counter() with the n-gram as key and the
    # follwing next letter as key and the count of that occuring as
    # value.
    def fit(self, series):
        if self.n == 1:
            self.token_count = Counter()
            for tune in series.values:
                tune = self._pad_string(tune)
                tune = self._remove_whitespace_punctuation(tune)
                self.token_count += Counter(tune)
            self.n_gram_count = self.token_count
            self._create_frequency()
        # for more than 1
        if self.n > 1:
            self.token_count = defaultdict(lambda: Counter())
            self.n_gram_count = Counter()
            # Go through each tune.
            for tune in series.values:
                tune = self._pad_string(tune)
                tune = self._remove_whitespace_punctuation(tune)
                for i in xrange(self.n - 1, len(tune)):
                    history, token = self.get_window_properties(tune, i)
                    self.token_count[history][token] += 1
                    ngram = history + token
                    self.n_gram_count[ngram] += 1
            self._create_frequency()

    # Returns the  psydo probability and perplexity of a given model.
    def perplexity_score(self, new_tune):
        sum_of_log_probs = 0
        for i in xrange(self.n - 1, len(working_tune)):
            history, token = self.get_window_properties(working_tune, i)
            probability = self.frequencies[history][token]
            sum_of_log_probs += log(probability + 1e-10)
        perplexity = 1 - sum_of_log_probs
        self.score = sum_of_log_probs
        return perplexity, sum_of_log_probs

    # Start reading at the token and get the history of it.
    def get_window_properties(self, tune, i):
        window = tune[i - self.n + 1:i + 1]
        history = window[:-1]
        token = window[-1]
        return history, token

    # This ensures a string has n-1 amount of history.
    def _pad_string(self, tune):
        pad = '?' * (self.n - 1)
        tune = pad + tune + '?'
        return tune

    def _remove_whitespace_punctuation(self, tune):
        tune = tune.encode('ascii', errors='ignore')
        tune = string.translate(tune, None, string.punctuation)
        tune = tune.replace(" ", "")
        return tune

    # Calculates the frequency of a token by deviding this token by
    # the number of tokens that follow a given history. Updates self.frequencies.
    def _create_frequency(self):
        n_total = 0
        # Special case for n == 1.
        if self.n == 1:
            self.frequencies = defaultdict(float)
            total = float(sum(self.token_count.values()))
            frequencies = {k: v/total for k, v in self.token_count.iteritems()}
            self.frequencies.update(frequencies)
        if self.n > 1:
            total_n = 0
            self.frequencies = defaultdict(lambda: defaultdict(float))
            for given, counter in self.token_count.iteritems():
                total_n = float(sum(counter.values()))
                self.frequencies[given] = defaultdict(float, {k: v/total_n for k, v in counter.iteritems()})

        # Converts frequencies if handed in at instatiation to a defaultdict.
        def _convert_to_defaultdict(self, frequencies):
            if self.n == 1:
                self.frequencies = defaultdict(float, frequencies)
            else:
                self.frequencies = defaultdict(lambda: defaultdict(float))
                for history, token in frequencies.iteritems():
                    self.frequencies[history] = defaultdict(float, token)

    # Returns the 10 most common n_grams.
    @property
    def most_common_n_grams(self):
        return self.n_gram_count.most_common(10)
