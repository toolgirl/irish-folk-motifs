#!/usr/bin/env python

"""
Main script.
"""

import pandas as pd
import numpy as np
from tune_fragment import TuneFragment





data = pd.read_json('../data/TheSession-data/json/tunes.json')

tunefr = TuneFragment({'mode': 'Dmajor', 'abc': 'EFGA | B2 B2 e2 B2'})
tunefr.play()
