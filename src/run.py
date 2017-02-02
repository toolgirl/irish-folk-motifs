#!/usr/bin/env python

"""
Main script.
"""

import pandas as pd
import numpy as np
from tune_fragment import TuneFragment
from n_gram import NGramModel
from data_cleaner import read_data
from ensemble import EnsembleModel
import glob
import time
import os
import cPickle as pickle
import json
import matplotlib.pyplot as plt




scriptdirectory = os.path.dirname(os.path.realpath(__file__))
data = read_data(os.path.join(scriptdirectory, '../data/TheSession-data/json/tunes.json'))

#get just the reels
reel_data = data[data['type'] == 'reel']

# jig_data = data[data['type'] == 'jig']

# words = pd.read_table('../data/alice.txt')
#
#
# train_words = words[:8]
# test_words = words[-8:]

# scriptdirectory = os.path.dirname(os.path.realpath(__file__))
# tunes1850 = construct_tune_list(glob.glob(os.path.join(scriptdirectory, '../data/oneills/1850/X/*.abc')))
# data = pd.DataFrame(tunes1850)
np.random.seed(seed=6)
shuffled = reel_data.reindex(np.random.permutation(reel_data.index))
reel_train = shuffled[:5214]
reel_verification = shuffled[5214:7822]
reel_test = shuffled[-2608:]
# print "There are {} empty cells.".format(reel_train['abc'].isnull().sum())
small_r_train = reel_train[:500]
small_r_test = reel_train[-500:]


# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': '|:GE|D2B BAG|BdB A2B|GED G2A|B2B AGE|\rD2B BAG|BdB A2B|GED G2A|BGE G:|\rBd|e2e edB|ege edB|d2B def|gfe dBA|\rG2A B2d|ege d2B|AGE G2A|BGE G:|'})
# tunefr.play()

# train = ['edBdBAGF', 'BEEdEEBA', 'DBBBAGBd', 'gfecdfed', 'EGBEGGBA']
# test = ['agfdegdB']
# train = pd.DataFrame(train)
# test = pd.DataFrame(test)

# start_time = time.time()
# em = EnsembleModel(n=3)
# em.fit_sub_models(train[0])
# em.construct_grid_weights()
# print("--- %s seconds ---" % (time.time() - start_time))
# print "I'm grid searching"
# em.grid_search(test[0])
# print("--- %s seconds ---" % (time.time() - start_time))



def make_ensembles(train, test, n_grams):
    "There are {} rows of train data".format(len(train))
    "There are {} rows of test data".format(len(test))
    ensemble_output = {}
    for i in range(1, n_grams):
        start_time = time.time()
        em = EnsembleModel(n=i)
        em.fit_sub_models(train)
        em.construct_grid_weights()
        print("--- %s seconds ---" % (time.time() - start_time))
        print "I'm grid searching"
        em.grid_search(test)
        ensemble_output[em.weights] = em.cumulative_score[em.weights]
        print("--- %s seconds ---" % (time.time() - start_time))

        # with open('model_'+str(i)+'.pkl', 'w') as f:
        #     for model in em.models:
    return ensemble_output

# results = make_ensembles(train[0], test[0], )

# results = make_ensembles(reel_data['abc'], reel_verification['abc'], 4)
results = make_ensembles(small_r_train['abc'], small_r_test['abc'], 5)
# results = make_ensembles(train_words, test_words, 6)
df = pd.DataFrame.from_dict(results.items())
df.columns = ['weights', 'score']
ns = [len(X) for X in results.keys() ]
df['n']=ns
df.sort('n',ascending=True,inplace=True)
df.to_csv('results_reels6.csv')
# plt.scatter(df.n.values.tolist(),df.score.values.tolist() )





# print "This is
# how many {}grams there are:{}".format(ngram2.n, len(ngram2.frequencies))
# print ngram2.perplexity_score('abccecedde,c')
