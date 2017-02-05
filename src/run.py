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
from classifier import BinaryNGramClassifier





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
reel_shuffled = reel_data.reindex(np.random.permutation(reel_data.index))

#REELS
reel_train = reel_shuffled[:int(len(reel_shuffled)* 0.5)]
reel_verification = reel_shuffled[5214:7822]
reel_test = reel_shuffled[-2608:]
# print "There are {} empty cells.".format(reel_train['abc'].isnull().sum())
small_r_train = reel_train[:500]
small_r_test = reel_train[-500:]




#NOT REELS
not_reel_shuffled = not_reel.reindex(np.random.permutation(not_reel.index))
not_reel_train = not_reel_shuffled[:5000]
not_reel_verification = not_reel_shuffled[8052:12078]
not_reel_test = not_reel_shuffled[-4026:]

train_size = 0.75
#D tunes
d_shuffled = d_tunes.reindex(np.random.permutation(d_tunes.index))
d_train = d_shuffled[:int(len(d_shuffled) * train_size)]
d_test = d_shuffled[len(d_train):]


#G tunes
g_shuffled = g_tunes.reindex(np.random.permutation(g_tunes.index))
g_train = g_shuffled[:int(len(g_shuffled) * train_size)]
g_test = g_shuffled[len(g_train):]

# Create DG dataframe.

dg_test = d_test.append(g_test)
y_test = dg_test.reindex(np.random.permutation(dg_test.index))


# Train and test D, G key classifier. Print confusion Matrix.
# classd = d_train['mode'].iloc[0]
# classg = g_train['mode'].iloc[0]
# bngc = BinaryNGramClassifier()
# bngc.train(d_train['abc'], g_train['abc'])
# bngc.predict(y_test['abc'], classd, classg)
# bngc.score_result(y_test['mode'])
#
#
# # Train and test binary classifier training it on reels and not reels.
# classd = d_train['mode'].iloc[0]
# classg = g_train['mode'].iloc[0]
# bngc1 = BinaryNGramClassifier()
# # Essentially trained on garbage.
# bngc1.train(reel_train['abc'], not_reel_train['abc'])
# bngc1.predict(y_test['abc'], classd, classg)
# bngc1.score_result(y_test['mode'])
# # Train and classify data:


# PLAY FRAGMENTS
weights = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
start_time = time.time()
em = EnsembleModel()
em.fit_sub_models(g_train['abc'])
grams = em.get_most_common_grams()
print grams
# tune = em.generate(weights)

tune2 = '4Bd4dFAGa2gGfBA2eBGAEFEGFGEF4AdGcdcdBdg2bfgdBgAefGe2dgfed2ABGz2GA2BcAG'
# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': tune})
# tunefr.play()


# em.construct_grid_weights()
# print("--- %s seconds ---" % (time.time() - start_time))
# print "I'm grid searching"
# em.grid_search(test[0])
# print("--- %s seconds ---" % (time.time() - start_time))

# em.write_to_json('all_data_models.json')

# tunefr = TuneFragment(tune)

# tunefr.create_abcfile(filename='test_tune.abc')
# tunefr.play()

# EnsembleModel.load_from_json('all_data_models.json')

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
