#!/usr/bin/env python

"""
Main script.
"""

import pandas as pd
import numpy as np
from tune_fragment import TuneFragment
from n_gram import NGram
from data_cleaner import read_data





data = read_data('../data/TheSession-data/json/tunes.json')


# tunefr = TuneFragment({'mode': 'G', 'meter': '6/8', 'abc': '|:GE|D2B BAG|BdB A2B|GED G2A|B2B AGE|\rD2B BAG|BdB A2B|GED G2A|BGE G:|\rBd|e2e edB|ege edB|d2B def|gfe dBA|\rG2A B2d|ege d2B|AGE G2A|BGE G:|'})
# tunefr.play()

# ngram2 = NGram(2)
# ngram2.fit(data['abc'])

# ngram3 = NGram(3)
# ngram3.fit(data['abc'])

ngram4 = NGramModel(4)
ngram4.fit(data['abc'])
print "This is how many {}grams there are:{}".format(ngram4.n, len(ngram4.frequencies))
