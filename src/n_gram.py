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
        Size of the window to look at my data.

    Attributes
    ----------
    n_grams_count : defaultdict of Counter()
        Counts the occurance of the last character in a window to the preceding ones.
    frequencies : defaultdict of defaultdicts.
        Holds the frequency a given last character shows up after the preceding ones given that all chararters show up.
    perplexity : float
        Holds the overall perplexity of my model given a new piece of data.

    """
    def __init__(self, n):
        self.n = n
        # dictionary of counters that take a prefix and count all occuranced of what comes after.
        self.n_grams_count = None
        # defaultdict of defaultdict that holds the frequencies of a given suffix.
        self.frequencies = None
        self.score = None

    #Start reading at the token and get the history of it.
    def get_window_properties(self, tune, i):
        window = tune[i - self.n + 1:i + 1]
        history = window[:-1]
        token = window[-1]
        return history, token

    def fit(self, series):
        # For one character at a time.
        if self.n == 1:
            self.n_grams_count = Counter()
            for tune in series.values:
                tune = self._pad_string(tune)
                tune = self._remove_whitespace_punctuation(tune)
                self.n_grams_count += Counter(tune)
            self._create_frequency()

        # for more than 1
        if self.n > 1:
            # Create dictionary of Counter() with the n-gram as key and the
            # follwing next letter as key and the count of that occuring as
            # value.
            self.n_grams_count = defaultdict(lambda: Counter())
            # Go through each tune.
            for tune in series.values:
                tune = self._pad_string(tune)
                tune = self._remove_whitespace_punctuation(tune)
                for i in xrange(self.n - 1, len(tune)):
                    history, token = self.get_window_properties(tune, i)
                    self.n_grams_count[history][token] += 1

            self._create_frequency()

    # This is to make sure the string has the right amount of history.
    def _pad_string(self, tune):
        #pad with n-1 times
        pad = '?' * (self.n - 1)
        tune = pad + tune + '?'
        return tune

    def _remove_whitespace_punctuation(self, tune):
        tune = tune.encode('ascii', errors='ignore')
        tune = string.translate(tune, None, string.punctuation)
        tune = tune.replace(" ", "")
        return tune

    # Calculates the frequency of a given n-gram.
    def _create_frequency(self):
        n_total = 0
        #for n size 1 its simpler and faster.
        if self.n == 1:
            self.frequencies = defaultdict(float)
            total = float(sum(self.n_grams_count.values()))
            #predict method.
            frequencies = {k: v/total for k, v in self.n_grams_count.iteritems()}
            self.frequencies.update(frequencies)

        if self.n >1:
            # Create a dictionary of frequencies that calculates the
            # occurance of a letter after an n-gram and returns the
            # frequency of that. Update self.frequencies
            total_n = 0
            self.frequencies = defaultdict(lambda: defaultdict(float))
            for given, counter in self.n_grams_count.iteritems():
                total_n = float(sum(counter.values()))
                self.frequencies[given] = defaultdict(float, {k: v/total_n for k, v in counter.iteritems()})


#Returns the sum_of_log_probs and perplexity of a given model.
    def perplexity_score(self, new_tune):
        sum_of_log_probs = 0
        for i in xrange(self.n - 1, len(working_tune)):
            history, token = self.get_window_properties(working_tune, i)
            probability = self.frequencies[history][token]
            sum_of_log_probs += log(probability + 1e-10)

        perplexity = 1 - sum_of_log_probs
        self.score = sum_of_log_probs

        return perplexity, sum_of_log_probs
