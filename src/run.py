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
print len(reel_data)

# scriptdirectory = os.path.dirname(os.path.realpath(__file__))
# tunes1001 = construct_tune_list(glob.glob(os.path.join(scriptdirectory, '../data/oneills/1001/T/*.abc')))
# data = pd.DataFrame(tunes1001)
np.random.seed(seed=6)
shuffled = reel_data.reindex(np.random.permutation(reel_data.index))
reel_train = shuffled[:5214]
reel_verification = shuffled[5214:7822]
reel_test = shuffled[-2608:]
print "There are {} empty cells.".format(reel_train['abc'].isnull().sum())

# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': '|:GE|D2B BAG|BdB A2B|GED G2A|B2B AGE|\rD2B BAG|BdB A2B|GED G2A|BGE G:|\rBd|e2e edB|ege edB|d2B def|gfe dBA|\rG2A B2d|ege d2B|AGE G2A|BGE G:|'})
# tunefr.play()


# start_time = time.time()
# em = EnsembleModel(n=2)
# em.fit_sub_models(reel_train['abc'])
# em.construct_grid_weights()
# print("--- %s seconds ---" % (time.time() - start_time))
# print "I'm grid searching"
# em.grid_search(reel_verification['abc'])
# print("--- %s seconds ---" % (time.time() - start_time))

def make_ensembles():
    ensemble_output = {}
    for i in range(1, 3):
        start_time = time.time()
        em = EnsembleModel(n=i)
        em.fit_sub_models(reel_train['abc'])
        em.construct_grid_weights()
        print("--- %s seconds ---" % (time.time() - start_time))
        print "I'm grid searching"
        em.grid_search(reel_verification['abc'])
        ensemble_output[em.weights] = em.cumulative_score[em.weights]
        print("--- %s seconds ---" % (time.time() - start_time))
        # with open('model_'+str(i)+'.pkl', 'w') as f:
        #     for model in em.models:
        #         pickle.dump(model, f)

    return ensemble_output

results = make_ensembles()
df = pd.DataFrame.from_dict(results.items())
df.columns = ['weights', 'score']
ns = [len(X) for X in results.keys() ]
df['n']=ns
df.sort('n',ascending=True,inplace=True)
df.to_csv('results.csv', index=False)
plt.scatter(df.n.values.tolist(),df.score.values.tolist() )





# print "This is
# how many {}grams there are:{}".format(ngram2.n, len(ngram2.frequencies))
# print ngram2.perplexity_score('abccecedde,c')
