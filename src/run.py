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

#Eveything that is not a reel.
not_reel = data[data['type'] != 'reel']

d_tunes = data[data['mode'] == 'Dmajor']
g_tunes = data[data['mode'] == 'Gmajor']


# scriptdirectory = os.path.dirname(os.path.realpath(__file__))
# tunes1850 = construct_tune_list(glob.glob(os.path.join(scriptdirectory, '../data/oneills/1850/X/*.abc')))
# data = pd.DataFrame(tunes1850)

# Setting up the shuffle.
# np.random.seed(seed=6)
shuffled = reel_data.reindex(np.random.permutation(reel_data.index))

#REELS
reel_train = shuffled[:5214]
reel_verification = shuffled[5214:7822]
reel_test = shuffled[-2608:]
# print "There are {} empty cells.".format(reel_train['abc'].isnull().sum())
small_r_train = reel_train[:500]
small_r_test = reel_train[-500:]

#NOT REELS
not_reel_shuffled = not_reel.reindex(np.random.permutation(not_reel.index))
not_reel_train = not_reel_shuffled[:8052]
not_reel_verification = not_reel_shuffled[8052:12078]
not_reel_test = not_reel_shuffled[-4026:]


#D tunes
d_shuffled = d_tunes.reindex(np.random.permutation(d_tunes.index))
d_train = d_shuffled[:3611]
d_verification = d_shuffled[3611:5416]
d_test = d_shuffled[-1805:]

#G tunes
g_shuffled = g_tunes.reindex(np.random.permutation(g_tunes.index))
g_train = g_shuffled[:3766]
g_verification = g_shuffled[3766:5649]
g_test = g_shuffled[-1883:]



# PLAY FRAGMENTS
# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': '|:GE|D2B BAG|BdB A2B|GED G2A|B2B AGE|\rD2B BAG|BdB A2B|GED G2A|BGE G:|\rBd|e2e edB|ege edB|d2B def|gfe dBA|\rG2A B2d|ege d2B|AGE G2A|BGE G:|'})
# tunefr.play()


weights = (0.0, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.19999999999999996)
start_time = time.time()
em = EnsembleModel(n=6, weights=weights)
em.fit_sub_models(g_tunes['abc'])
# em.construct_grid_weights()
# print("--- %s seconds ---" % (time.time() - start_time))
# print "I'm grid searching"
# em.grid_search(test[0])
# print("--- %s seconds ---" % (time.time() - start_time))
tune = em.generate()
em.write_to_json()

tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': tune})
tunefr.play()


# def make_ensembles(train, test, n_grams):
#     "There are {} rows of train data".format(len(train))
#     "There are {} rows of test data".format(len(test))
#     ensemble_output = {}
#     for i in range(1, n_grams):
#         start_time = time.time()
#         em = EnsembleModel(n=i)
#         em.fit_sub_models(train)
#         em.construct_grid_weights()
#         print("--- %s seconds ---" % (time.time() - start_time))
#         print "I'm grid searching"
#         em.grid_search(test)
#         ensemble_output[em.weights] = em.cumulative_score[em.weights]
#         print("--- %s seconds ---" % (time.time() - start_time))
#
#         # with open('model_'+str(i)+'.pkl', 'w') as f:
#         #     for model in em.models:
#
#     return ensemble_output
#
# # results = make_ensembles(train[0], test[0], )
#
# #results = make_ensembles(reel_data['abc'], reel_verification['abc'], 7)
# # results = make_ensembles(small_r_train['abc'], small_r_test['abc'], 5)
# # results = make_ensembles(train_words, test_words, 6)
# # results = make_ensembles(not_reel_train['abc'], not_reel_verification['abc'], 7)
# # results = make_ensembles(d_train['abc'], d_verification['abc'], 8)
# # results = make_ensembles(g_train['abc'], g_verification['abc'], 8)
#
# df = pd.DataFrame.from_dict(results.items())
# df.columns = ['weights', 'score']
# ns = [len(X) for X in results.keys() ]
# df['n']=ns
# df.sort('n',ascending=True,inplace=True)
# df.to_csv('results.csv')
# # plt.scatter(df.n.values.tolist(),df.score.values.tolist() )
#
#
# # Testing model with words. It works
# # words = pd.read_table('../data/alice.txt')
# #
# # train_words = words[:8]
# # test_words = words[-8:]
#
# # Tiny test set for finding out if this works. It works.
# # train = ['edBdBAGF', 'BEEdEEBA', 'DBBBAGBd', 'gfecdfed', 'EGBEGGBA']
# # test = ['agfdegdB']
# # train = pd.DataFrame(train)
# # test = pd.DataFrame(test)
#
#
# # print "This is
# # how many {}grams there are:{}".format(ngram2.n, len(ngram2.frequencies))
# # print ngram2.perplexity_score('abccecedde,c')
