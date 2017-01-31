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
from read_abc import construct_tune_list
import glob
import time



# data = read_data('../data/TheSession-data/json/tunes.json')

tunes1001 = construct_tune_list(glob.glob('../data/oneills/1001/T/*.abc'))
data = pd.DataFrame(tunes1001)
shuffled = data.reindex(np.random.permutation(data.index))
train = shuffled[:200]
test = shuffled[-100:]



# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': '|:GE|D2B BAG|BdB A2B|GED G2A|B2B AGE|\rD2B BAG|BdB A2B|GED G2A|BGE G:|\rBd|e2e edB|ege edB|d2B def|gfe dBA|\rG2A B2d|ege d2B|AGE G2A|BGE G:|'})
# tunefr.play()

# ngram2 = NGramModel(2)
# ngram2.fit(data['abc'])

# ngram3 = NGramModel(3)
# ngram3.fit(data['abc'])

# ngram4 = NGramModel(4)
# ngram4.fit(data['abc'])

start_time = time.time()
em = EnsembleModel(n=6)
em.fit_sub_models(train['abc'])
em.construct_grid_weights()
print "I'm grid searching"
em.grid_search(test['abc'])
print("--- %s seconds ---" % (time.time() - start_time))

# print "This is how many {}grams there are:{}".format(ngram2.n, len(ngram2.frequencies))
# print ngram2.perplexity_score('abccecedde,c')
